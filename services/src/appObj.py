#appObj.py - This file contains the main application object
# to be constructed by app.py

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj, readFromEnviroment, getInvalidEnvVarParamaterException

def readDictFromEnviroment(
  env,
  envVarName,
  defaultValue,
  safeToOutput=False
):
  valueJSON = readFromEnviroment(
    env=env,
    envVarName=envVarName,
    defaultValue=defaultValue,
    acceptableValues=None
  )
  valueDict = None
  try:
    if valueJSON != '{}':
      valueDict = json.loads(valueJSON)
  except Exception as err:
    print("Error parsing JSON for " + envVarName)
    if safeToOutput:
      print("Value:" + valueJSON + ":")
    print(err)  # for the repr
    print(str(err))  # for just the message
    print(err.args)  # the arguments that the exception has been called with.
    raise getInvalidEnvVarParamaterException(envVarName=envVarName, actualValue=None, messageOverride=None)

  if isinstance(valueDict, str):
    # Codfresh container test has problems passing json this deals with it's input
    print(envVarName + " parsing First JSON pass gave string")
    #####print("XXX", valueDict) (This debug comment may display a password)
    valueDict = json.loads(valueDict)

    if not valueDict is None:
      if not isinstance(valueDict, dict):
        print(envVarName + " did not evaluate to a dictionary")
        raise getInvalidEnvVarParamaterException(envVarName=envVarName, actualValue=None, messageOverride=None)

  return valueDict

import constants
import json

import logging
import sys
import APIs

import Logic

from object_store_abstraction import createObjectStoreInstance

invalidConfigurationException = constants.customExceptionClass('Invalid Configuration')

InvalidObjectStoreConfigInvalidJSONException = constants.customExceptionClass('APIAPP_OBJECTSTORECONFIG value is not valid JSON')
InvalidRedirectPrefixException = constants.customExceptionClass('APIAPP_REDIRECTPREFIX value is not valid - can not end with slash, must start with http:// or https://')

class appObjClass(parAppObj):
  objectStore = None
  APIAPP_OBJECTSTOREDETAILLOGGING = None
  APIAPP_REDIRECTPREFIX = None
  APIAPP_URLEXPIREDAYS = None
  APIAPP_DESTWHITELIST = None
  accessControlAllowOriginObj = None

  shortUrlFunctions = None

  def setupLogging(self):
    root = logging.getLogger()
    #root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

  def init(self, env, serverStartTime, testingMode = False):
    ##self.setupLogging() Comment in when debugging

    super(appObjClass, self).init(env, serverStartTime, testingMode, serverinfoapiprefix='public/info')
    ##print("appOBj init")

    self.APIAPP_REDIRECTPREFIX = readFromEnviroment(
      env=env,
      envVarName='APIAPP_REDIRECTPREFIX',
      defaultValue=None,
      acceptableValues=None,
      nullValueAllowed=False
    )
    print("APIAPP_REDIRECTPREFIX:", self.APIAPP_REDIRECTPREFIX)
    if self.APIAPP_REDIRECTPREFIX.endswith("/"):
      raise InvalidRedirectPrefixException
    if not self.APIAPP_REDIRECTPREFIX.startswith("http://"):
      if not self.APIAPP_REDIRECTPREFIX.startswith("https://"):
        raise InvalidRedirectPrefixException

    self.APIAPP_URLEXPIREDAYS = readFromEnviroment(
      env=env,
      envVarName='APIAPP_URLEXPIREDAYS',
      defaultValue=None,
      acceptableValues=None,
      nullValueAllowed=False
    )
    print("APIAPP_URLEXPIREDAYS:", self.APIAPP_URLEXPIREDAYS)
    self.APIAPP_URLEXPIREDAYS = int(self.APIAPP_URLEXPIREDAYS)
    if (self.APIAPP_URLEXPIREDAYS < 0):
      print("ERROR - Expire days less than 0")
      raise invalidConfigurationException

    objectStoreConfigDict = readDictFromEnviroment(
      env=env,
      envVarName='APIAPP_OBJECTSTORECONFIG',
      defaultValue='{}'
    )

    self.APIAPP_OBJECTSTOREDETAILLOGGING = readFromEnviroment(
      env=env,
      envVarName='APIAPP_OBJECTSTOREDETAILLOGGING',
      defaultValue='N',
      acceptableValues=['Y', 'N'],
      nullValueAllowed=True
    ).strip()
    if (self.APIAPP_OBJECTSTOREDETAILLOGGING=='Y'):
      print("APIAPP_OBJECTSTOREDETAILLOGGING set to Y - statement logging enabled")

    fns = {
      'getCurDateTime': self.getCurDateTime
    }
    self.objectStore = createObjectStoreInstance(
      objectStoreConfigDict,
      fns,
      detailLogging=(self.APIAPP_OBJECTSTOREDETAILLOGGING == 'Y')
    )

    self.shortUrlFunctions = Logic.ShortUrlFunctionClass(appObj=self)

    self.APIAPP_DESTWHITELIST = readDictFromEnviroment(
      env=env,
      envVarName='APIAPP_DESTWHITELIST',
      defaultValue='{}',
      safeToOutput=True
    )
    if self.APIAPP_DESTWHITELIST is None:
      self.APIAPP_DESTWHITELIST = {}
    for curTenant in self.APIAPP_DESTWHITELIST:
      if not isinstance(self.APIAPP_DESTWHITELIST[curTenant], list):
        print("ERROR - APIAPP_DESTWHITELIST tenant values must be lists of string")
        raise invalidConfigurationException
      for ite in self.APIAPP_DESTWHITELIST[curTenant]:
        if not isinstance(ite, str):
          print("ERROR - APIAPP_DESTWHITELIST tenant value lists can only contain strings")
          raise invalidConfigurationException

  def initOnce(self):
    super(appObjClass, self).initOnce()
    ##print("appOBj initOnce")
    APIs.registerAPIs(self)

    self.flastRestPlusAPIObject.title = "Challange Platform"
    self.flastRestPlusAPIObject.description = "API for Challange Platform"

  def stopThread(self):
    ##print("stopThread Called")
    pass

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.stopThread()
    super(appObjClass, self).exit_gracefully(signum, frame)

  def getDerivedServerInfoData(self):
    return {
    }

appObj = appObjClass()

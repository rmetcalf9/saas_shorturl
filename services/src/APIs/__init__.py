from .APIPrivate import registerAPI as private_registerAPI
from .APIPublic import registerAPI as public_registerAPI

def registerAPIs(appObj):
  nsPrivate = appObj.flastRestPlusAPIObject.namespace('private/user', description='Private API')
  private_registerAPI(appObj=appObj, APInamespace=nsPrivate)
  nsPublic = appObj.flastRestPlusAPIObject.namespace('public/r', description='Publice API')
  public_registerAPI(appObj=appObj, APInamespace=nsPublic)

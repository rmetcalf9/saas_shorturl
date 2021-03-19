import TestHelperSuperClass
import LoginUtilities
import json
from object_store_abstraction import RepositoryObjBaseClass
import datetime
import pytz
from appObj import appObj
from dateutil.parser import parse
import constants

targetUrl = "http://random.com/1/2/3"
#targetUrl = "https://challengeswipe.com/#/challengeapp/about"
suspectTargetUrl = "http://suspectrandom.com/1/2/3"

class helpers(TestHelperSuperClass.simpleTests):
  def putUrl(
    self,
    loginSession,
    tenantName,
    url,
    checkAndParseResponse=True,
    msg=""
  ):
    result = self.assertUserPrivateAPIResult(
      methodFN=self.testClient.put,
      url="/" + tenantName + "/shortUrl",
      session=loginSession,
      data={
        "url": url
      }
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 202, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

  def getUrlByCode(
    self,
    loginSession,
    tenantName,
    urlCode,
    checkAndParseResponse=True,
    msg=""
  ):
    result = self.assertUserPrivateAPIResult(
      methodFN=self.testClient.get,
      url="/" + tenantName + "/shortUrl/" + urlCode,
      session=loginSession,
      data=None
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

  def deleteUrlByCode(
    self,
    loginSession,
    tenantName,
    urlCode,
    checkAndParseResponse=True,
    msg=""
  ):
    result = self.assertUserPrivateAPIResult(
      methodFN=self.testClient.delete,
      url="/" + tenantName + "/shortUrl/" + urlCode,
      session=loginSession,
      data=None
    )
    if not checkAndParseResponse:
      return result
    self.assertEqual(result.status_code, 200, str(msg) + " - " + result.get_data(as_text=True))
    return json.loads(result.get_data(as_text=True))

class test_apiPrivate(helpers):
  def test_putShortURL(self):
    testTime = datetime.datetime.now(pytz.timezone("UTC"))
    appObj.setTestingDateTime(testTime)

    loginSession = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    resultJSON = self.putUrl(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=True
    )

    self.assertTrue(resultJSON["shortURL"].startswith(TestHelperSuperClass.env["APIAPP_REDIRECTPREFIX"] + "/"))
    self.assertEqual(len(resultJSON["shortURL"]), len(TestHelperSuperClass.env["APIAPP_REDIRECTPREFIX"]) + 1 + 5)
    self.assertEqual(len(resultJSON["id"]), 5)
    self.assertNotEqual(resultJSON[RepositoryObjBaseClass.getMetadataElementKey()]["creationDateTime"], None)

    dt = parse(resultJSON[RepositoryObjBaseClass.getMetadataElementKey()]["creationDateTime"])
    creationTime = dt.astimezone(pytz.utc)
    expectedExpireTime =  creationTime + datetime.timedelta(days=int(TestHelperSuperClass.env["APIAPP_URLEXPIREDAYS"]))
    self.assertEqual(resultJSON["expectedExpire"],expectedExpireTime.isoformat())

    reditectToUrl, result = self.getRedirectUrlUSINGPUBLICAPI(
      shortURL=resultJSON["shortURL"]
    )
    self.assertEqual(reditectToUrl, targetUrl)

    resultGetJSON = self.getUrlByCode(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      urlCode=resultJSON["id"],
      checkAndParseResponse=True
    )
    self.assertEqual(resultGetJSON, resultJSON)

  def test_userCanOnlyCreateOnTheirLoggedInDomain(self):
    loginSession = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    result = self.putUrl(
      loginSession=loginSession,
      tenantName="OtherDomain",
      url=targetUrl,
      checkAndParseResponse=False
    )
    self.assertEqual(result.status_code, 403, result.get_data(as_text=True))

  def test_userCanOnlyGetOwnRecords(self):
    loginSessionA = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    loginSessionB = LoginUtilities.getUserLoginSession("TESTTenantName", 2)
    resultJSON = self.putUrl(
      loginSession=loginSessionA,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=True
    )
    urlCode = resultJSON["id"]
    resultGet = self.getUrlByCode(
      loginSession=loginSessionB,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=False
    )
    self.assertEqual(resultGet.status_code, 403, resultGet.get_data(as_text=True))

  def test_notFoundWhenURLNotExist(self):
    loginSessionA = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    urlCode = "a-a-a"
    resultGet = self.getUrlByCode(
      loginSession=loginSessionA,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=False
    )
    self.assertEqual(resultGet.status_code, 404, resultGet.get_data(as_text=True))

  def test_putShortURLWithNoLogin_isUnAuth(self):
    testTime = datetime.datetime.now(pytz.timezone("UTC"))
    appObj.setTestingDateTime(testTime)

    result = self.putUrl(
      loginSession=None,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=False
    )
    self.assertEqual(result.status_code, 401, result.get_data(as_text=True))

  def test_getShortURLWithNoLogin_isUnAuth(self):
    loginSession = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    resultJSON = self.putUrl(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=True
    )
    urlCode = resultJSON["id"]
    resultGet = self.getUrlByCode(
      loginSession=None,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=False
    )
    self.assertEqual(resultGet.status_code, 401, resultGet.get_data(as_text=True))

  def test_deleteShortURLWithNoLogin_isUnAuth(self):
    loginSession = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    resultJSON = self.putUrl(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=True
    )
    urlCode = resultJSON["id"]
    resultDelete = self.deleteUrlByCode(
      loginSession=None,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=False
    )
    self.assertEqual(resultDelete.status_code, 401, resultDelete.get_data(as_text=True))

  def test_deleteAnotherUSersShortURL_isForbidden(self):
    loginSessionA = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    loginSessionB = LoginUtilities.getUserLoginSession("TESTTenantName", 2)
    resultJSON = self.putUrl(
      loginSession=loginSessionA,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=True
    )
    urlCode = resultJSON["id"]
    resultDelete = self.deleteUrlByCode(
      loginSession=loginSessionB,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=False
    )
    self.assertEqual(resultDelete.status_code, 403, resultDelete.get_data(as_text=True))

  def test_deleteOwnShortURL_Successful(self):
    loginSession = LoginUtilities.getUserLoginSession("TESTTenantName", 1)
    resultJSON = self.putUrl(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      url=targetUrl,
      checkAndParseResponse=True
    )
    urlCode = resultJSON["id"]
    resultDelete = self.deleteUrlByCode(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=True
    )
    resultGet = self.getUrlByCode(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      urlCode=urlCode,
      checkAndParseResponse=False
    )
    self.assertEqual(resultGet.status_code, 404, resultGet.get_data(as_text=True))

  def test_puttoSuspectDomain_failsWithError(self):
    loginSession = LoginUtilities.getUserLoginSession("TESTTenantName", 1)

    result = self.putUrl(
      loginSession=loginSession,
      tenantName="TESTTenantName",
      url=suspectTargetUrl,
      checkAndParseResponse=False
    )
    self.assertEqual(result.status_code, 403, result.get_data(as_text=True))
    resultJSON = json.loads(result.get_data(as_text=True))

    self.assertEqual(resultJSON["message"],constants.canNotLinkToDomainMessage + " Start mismatch")

  def test_putDiffTenant_failsWithError(self):
    loginSession = LoginUtilities.getUserLoginSession("TESTTenantNameXX", 1)

    result = self.putUrl(
      loginSession=loginSession,
      tenantName="TESTTenantNameXX",
      url=suspectTargetUrl,
      checkAndParseResponse=False
    )
    self.assertEqual(result.status_code, 403, result.get_data(as_text=True))
    resultJSON = json.loads(result.get_data(as_text=True))

    self.assertEqual(resultJSON["message"],constants.canNotLinkToDomainMessage + " bad tenant")

  def test_putwithnopostdata_fails(self):
    tenantName="ABC"
    loginSession = LoginUtilities.getUserLoginSession(tenantName, 1)
    result = self.assertUserPrivateAPIResult(
      methodFN=self.testClient.put,
      url="/" + tenantName + "/shortUrl",
      session=loginSession,
      data=None
    )
    self.assertEqual(result.status_code, 400)
    resultJSON = json.loads(result.get_data(as_text=True))

    self.assertEqual(resultJSON["message"],"url not in payload")

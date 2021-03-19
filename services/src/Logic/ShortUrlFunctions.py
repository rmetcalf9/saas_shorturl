from .ShortUrl import ShortUrlClass
import Store
from .Exceptions import LogicException
import datetime
from werkzeug.exceptions import Forbidden, NotFound, BadRequest
import constants
from .UrlValidator import isValidUrl

class ShortUrlFunctionClass():
  appObj = None
  shortenedUrlRepository = None
  shortUrl = None

  def __init__(self, appObj):
    self.appObj = appObj
    self.shortenedUrlRepository = Store.ShortenedUrlRepositoryClass(
      appObj=appObj
    )
    self.shortUrl = ShortUrlClass(self.shortenedUrlRepository)


  def putNewShortUrl(
    self,
    decodedJWTToken,
    storeConnection,
    content,
    tenantName
  ):
    if len(content["url"]) < 10:
      raise Forbidden(constants.canNotLinkToDomainMessage + " URL passed is less than 10 chars")
    isDestAllowed, reason = self._isDestAllowed(tenantName=tenantName, url=content["url"])
    if not isDestAllowed:
      raise Forbidden(constants.canNotLinkToDomainMessage + " " + reason)
    urlCode = self.shortUrl.getShortUrl(storeConnection=storeConnection)
    expire = self.appObj.getCurDateTime() + datetime.timedelta(days=self.appObj.APIAPP_URLEXPIREDAYS)
    shortUrlJson = {
      "id":urlCode,
      "shortURL": self.appObj.APIAPP_REDIRECTPREFIX + "/" + urlCode,
      "createdby": decodedJWTToken.getUserID(),
      "targetUrl": content["url"],
      "expectedExpire": expire.isoformat()
    }

    _, _ = self.shortenedUrlRepository.upsert(
      obj=shortUrlJson,
      objectVersion=None,
      storeConnection=storeConnection
    )

    shortenedUrlObj = self.shortenedUrlRepository.get(urlCode, storeConnection=storeConnection)

    return shortenedUrlObj.getUserDict(), 202

  def getRedirectTargetUrl(self, urlCode, storeConnection):
    if not self.shortUrl.isValidUrlCode(urlCode):
      raise LogicException("Invalid URL Code")

    shortenedUrlObj = self.shortenedUrlRepository.get(urlCode, storeConnection=storeConnection)
    if shortenedUrlObj is None:
      return None
    return shortenedUrlObj.getTargetUrl()


  def getShortUrl(
    self,
    decodedJWTToken,
    storeConnection,
    urlCode,
    andDeleteIt = False
  ):
    if not self.shortUrl.isValidUrlCode(urlCode):
      raise LogicException("Invalid URL Code")

    shortenedUrlObj = self.shortenedUrlRepository.get(urlCode, storeConnection=storeConnection)
    if shortenedUrlObj is None:
      raise NotFound()

    if shortenedUrlObj.getCreatedBy() != decodedJWTToken.getUserID():
      raise Forbidden()

    if andDeleteIt:
      # Object version checks are not important
      #  because shorturl's can never be edited
      self.shortenedUrlRepository.remove(
        id=shortenedUrlObj.getId(),
        storeConnection=storeConnection,
        objectVersion=None,
        ignoreMissingObject=True
      )

    return shortenedUrlObj.getUserDict(), 200

  def _isDestAllowed(self, tenantName, url):
    if tenantName not in self.appObj.APIAPP_DESTWHITELIST:
      return False, "bad tenant"
    if not isValidUrl(url):
      return False, "invalid url"
    for allowedStart in self.appObj.APIAPP_DESTWHITELIST[tenantName]:
      if url.startswith(allowedStart):
        return True, ""
    return False, "Start mismatch"


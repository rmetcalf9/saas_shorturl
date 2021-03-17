from object_store_abstraction import RepositoryBaseClass, RepositoryValidationException, RepositoryObjBaseClass
from .ShortenedUrlObj import factoryFn as shortenedUrlObjFactoryFn


class ShortenedUrlRepositoryClass(RepositoryBaseClass):
  objName = "ShortUrl"

  appObj = None

  def __init__(self, appObj):
    RepositoryBaseClass.__init__(self, "shorturls", shortenedUrlObjFactoryFn)
    self.appObj = appObj

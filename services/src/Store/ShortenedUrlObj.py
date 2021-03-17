from object_store_abstraction import RepositoryObjBaseClass

def factoryFn(obj, objVersion, creationDateTime, lastUpdateDateTime, objKey, repositoryObj, storeConnection):
  return ShortenedUrlObjClass(obj, objVersion, creationDateTime, lastUpdateDateTime, objKey, repositoryObj=repositoryObj, storeConnection=storeConnection)

class ShortenedUrlObjClass(RepositoryObjBaseClass):
  changed = None
  def __init__(self, obj, objVersion, creationDateTime, lastUpdateDateTime, objKey, repositoryObj, storeConnection):
    RepositoryObjBaseClass.__init__(self, obj, objVersion, creationDateTime, lastUpdateDateTime, objKey, repositoryObj)

  def getUserDict(self):
    # dict returned to user who owns this shorturl
    d = self.getDict()
    return {
      "id": d["id"],
      "shortURL": d["shortURL"],
      "expectedExpire": d["expectedExpire"],
      "targetUrl": d["targetUrl"],
      RepositoryObjBaseClass.getMetadataElementKey(): d[RepositoryObjBaseClass.getMetadataElementKey()]
    }

  def getTargetUrl(self):
    return self.getDict()["targetUrl"]

  def getCreatedBy(self):
    return self.getDict()["createdby"]

  def getId(self):
    return self.getDict()["id"]
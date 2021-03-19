from flask_restx import Resource, fields, marshal
from object_store_abstraction import RepositoryObjBaseClass

def putNewShortUrlModel(appObj):
  return appObj.flastRestPlusAPIObject.model('putNewShortUrl', {
    'url': fields.String(default=None, description='URL to point to')
  })


def putResponseNewShortUrlModel(appObj):
  return appObj.flastRestPlusAPIObject.model('putResponseNewShortUrl', {
    'id': fields.String(default='', description='Short Code for this URL'),
    'shortURL': fields.String(default='', description='Short URL for this URL'),
    'expectedExpire': fields.DateTime(dt_format=u'iso8601', description='Date url was created'),
    'targetUrl': fields.String(default='', description='Url to redirect to'),
    RepositoryObjBaseClass.getMetadataElementKey(): fields.Nested(RepositoryObjBaseClass.getMetadataModel(appObj, flaskrestplusfields=fields))
  })


def getResponseShortUrlModel(appObj):
  return appObj.flastRestPlusAPIObject.model('getResponseShortUrl', {
    'id': fields.String(default='', description='Short Code for this URL'),
    'shortURL': fields.String(default='', description='Short URL for this URL'),
    'expectedExpire': fields.DateTime(dt_format=u'iso8601', description='Date url was created'),
    'targetUrl': fields.String(default='', description='Url to redirect to'),
    RepositoryObjBaseClass.getMetadataElementKey(): fields.Nested(RepositoryObjBaseClass.getMetadataModel(appObj, flaskrestplusfields=fields))
  })
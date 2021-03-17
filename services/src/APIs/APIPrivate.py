from .Models import putNewShortUrlModel, putResponseNewShortUrlModel, getResponseShortUrlModel
from flask import request
from flask_restx import Resource, fields, marshal
from werkzeug.exceptions import BadRequest, Conflict
from object_store_abstraction import WrongObjectVersionExceptionClass, RepositoryBaseClass, RepositoryValidationException
import Logic
import constants

# This app will not worry about roles. Leaving that to the API gateway
def verifySecurityOfAPICall(appObj, request, tenantName):
  decodedJWTToken = appObj.apiSecurityCheck(
    request=request,
    tenant=tenantName,
    requiredRoleList=[ constants.DefaultHasAccountRole ],
    headersToSearch=[constants.jwtHeaderName],
    cookiesToSearch=[constants.jwtCookieName, constants.loginCookieName]
  )
  return decodedJWTToken


def requiredInPayload(content, fieldList):
  for a in fieldList:
    if a not in content:
      raise BadRequest(a + ' not in payload')
    if content[a] is None:
      raise BadRequest(a + ' not in payload')

def registerAPI(appObj, APInamespace):
  @APInamespace.route('/<string:tenantName>/shortUrl')
  class shortUrls(Resource):
    '''Private API'''

    @APInamespace.doc('Short URL')
    @APInamespace.expect(putNewShortUrlModel(appObj), validate=False)
    @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
    @appObj.flastRestPlusAPIObject.marshal_with(putResponseNewShortUrlModel(appObj), code=202, description='User details updated', skip_none=True)
    @APInamespace.response(403, 'Forbidden - User does not have required role')
    def put(self, tenantName):
      ''' Update user details  '''
      decodedJWTToken = verifySecurityOfAPICall(appObj, request, tenantName=tenantName)
      content_raw = request.get_json()
      content = marshal(content_raw, putNewShortUrlModel(appObj))

      requiredInPayload(content, ["url"])

      def dbfn(storeConnection):
        return appObj.shortUrlFunctions.putNewShortUrl(
          decodedJWTToken=decodedJWTToken,
          storeConnection=storeConnection,
          content=content,
          tenantName=tenantName
        )
      try:
        return appObj.objectStore.executeInsideTransaction(dbfn)
      except Logic.LogicException as e:
        raise BadRequest(str(e))
        #raise e
      except RepositoryValidationException as e:
        raise BadRequest(str(e))
      except WrongObjectVersionExceptionClass as err:
        raise Conflict(err)

  @APInamespace.route('/<string:tenantName>/shortUrl/<string:urlCode>')
  class shortUrl(Resource):
    '''Short URLs'''
    @APInamespace.doc('Short Urls')
    @APInamespace.marshal_with(getResponseShortUrlModel(appObj))
    @APInamespace.response(200, 'Success', model=getResponseShortUrlModel(appObj))
    @APInamespace.response(401, 'Unauthorized')
    @APInamespace.response(403, 'Forbidden')
    @appObj.addStandardSortParams(APInamespace)
    def get(self, tenantName, urlCode):
      '''Get Short URL'''
      decodedJWTToken = verifySecurityOfAPICall(appObj, request, tenantName=tenantName)

      try:
        def dbfn(storeConnection):
          return appObj.shortUrlFunctions.getShortUrl(
            decodedJWTToken=decodedJWTToken,
            storeConnection=storeConnection,
            urlCode=urlCode
          )
        return appObj.objectStore.executeInsideConnectionContext(dbfn)
      except Exception as e:
        raise e

    @APInamespace.doc('Delete Short Urls')
    @APInamespace.marshal_with(getResponseShortUrlModel(appObj))
    @APInamespace.response(200, 'Success', model=getResponseShortUrlModel(appObj))
    @APInamespace.response(401, 'Unauthorized')
    @APInamespace.response(403, 'Forbidden')
    @appObj.addStandardSortParams(APInamespace)
    def delete(self, tenantName, urlCode):
      '''Delete Short URL'''
      decodedJWTToken = verifySecurityOfAPICall(appObj, request, tenantName=tenantName)

      try:
        def dbfn(storeConnection):
          return appObj.shortUrlFunctions.getShortUrl(
            decodedJWTToken=decodedJWTToken,
            storeConnection=storeConnection,
            urlCode=urlCode,
            andDeleteIt=True
          )
        return appObj.objectStore.executeInsideTransaction(dbfn)
      except Exception as e:
        raise e
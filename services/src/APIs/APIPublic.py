#Public API is not tenant spercific
# and only privdes our redirects
from .Models import putNewShortUrlModel, putResponseNewShortUrlModel
from flask import redirect
from flask_restx import Resource, fields, marshal
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from object_store_abstraction import WrongObjectVersionExceptionClass, RepositoryBaseClass, RepositoryValidationException
import Logic
import constants


def registerAPI(appObj, APInamespace):
  @APInamespace.route('/<string:urlCode>')
  class shortUrl(Resource):

    @APInamespace.doc('Follow Redirect')
    def get(self, urlCode):
      redirectTargetUrl = None

      def dbfn(storeConnection):
        return appObj.shortUrlFunctions.getRedirectTargetUrl(urlCode, storeConnection)

      try:
        redirectTargetUrl = appObj.objectStore.executeInsideConnectionContext(dbfn)
      except Logic.LogicException as e:
        raise BadRequest(str(e))

      if redirectTargetUrl is None:
        raise NotFound()

      return redirect(redirectTargetUrl, code=301)

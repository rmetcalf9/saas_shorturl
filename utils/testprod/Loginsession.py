import requests
import json

def getLoginSessionForSaasUsermanagement(tenantName, username, password, authProviderGUID):
  #this will login using basic method

  postData =  {
    "credentialJSON": {
      "username": username,
      "password": password
    },
    "authProviderGUID": authProviderGUID
  }
  postURl = "https://api.metcarob.com/saas_user_management/v0/public/api/login/" + tenantName + "/authproviders"

  headers = {}
  headers["Content-Type"] = "application/json"
  headers["Origin"] = "https://api.metcarob.com"

  response = requests.post(
    url=postURl,
    headers=headers,
    data=json.dumps(postData)
  )
  if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    raise Exception("Login failed")

  responseJSON = json.loads(response.text)

  return LoginSession(responseJSON)

class LoginSession:
  sessionData = None
  def __init__(self, loginResponseJSON):
    self.sessionData = loginResponseJSON

  def addHeaders(self, headers):
    headers["Authorization"] = "Bearer " + self.sessionData["jwtData"]["JWTToken"]

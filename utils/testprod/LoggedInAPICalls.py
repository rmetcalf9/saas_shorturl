import requests
import json

def createUrl(loginSession, target, tenantName):
  URL = "https://api.metcarob.com/saas_shorturl/v0/private/api/user/" + tenantName + "/shortUrl"

  postData = {
    "url": target
  }

  headers = {}
  headers["Content-Type"] = "application/json"
  headers["Origin"] = "https://api.metcarob.com"
  loginSession.addHeaders(headers)

  response = requests.put(
    url=URL,
    headers=headers,
    data=json.dumps(postData)
  )
  # print("url:", URL)
  # print("postData:", postData)

  if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    raise Exception("Put URL failed")

  return json.loads(response.text)

def deleteShortUrl(shortUrl, tenantName):
  URl = "https://api.metcarob.com/saas_shorturl/v0/private/api/user/" + tenantName + "/shortUrl/" + shortUrl["id"]

  headers = {}
  headers["Content-Type"] = "application/json"
  headers["Origin"] = "https://api.metcarob.com"
  loginSession.addHeaders(headers)

  response = requests.delete(
    url=URl,
    headers=headers
  )
  if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    raise Exception("Delete URL failed")


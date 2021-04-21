import requests

def getRedirectUrl(shortUrl):
  print("xxx", shortUrl["shortURL"])

  response = requests.get(
    url=shortUrl["shortURL"],
    headers=None,
    data=None,
    allow_redirects=False
  )
  # print("url:", URL)
  # print("postData:", postData)

  if response.status_code != 301:
    print(response.status_code)
    print(response.text)
    print("FAIL FAIL FAIL - redirect failed - not excepting so we still try and delete")
    #raise Exception("Redirect failed")

  return response.headers["Location"]


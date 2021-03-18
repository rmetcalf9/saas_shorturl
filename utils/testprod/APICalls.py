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
    raise Exception("Redirect failed")

  return response.headers["Location"]


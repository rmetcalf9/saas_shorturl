# This validates realworld urls
from urllib.parse import urlparse

def isValidUrl(url):
  try:
    parsed = urlparse(url)
  except:
    return False
  #print("D", parsed)

  if parsed.scheme not in ["http", "https"]:
    return False
  if len(parsed.netloc) < 3:
    return False
  if parsed.netloc.startswith("."):
    return False
  if parsed.netloc.endswith("."):
    return False
  for c in parsed.netloc:
    if c in ["/", "?", "#", "@"]: # colan allowed
      return False
  if "//" in parsed.path:
    return False
  return True

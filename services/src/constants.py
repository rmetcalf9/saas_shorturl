
jwtHeaderName="jwt-auth-token"
jwtCookieName="jwt-auth-token"
loginCookieName="usersystemUserCredentials"

DefaultHasAccountRole="hasaccount"

canNotLinkToDomainMessage="Invalid domain for shorturl"

class customExceptionClass(Exception):
  id = None
  text = None
  def __init__(self, text, iid=None):
    if iid is None:
      self.id = text
    else:
      self.id = iid
    self.text = text


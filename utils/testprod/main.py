# Quick script to test this in prod.
import os

import Loginsession
import LoggedInAPICalls
import APICalls

print("Start")

testTarget="https://challengeswipe.com/#/challengeapp/about"
tenantName="challengeapp"

loginSession = Loginsession.getLoginSessionForSaasUsermanagement(
  tenantName=tenantName,
  username=os.environ["CHALLENGEAPPTESTACCOUNTUSERNAME"],
  password=os.environ["CHALLENGEAPPTESTACCOUNTPASSWORD"],
  authProviderGUID="1a1a101a-4df3-427a-9863-d2423e4a7561"
)

shortUrl = LoggedInAPICalls.createUrl(
  loginSession=loginSession,
  target=testTarget,
  tenantName=tenantName
)

redirectUrl = APICalls.getRedirectUrl(
  shortUrl=shortUrl
)

if redirectUrl != testTarget:
  print("FAILED, not redirecting to correct target")
else:
  print("PASSED, url redirect is correct")

LoggedInAPICalls.deleteShortUrl(
  shortUrl=shortUrl,
  tenantName = tenantName
)


print("End")


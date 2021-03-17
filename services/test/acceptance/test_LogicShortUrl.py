# Testing uniqueness requries the DB so is not a unit test
import TestHelperSuperClass
from appObj import appObj
from unittest.mock import patch
from Logic import ShortUrlClass
import Store

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def _getEnvironment(self):
    return TestHelperSuperClass.env

class test_acceptanceLogicShortUrl(helpers):
  def test_uniqueURLs(self):
    def runFn(storeConnection):
      shortenedUrlRepository = Store.ShortenedUrlRepositoryClass(appObj=appObj)
      shortUrl = ShortUrlClass(shortenedUrlRepository=shortenedUrlRepository)
      testCodes = ["11111", "11111", "11111", "11211"]

      with patch("Logic.shortCodeGenerator.getObscureURLStringFromSequence", side_effect=testCodes) as mock_gen:
        url = shortUrl.getShortUrl(storeConnection=storeConnection)
        self.assertEqual(url, "11111")

        _, _ = shortenedUrlRepository.upsert(
          obj={ "id": url },
          objectVersion=None,
          storeConnection=storeConnection
        )

        # Second call gives us another entry as there are duplicates
        url2 = shortUrl.getShortUrl(storeConnection=storeConnection)
        self.assertEqual(url2, "11211")

    appObj.objectStore.executeInsideTransaction(runFn)

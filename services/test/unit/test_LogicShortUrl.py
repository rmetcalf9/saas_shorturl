import unittest
from Logic import ShortUrlClass, CODELENGTH
from unittest.mock import patch, MagicMock
from appObj import appObj
import Store

class testLogicShortUrl(unittest.TestCase):

  def test_normal(self):
    shortUrl = ShortUrlClass(shortenedUrlRepository=Store.ShortenedUrlRepositoryClass(appObj=appObj))
    mm = MagicMock()
    mm.getObjectJSON.return_value = None, None, None, None, None
    url = shortUrl.getShortUrl(storeConnection=mm)
    self.assertEqual(len(url), CODELENGTH)

  def test_badwordWillNotBeGenerated(self):
    shortUrl = ShortUrlClass(shortenedUrlRepository=Store.ShortenedUrlRepositoryClass(appObj=appObj))

    testCodes = ["fuck5", "sH1it", "shit5", "sh1t5", "5h1t4", "12ok5"]

    with patch("Logic.shortCodeGenerator.getObscureURLStringFromSequence", side_effect=testCodes) as mock_gen:
      mm = MagicMock()
      mm.getObjectJSON.return_value=None, None, None, None, None
      url = shortUrl.getShortUrl(storeConnection=mm)
      self.assertEqual(url, "12ok5")
    self.assertEqual(len(url), CODELENGTH)

  def test_partialBadWordNotRejected(self):
    shortUrl = ShortUrlClass(shortenedUrlRepository=Store.ShortenedUrlRepositoryClass(appObj=appObj))

    testCodes = ["12fuc"]

    with patch("Logic.shortCodeGenerator.getObscureURLStringFromSequence", side_effect=testCodes) as mock_gen:
      mm = MagicMock()
      mm.getObjectJSON.return_value=None, None, None, None, None
      url = shortUrl.getShortUrl(storeConnection=mm)
      self.assertEqual(url, "12fuc")
    self.assertEqual(len(url), CODELENGTH)


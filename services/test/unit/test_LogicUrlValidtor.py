import unittest
from Logic import isValidUrl

workingURLsToTest = [
  "http://random.com",
  "https://random.com",
  "http://random.com:80",
  "https://random.com:80",
  "http://random.com:80/",
  "https://random.com:80/",
  "http://random.com:80/1/2/3",
  "https://random.com:80/1/2/3?a=b&c=d&e=f"
]
failingURLsToTest = [
  "",
  "http://",
  "https://",
  "https://.",
  "https://.a",
  "https://a.",
  "https://a.?",
  "https://a.ahttps://a.v.c",
  "https://a.a//a/v/c//cs"
  "https://a.a//a/v/c//cs?a=b&c=d"
]

class testLogicUrlValidator(unittest.TestCase):

  def test_working(self):
    for url in workingURLsToTest:
      self.assertTrue(isValidUrl(url), msg=url + " should be valid")

  def test_broken(self):
    for url in failingURLsToTest:
      self.assertFalse(isValidUrl(url), msg=url + " should not be valid")

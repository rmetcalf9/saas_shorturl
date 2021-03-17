import TestHelperSuperClass
import json

class helpers(TestHelperSuperClass.simpleTests):
  pass


class test_apiPrivate(helpers):
  def test_urlCodeTooShort(self):
    reditectToUrl, result = self.getRedirectUrlUSINGPUBLICAPI(
      shortURL="",
      shortCodeOverride="aa",
      checkAndParseResponse=False
    )
    apiResultJSON = json.loads(result.get_data(as_text=True))

    self.assertEqual(result.status_code, 400)
    self.assertEqual(apiResultJSON["message"], "Invalid URL Code")

  def test_urlCodeTooLong(self):
    reditectToUrl, result = self.getRedirectUrlUSINGPUBLICAPI(
      shortURL="",
      shortCodeOverride="aegddsddfdfda",
      checkAndParseResponse=False
    )
    apiResultJSON = json.loads(result.get_data(as_text=True))

    self.assertEqual(result.status_code, 400)
    self.assertEqual(apiResultJSON["message"], "Invalid URL Code")

  def test_urlCodeInvalidChar(self):
    reditectToUrl, result = self.getRedirectUrlUSINGPUBLICAPI(
      shortURL="",
      shortCodeOverride="aa%tt",
      checkAndParseResponse=False
    )
    apiResultJSON = json.loads(result.get_data(as_text=True))

    self.assertEqual(result.status_code, 400)
    self.assertEqual(apiResultJSON["message"], "Invalid URL Code")


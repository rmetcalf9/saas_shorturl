import unittest
from Logic import shortCodeGenerator, MAXSOURCEINT, OutOfRangeException, InvalidOneTimePadException

class testLogicShortCodeGenerator(unittest.TestCase):
  ## ********************************
  ##  Tests for ontimepad
  ## ********************************

  def test_simplepad_rangeworks(self):
    for source in list(range(0,1000)) + list(range(MAXSOURCEINT-1000,MAXSOURCEINT)):
      target =  shortCodeGenerator._getTargetNumber(source=source)
      self.assertEqual(source, shortCodeGenerator._getSequenceSourceNumber(target=target))

  def test_sourceMustNotBeNegative(self):
    self.assertRaises(OutOfRangeException, shortCodeGenerator._getTargetNumber, -1)

  def test_sourceMustNotGreaterThanMax(self):
    self.assertRaises(OutOfRangeException, shortCodeGenerator._getTargetNumber, MAXSOURCEINT)

  ## ********************************
  ##  Tests for urlString Sequence
  ## ********************************

  def test_urlstring_rangeallworks(self):
    for source in list(range(0,1000)) + list(range(MAXSOURCEINT-1000,MAXSOURCEINT)):
      urlString =  shortCodeGenerator._getURLStringFromSequence(sequence=source)
      self.assertEqual(len(urlString), 5)
      self.assertEqual(source, shortCodeGenerator._getSequenceFromURLSring(URLString=urlString))

  ## ********************************
  ##  Tests putting it all together
  ## ********************************

  def test_fullencoding_rangeallworks(self):
    #for source in list(range(0,10)):
    for source in list(range(0,1000)) + list(range(MAXSOURCEINT-1000,MAXSOURCEINT)):
      urlString =  shortCodeGenerator.getObscureURLStringFromSequence(sequence=source)
      self.assertEqual(len(urlString), 5)
      self.assertEqual(source, shortCodeGenerator.getSequenceFromObscureURLSring(URLString=urlString))

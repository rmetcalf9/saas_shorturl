
# Source number is a increment sequence number 1, 2, 3, 4...
# Target number is an integer that is mapped to 4565, 2346, 5434, 2344...

# I want to represent url's as 5 charactors in the set [A-Za-z0-9_.-~] = 56 chars
lowerCaseLetters = "abcdefghijklmnopqrstuvwxyz"
upperCaseLetters = lowerCaseLetters.upper()
numbers = "0123456789"
specialchars = "_.-~"

charsToUseInURL = lowerCaseLetters + upperCaseLetters + numbers + specialchars

# 5 chars = 66 * 66 * 66 * 66 * 66 = 1252332576 possible combinations
# so source and target numbers must be in the range 0-1252332575

# 2^30 = 1073741824 so if I reduce the range to 1073741824 then I will
#  always be able to fit the result in 5 chars (I will waste some combinations)
MAXSOURCEINT = 2 ** 30

# I will apply a onetimepad to each number. This just means that the mapping is a bit jumbled up but will not break
#  the sequence in the results because the same one time pad is used mutiple times. To generate the pad:
##from random import randrange
##randrange(MAXSOURCEINT)
PAD = 315521835

# The system will use a secret 29 bit one time pad

# Don't change this without going through all the logic above
CODELENGTH = 5

class OutOfRangeException(Exception):
  pass
class InvalidOneTimePadException(Exception):
  pass

class ShortCodeGenerator():
  def _getTargetNumber(self, source):
    if source < 0:
      raise OutOfRangeException("Source less than 0")
    if source >= MAXSOURCEINT:
      raise OutOfRangeException("Source greater than max")
    return PAD ^ source

  def _getSequenceSourceNumber(self, target):
    return PAD ^ target

  def _getURLStringFromSequence(self, sequence):
    retVal = ""
    for _ in range(0,CODELENGTH):
      remainder = int(sequence % len(charsToUseInURL))
      retVal += charsToUseInURL[remainder]
      sequence -= remainder
      sequence = sequence / len(charsToUseInURL)

    return retVal[::-1]

  def _getSequenceFromURLSring(self, URLString):
    retVal = 0
    for x in range(0,CODELENGTH):
      retVal *= len(charsToUseInURL)
      retVal += charsToUseInURL.index(URLString[x])

    return retVal

  def getObscureURLStringFromSequence(self, sequence):
    return self._getURLStringFromSequence(self._getTargetNumber(source=sequence))

  def getSequenceFromObscureURLSring(self, URLString):
    return self._getSequenceSourceNumber(target=self._getSequenceFromURLSring(URLString))

  def isValidUrlCode(self, urlCode):
    if len(urlCode) != CODELENGTH:
      return False
    for char in urlCode:
      if char not in charsToUseInURL:
        return False
    return True

shortCodeGenerator = ShortCodeGenerator()

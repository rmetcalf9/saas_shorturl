from random import randrange
from .ShortCodeGenerator import MAXSOURCEINT, shortCodeGenerator

# All words here must be lowercase and list. 5 chars or less
#badWords = ['bitch', 'cock', 'crap', 'cunt', 'dick', 'fuck', 'gash', 'knob', 'penis', 'prick', 'pussy', 'sex', 'shag', 'shit', 'tits']
badWords = ['fuck', 'shit']

# must be lowercase
leetMap = {
  "1": ["i", "l"],
  "3": ["e"],
  "5": ["s"],
  "8": ["b"],
  "0": ["o"]
}

class ShortUrlClass():
  shortenedUrlRepository = None

  def __init__(self, shortenedUrlRepository):
    self.shortenedUrlRepository = shortenedUrlRepository

  def getShortUrl(self, storeConnection):
    foundGood = False

    urlStr = ""
    while not foundGood:
      num = randrange(MAXSOURCEINT)
      urlStr = shortCodeGenerator.getObscureURLStringFromSequence(num)
      if self._isUrlStrSafe(urlStr):
        if self._isUrlStrUnique(urlStr=urlStr, storeConnection=storeConnection):
          foundGood = True

    return urlStr

  def isValidUrlCode(self, urlCode):
    return shortCodeGenerator.isValidUrlCode(urlCode)

  def _charequalleet(self, possibleleet, alpha):
    if possibleleet == alpha:
      return True
    if possibleleet not in leetMap:
      return False
    for possibleleetreplacement in leetMap[possibleleet]:
      if possibleleetreplacement == alpha:
        return True
    return False

  def _urlContains(self, urlStr, badWord):
    badWordCharSearchingFor = 0
    for curUrlStrChar in urlStr:
      if self._charequalleet(possibleleet=curUrlStrChar, alpha=badWord[badWordCharSearchingFor]):
        badWordCharSearchingFor += 1
        if len(badWord) == badWordCharSearchingFor:
          return True

    return False

  def _isUrlStrSafe(self, urlStr):
    for badword in badWords:
      if self._urlContains(urlStr.lower(), badword):
        return False
    return True

  def _isUrlStrUnique(self, urlStr, storeConnection):
    urlObj = self.shortenedUrlRepository.get(urlStr, storeConnection=storeConnection)
    return urlObj == None

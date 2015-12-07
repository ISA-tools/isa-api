__author__ = 'alfie'

import string

class CommonFunctions():
    def makeLowercaseFirstChar(self, s):
        if len(s) == 0:
            return s
        else:
            return s[0].lower() + s[1:]

    def makeUppercaseFirstCharInStringArray(self, s):
        myStr = ""
        for i in s.split(' '):
            if len(i) == 0:
                myStr = myStr + i
            else:
                myStr = myStr + i[0].upper() + i[1:]
        return myStr

    def makeAttributeName(self, tag):
        table = ''.maketrans('', '')
        stripTag = tag.translate(dict.fromkeys(' ', table))
        if (len(stripTag.split(' ',1)) > 1):
            return self.makeLowercaseFirstChar(stripTag.split(' ',1)[0]) + self.makeUppercaseFirstCharInStringArray(stripTag.split(' ',1)[1])
        else:
            return self.makeLowercaseFirstChar(stripTag.split(' ',1)[0])
# coding: utf-8
__author__ = 'alfie'

import string

class CommonFunctions():
    def makeLowercaseFirstChar(self, s):
        if not s:
            return s
        else:
            return s[0].lower() + s[1:]

    def makeUppercaseFirstCharInStringArray(self, s):
        myStr = ""
        for i in s.split(' '):
            if i:
                myStr = ''.join([myStr, i[0].upper(), i[1:]])
        return myStr

    def makeAttributeName(self, tag):
        table = ''.maketrans('', '')
        stripTag = tag.translate(dict.fromkeys(' ', table))
        stripped_tag = stripTag.split(' ',1)
        if len(stripped_tag) > 1:
            return self.makeLowercaseFirstChar(stripped_tag[0]) + self.makeUppercaseFirstCharInStringArray(stripped_tag[1])
        else:
            return self.makeLowercaseFirstChar(stripped_tag[0])

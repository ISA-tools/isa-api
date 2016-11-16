# coding: utf-8
__author__ = 'alfie'
__author__ = 'althonos'

import string

class CommonFunctions(object):

    @staticmethod
    def makeLowercaseFirstChar(s):
        if not s:
            return s
        else:
            return ''.join([s[0].lower(), s[1:]])

    @staticmethod
    def makeUppercaseFirstCharInStringArray(s):
        myStr = ""
        for i in s.split(' '):
            if i:
                myStr = ''.join([myStr, i[0].upper(), i[1:]])
        return myStr

    @staticmethod
    def makeAttributeName(tag):
        #table = ''.maketrans('', '')
        #stripTag = tag.translate(dict.fromkeys(' ', table))
        stripped_tag = stripTag.split(' ',1)
        if len(stripped_tag) > 1:
            return "".join([CommonFunctions.makeLowercaseFirstChar(stripped_tag[0]), CommonFunctions.makeUppercaseFirstCharInStringArray(stripped_tag[1])])
        else:
            return CommonFunctions.makeLowercaseFirstChar(stripped_tag[0])

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


    def makeAttributeName(self, tag, toBeRemovedTag):
        tag = tag.replace(toBeRemovedTag, '')
        if 'term accession' in tag.lower():
            tag = 'Term Accession'
        if 'term source' in tag.lower():
            tag = 'Term Source'
        if 'pubmed id' in tag.lower():
            tag = 'PubMed ID'
        if 'doi' in tag.lower():
            tag = 'doi'
        if 'uri' in tag.lower():
            tag = 'uri'
        table = string.maketrans("","")
        stripTag = tag.translate(table, string.punctuation)
        stripTag = stripTag.lstrip(' ')
        if (len(stripTag.split(' ',1)) > 1):
            return self.makeLowercaseFirstChar(stripTag.split(' ',1)[0]) + self.makeUppercaseFirstCharInStringArray(stripTag.split(' ',1)[1])
        else:
            return self.makeLowercaseFirstChar(stripTag.split(' ',1)[0])


    def strToBool(self, str):
        if (str == "true"):
            return True
        else:
            return False

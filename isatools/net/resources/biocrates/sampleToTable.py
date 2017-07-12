import sys, os
from bs4 import BeautifulSoup as Soup
from collections import defaultdict

__author__ = 'alfie'


def generatePolarityAttrsDict(plate, polarity, myAttrs, myMetabolites, mydict):
    usedop = plate.get('usedop')
    platebarcode = plate.get('platebarcode')
    injection = plate.find_all('injection', {'polarity': polarity})
    if len(injection) > 0:
        for pi in injection:
            myAttrList = []
            myMetabolitesList = []
            for p in pi.find_all('measure'):
                myrdfname = p.find_parent('injection').get('rawdatafilename').split('.')[0]
                for attr, value in p.attrs.iteritems():
                    if attr != 'metabolite':
                        mydict[p.get('metabolite') + '-' + myrdfname + '-' + attr + '-' + polarity.lower() + '-' + usedop + '-' + platebarcode] = value
                        if attr not in myAttrList:
                            myAttrList.append(attr)
                myMblite = p.get('metabolite')
                if myMblite not in myMetabolitesList:
                    myMetabolitesList.append(myMblite)
            # it is assume that the rawdatafilename is unique in each of the plate grouping and polarity
            myAttrs[pi.get('rawdatafilename').split('.')[0]] = myAttrList
        myMetabolites[usedop + '-' + platebarcode + '-' + polarity.lower()] = myMetabolitesList
    return (myAttrs, mydict)


def generateAttrsDict(plate):
    # using dictionaries of lists
    posAttrs = defaultdict(list)
    negAttrs = defaultdict(list)
    posMetabolites = defaultdict(list)
    negMetabolites = defaultdict(list)
    mydict = {}
    posAttrs, mydict = generatePolarityAttrsDict(plate, 'POSITIVE', posAttrs, posMetabolites, mydict)
    negAttrs, mydict = generatePolarityAttrsDict(plate, 'NEGATIVE', negAttrs, negMetabolites, mydict)
    return (posAttrs, negAttrs, posMetabolites, negMetabolites, mydict)


def writeOutToFile(plate, polarity, usedop, platebarcode, output_dir, uniqueAttrs, uniqueMetaboliteIdentifiers, mydict):
    pos_injection = plate.find_all('injection', {'polarity': polarity})
    if (len(pos_injection) > 0):
        filename = usedop + '-' + platebarcode + '-' + polarity.lower() + '-maf.txt'
        print(filename)
        with open(os.path.join(output_dir, filename), 'w') as file_handler:
            # writing out the header
            file_handler.write('Sample ID')
            for ua in uniqueAttrs:
                for myattr in uniqueAttrs[ua]:
                    file_handler.write('\t' + ua + '[' + myattr + ']')
            # now the rest of the rows
            for myMetabolite in uniqueMetaboliteIdentifiers[usedop + '-' + platebarcode + '-' + polarity.lower()]:
                file_handler.write('\n' + myMetabolite)
                for ua in uniqueAttrs:
                    for myattr in uniqueAttrs[ua]:
                        mykey = myMetabolite + '-' + ua + '-' + myattr + '-' + polarity.lower() + '-' + usedop + '-' + platebarcode
                        if mykey in mydict:
                            file_handler.write('\t' + mydict[mykey])
                        else:
                            file_handler.write('\t')
        file_handler.close()


def parseSample(file):
    folder_name = 'output'
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder_name)

    # create the output directory if it does not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file = sys.argv[1]
    # open and read up the file
    handler = open(file).read()
    soup = Soup(handler)

    # get all the plates
    plates = soup.find_all('plate')
    for plate in plates:
        usedop = plate.get('usedop')
        platebarcode = plate.get('platebarcode')
        # extracting the the distinct column labels, metabolites, and rawdatafilename
        # collect the data into a dictionary
        posAttrs, negAttrs, posMetabolites, negMetabolites, mydict = generateAttrsDict(plate)
        # and start creating the sample tab files
        writeOutToFile(plate, 'POSITIVE', usedop, platebarcode, output_dir, posAttrs, posMetabolites, mydict)
        writeOutToFile(plate, 'NEGATIVE', usedop, platebarcode, output_dir, negAttrs, negMetabolites, mydict)


if __name__ == "__main__":
    parseSample(sys.argv[1])

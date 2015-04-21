#!/usr/bin/env python

import os
import re
import types
import math

os.system('printf "\033c"')


class self:
    f = open("file.gb", "r")
    alllines = f.readlines()
    sequence = [None]
    genes = []

    def getSequence(self):
        # print type(self.alllines)
        #print len(self.alllines)
        for i in range(len(self.alllines)):
            line = self.alllines[i].strip()
            self.alllines[i] = line
            if line == "ORIGIN":  # after this, get the sequence
                #print i
                break
            i += 1

        for k in range(i + 1, len(self.alllines)):
            self.alllines[k].strip()  # delete blank space, before and after
            self.alllines[k].replace(' ', '')  # delete blank space in characters
            for j in range(len(self.alllines[k])):
                if self.alllines[k][j].isalpha():  # delete numbers in sequence
                    self.sequence.append(self.alllines[k][j])
                #print len(self.sequence)
                #print type(self.sequence)
                #print self.sequence[0:60]

    def getGenes(self):
        countCDS = 0
        countGene = 0
        for i in range(40, len(self.alllines)):
            match = re.match(r'^gene', self.alllines[i])
            if match:
                # find the position, sequence start and end point
                position = re.findall(r'(\d+)\.\.(\d+)', self.alllines[i])
                # judge 'complement'
                hasComplement = False
                isComplement = re.search(r'complement', self.alllines[i])
                if isComplement:
                    hasComplement = True  # 'complement' exists
                if len(position) == 0:
                    continue
                    # countGene -= 1
                #break
                start = position[0][0]
                end = position[0][1]
                # print start, end
                # get geneName
                if 'gene' in self.alllines[i + 1]:
                    geneName = re.findall(r'"(.+)"', self.alllines[i + 1])[0]
                    # if exists '/gene', then judge whether '/locus_tag' exists or not
                    if 'locus_tag' in self.alllines[i + 2]:
                        tagName = re.findall(r'"(.+)"', self.alllines[i + 2])[0]
                    else:  # exist '/gene', but not exist '/locus_tag', then tagName must be None
                        tagName = None
                else:
                    geneName = None  # not exist '/gene'
                    if 'locus_tag' in self.alllines[i + 1]:
                        tagName = re.findall(r'"(.+)"', self.alllines[i + 1])[0]
                    else:
                        tagName = None  # '/gene' & '/locus_tag' not exist
                tmpDict = {'start': int(start), 'end': int(end) + 1, 'geneName': geneName, 'tagName': tagName,
                           'complement': hasComplement}
                self.genes.append(tmpDict)
                # print len(self.genes)
            #print "CDS: ", countCDS, "gene: ", countGene


def handleComplement(primarySeq):
    i = 0
    handledSeq = ''
    translate = {'a': 't', 't': 'a', 'c': 'g', 'g': 'c'}
    while i < len(primarySeq):
        handledSeq += translate[primarySeq[i]]  # complement sequence
        i += 1
    return handledSeq


def inputLengthDistance():
    while True:
        length = raw_input("please input the length of extracted segment \ninput: ")
        try:
            length = float(length)
        except:
            print '\033[2;31m' + 'input length error!! please input again' + '\033[1;m'
            continue
        else:
            break
    while True:
        distance = raw_input(
            "please input the distance between midpoint of extracted segment and starting point \ninput: ")
        try:
            distance = int(distance)
        except:
            print '\033[2;31m' + 'input distance error!! please input again' + '\033[1;m'
            continue
        else:
            break
    return length, distance


def extractSeq(i, name, outFile, length, distance):  # , iscomplement):
    if HandleSequence.genes[i]['complement'] == True:
        # formular: start: s + d - l/2(ceil) +1
        start = HandleSequence.genes[i]['end'] + distance - int(math.ceil(float(length) / 2.0))  # + 1
        # formular: end: s + d + l/2(ceil)
        end = HandleSequence.genes[i]['end'] + distance + int(math.ceil(float(length) / 2.0))
    else:
        # formular: start: s + d - l/2(ceil) +1
        start = HandleSequence.genes[i]['start'] + distance - int(math.ceil(float(length) / 2.0))  # + 1
        # formular: end: s + d + l/2(ceil)
        end = HandleSequence.genes[i]['start'] + distance + int(math.ceil(float(length) / 2.0))
    tmpSequence = ''.join(HandleSequence.sequence[start:end])  # translate list to str!!

    #if iscomplement:
    # if iscomplement is True, then handle complement sign
    if HandleSequence.genes[i]['complement'] == True:
        tmpSequence = handleComplement(tmpSequence)
        tmpSequence = tmpSequence[::-1]
    outFile.write(">" + name + '\n')
    outFile.write(tmpSequence + '\n\n')
    print ">" + name
    print tmpSequence + '\n'


def handleGeneTag(nameJudge, outFile):
    length, distanceOrigin = inputLengthDistance()
    while True:
        i = 0
        if nameJudge == 'gene':  # using gene name to search
            name = raw_input("please input gene names(if input exit to exit) \ninput: ")
            name.strip()
            if name == 'exit':
                break
            # judge whether geneName exists or not
            while i < len(HandleSequence.genes):
                if name == HandleSequence.genes[i]['geneName']:
                    if HandleSequence.genes[i]['complement'] == True:
                        print '\n' + name + ' has "complement" sign!!'
                        distance = -distanceOrigin
                        # print 'distance: ', distance
                        choice = -1
                        while True:
                            try:
                                originExtracted = raw_input("""
please input:
  1.origin sequence
  2.reverse complement sequence
input: """)
                                #print "originExtracted: ", originExtracted
                                choice = int(originExtracted)
                                #print 'choice: ', choice
                                if choice != 1 and choice != 2:
                                    print '\033[2;31m' + 'input error!! input again!!' + '\033[1;m'
                                    continue
                                else:
                                    break
                            except:
                                print '\033[2;31m' + 'input error!! input again!!' + '\033[1;m'
                                continue
                            else:
                                break
                        if choice == 1:
                            extractSeq(i, name, outFile, length, distance)  #, False)
                        else:
                            extractSeq(i, name, outFile, length, distance)  #, True)
                    else:
                        distance = distanceOrigin
                        extractSeq(i, name, outFile, length, distance)  # , False)
                    break
                i += 1
            else:
                print '\033[2;31m'
                print "gene " + name + " not exists!"
                print '\033[1;m'
                continue
        else:  # using tag name to search
            name = raw_input("please input tag names(input exit to exit) \ninput: ")
            name.strip()
            if name == 'exit':
                break
            # judge whether tagName exists or not
            while i < len(HandleSequence.genes):
                if name == HandleSequence.genes[i]['tagName']:
                    if HandleSequence.genes[i]['complement'] == True:
                        print '\n' + name + ' has "complement" sign!!'
                        distance = -distanceOrigin
                        choice = -1
                        while True:
                            try:
                                originExtracted = raw_input("""
please input:
  1.origin sequence
  2.reverse complement sequence
input: """)
                                choice = int(originExtracted)
                                if choice != 1 and choice != 2:
                                    print '\033[2;31m' + 'input error!! input again!!' + '\033[1;m'
                                    continue
                                else:
                                    break
                            except:
                                print '\033[2;31m' + 'input error!! input again!!' + '\033[1;m'
                                continue
                            else:
                                break
                        if choice == 1:
                            extractSeq(i, name, outFile, length, distance)  # , False)
                        else:
                            extractSeq(i, name, outFile, length, distance)  # , True)
                    else:
                        distance = distanceOrigin
                        extractSeq(i, name, outFile, length, distance)  # , False)
                    break
                i += 1
            else:
                print '\033[2;31m' + "tag " + name + " not exists!" + '\033[1;m'
                continue


if __name__ == "__main__":
    outFileName = raw_input('please input filename to save the result \ninput: ')
    outFileName.strip()  # delete the blank space before and after
    # if os.path.exists(outFileName):
    #print 'the filename has exists!'
    #outFile = open(outFileName, 'a+') # finally use this
    outFile = open(outFileName, 'w')  # just using this test
    handle = HandleSequence()
    handle.getSequence()
    handle.getGenes()
    while True:
        inputType = raw_input("""
please choose input type:
  1.gene names
  2.tag names
  3.all genes
  4.all tags
  5.exit
If you input 1 or 2, you will need to input gene names or tages
input: """)
        try:
            inputType = int(inputType)
        except:
            print '\033[2;31m' + '\nyou input type error!! input again' + '\033[1;m'
            continue
        if inputType == 5:
            outFile.close()
            break
        if inputType > 5 or inputType < 1:
            print '\033[2;31m' + "\ninput number error!! input again!!" + '\033[1;m'
            continue
        if inputType == 1:
            handleGeneTag('gene', outFile)

        if inputType == 2:
            handleGeneTag('tag', outFile)

        # output all genes
        if inputType == 3:
            i = 0
            length, distanceOrigin = inputLengthDistance()
            while i < len(HandleSequence.genes):
                if type(HandleSequence.genes[i]['geneName']) != types.NoneType:
                    if HandleSequence.genes[i]['complement'] == True:
                        distance = -distanceOrigin
                        extractSeq(i, HandleSequence.genes[i]['geneName'], outFile, length, distance)  #, True)
                    else:
                        distance = distanceOrigin
                        extractSeq(i, HandleSequence.genes[i]['geneName'], outFile, length, distance)  #), False)
                i += 1

        # output all tags
        if inputType == 4:
            i = 0
            length, distanceOrigin = inputLengthDistance()
            while i < len(HandleSequence.genes):
                if type(HandleSequence.genes[i]['tagName']) != types.NoneType:
                    if HandleSequence.genes[i]['complement'] == True:
                        distance = -distanceOrigin
                        extractSeq(i, HandleSequence.genes[i]['tagName'], outFile, length, distance)  #, True)
                    else:
                        distance = distanceOrigin
                        extractSeq(i, HandleSequence.genes[i]['tagName'], outFile, length, distance)  #, False)
                i += 1

#!/usr/bin/env python

import os
import re
import types
import math

os.system('printf "\033c"')

class HandleSequence:
	f = open("file.gb", "r")
	alllines = f.readlines()
	sequence = [None] 
	genes = []

	def getSequence(self):
		#print type(HandleSequence.alllines)
		#print len(HandleSequence.alllines)
		for i in range(len(HandleSequence.alllines)):
			line = HandleSequence.alllines[i].strip()
			HandleSequence.alllines[i] = line
			if line == "ORIGIN": # after this, get the sequence
				#print i
				break
			i += 1

		for k in range(i+1, len(HandleSequence.alllines)):
			HandleSequence.alllines[k].strip() # delete blank space, before and after
			HandleSequence.alllines[k].replace(' ', '') # delete blank space in characters
			for j in range(len(HandleSequence.alllines[k])):
				if HandleSequence.alllines[k][j].isalpha(): # delete numbers in sequence 
					HandleSequence.sequence.append(HandleSequence.alllines[k][j])
		#print len(HandleSequence.sequence)
		#print type(HandleSequence.sequence)
		#print HandleSequence.sequence[0:60]

	def getGenes(self):
		countCDS = 0
		countGene = 0
		for i in range(40, len(HandleSequence.alllines)):
			match = re.match(r'^gene', HandleSequence.alllines[i])
			#matchCDS = re.match(r'^CDS', HandleSequence.alllines[i])

			#if type(match) != types.NoneType:
			#	print HandleSequence.alllines[i]
			#	countGene += 1
			#if type(matchCDS) != types.NoneType:
			#	print HandleSequence.alllines[i]
			#	countCDS += 1
			#	raw_input()

			if match:
				# find the position, sequence start and end point
				position = re.findall(r'(\d+)\.\.(\d+)', HandleSequence.alllines[i])
				# judge 'complement' 
				hasComplement = False
				isComplement = re.search(r'complement', HandleSequence.alllines[i])
				if isComplement:
					hasComplement = True # 'complement' exists
				if len(position) == 0:
					continue
					#countGene -= 1
					#break
				start = position[0][0]
				end = position[0][1]
				#print start, end
				# get geneName
				if 'gene' in HandleSequence.alllines[i+1]:
					geneName = re.findall(r'"(.+)"', HandleSequence.alllines[i+1])[0]
					# if exists '/gene', then judge whether '/locus_tag' exists or not 
					if 'locus_tag' in HandleSequence.alllines[i+2]:
						tagName = re.findall(r'"(.+)"', HandleSequence.alllines[i+2])[0]
					else: # exist '/gene', but not exist '/locus_tag', then tagName must be None
						tagName = None
				else:
					geneName = None # not exist '/gene'
					if 'locus_tag' in HandleSequence.alllines[i+1]:
						tagName = re.findall(r'"(.+)"', HandleSequence.alllines[i+1])[0]
					else:
						tagName = None # '/gene' & '/locus_tag' not exist
				tmpDict = { 'start':int(start), 'end':int(end) + 1, 'geneName':geneName, 'tagName':tagName, 'complement': hasComplement }
				HandleSequence.genes.append(tmpDict)
		#print len(HandleSequence.genes)
		#print "CDS: ", countCDS, "gene: ", countGene

def handleComplement(primarySeq):
	i = 0
	handledSeq = ''
	translate = { 'a':'t', 't':'a', 'c':'g', 'g':'c' }
	while i < len(primarySeq):
		handledSeq += translate[primarySeq[i]]
		i += 1
	return handledSeq

def extractSeq(i, name, outFile):
	while True:
		length = raw_input("please input the length of extracted segment \ninput: ")
		try:
			length = float(length)
		except:
			print 'input length error!! please input again'
			continue
		else:
			break
	while True:
		positionD = raw_input("please input the distance between midpoint of extracted segment and starting point \ninput: ")
		try:
			positionD = int(positionD)
		except:
			print 'input distance error!! please input again'
			continue
		else:
			break
	# formular: start: s + d - l/2(ceil) +1
	start = HandleSequence.genes[i]['start'] + positionD - int(math.ceil(float(length)/2.0)) + 1 				
	# formular: end: s + d + l/2(ceil) 
	end = HandleSequence.genes[i]['start'] + positionD + int(math.ceil(float(length)/2.0))
	tmpSequence = ''.join(HandleSequence.sequence[start:end]) # translate list to str!!
	if HandleSequence.genes[i]['complement']:
		tmpSequence = handleComplement(tmpSequence)
		#print type(tmpSequence)
	outFile.write(">" + name + '\n')
	outFile.write(tmpSequence + '\n\n')
	print ">" + name
	print tmpSequence + '\n'
		

def handleGeneTag(nameJudge, outFile):
	while True:
		i = 0
		if nameJudge == 'gene': # using gene name to search
			name = raw_input("please input gene names(if input exit to exit) \ninput: ")
			name.strip()
			if name == 'exit':
				break
			hasGene = False
			# judge whether geneName exists or not
			while i < len(HandleSequence.genes):
				if name == HandleSequence.genes[i]['geneName']:
					hasGene = True
					if HandleSequence.genes[i]['complement'] == True:
						print name + ' has "complement" sign!!'
					break
				i += 1
			else:
				print "gene " + name + " not exists!"
				continue
		else: # using tag name to search
			name = raw_input("please input tag names(input exit to exit) \ninput: ")
			name.strip()
			if name == 'exit':
				break
			hasTag = False
			# judge whether tagName exists or not
			while i < len(HandleSequence.genes):
				if name == HandleSequence.genes[i]['tagName']:
					hasTag = True
					break
				i += 1
			else:
				print "tag " + name + " not exists!"
				continue
		extractSeq(i, name, outFile)

if __name__ == "__main__":
	outFileName = raw_input('please input filename to save the result \ninput: ')
	outFileName.strip() # delete the blank space before and after
	#if os.path.exists(outFileName):
		#print 'the filename has exists!'
	#outFile = open(outFileName, 'a+') # finally use this
	outFile = open(outFileName, 'w') # just using this test
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
		inputType = int(inputType)
		if inputType == 5:
			outFile.close()
			break
		if inputType > 5 or inputType <1:
			print "input number error!!"
			continue
		if inputType == 1:
			handleGeneTag('gene', outFile)
			
		if inputType == 2:
			handleGeneTag('tag', outFile)
			
		# output all genes
		if inputType == 3:
			i = 0
			while i < len(HandleSequence.genes):
				if type(HandleSequence.genes[i]['geneName']) != types.NoneType:
					extractSeq(i, HandleSequence.genes[i]['geneName'], outFile)
					#tmpName = ">" + HandleSequence.genes[i]['geneName']
					#tmpSequence = ''.join(HandleSequence.sequence[HandleSequence.genes[i]['start']:HandleSequence.genes[i]['end']])
					#outFile.write(tmpName +'\n')
					#outFile.write(tmpSequence + '\n\n')
					#print ">" + tmpName
					#print tmpSequence + '\n'
				i += 1

		# output all tags
		if inputType == 4:
			i = 0
			while i < len(HandleSequence.genes):
				if type(HandleSequence.genes[i]['tagName']) != types.NoneType:
					extracSeq(i, HandleSequence.genes[i]['tagName'], outFile)
					#tmpName = ">" +  HandleSequence.genes[i]['tagName']
					#tmpSequence = ''.join(HandleSequence.sequence[HandleSequence.genes[i]['start']: HandleSequence.genes[i]['end']])
					#outFile.write(tmpName + '\n')
					#outFile.write(tmpSequence + '\n\n')
					#print tmpName
					#print tmpSequence + '\n'
				i += 1

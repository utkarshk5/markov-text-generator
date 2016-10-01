#!/usr/bin/python

import sys
import json

def getFiles():
	openFile = open(sys.argv[1], "r");
	allFiles = [x for x in openFile.read().split("\n") if len(x) > 0];
	openFile.close();
	return allFiles;

def processFile(filename, trigram, bigram, total, startConstant, separator):
	openFile = open(filename, "r")
	prevWord = startConstant
	prevprevWord = startConstant
	for word in openFile.read().split():
		if len(word) == 0:
			continue
		word = word.lower()
		last = word[len(word)-1]
		lastString = "" + last
		cut = False

		if not last.isalnum():
			cut = True
			word = word[0:-1]
			
		if not prevprevWord + separator + prevWord + separator + word in trigram:
			trigram[prevprevWord + separator + prevWord + separator + word]=0

		trigram[prevprevWord + separator + prevWord + separator + word]+=1

		if not prevWord + separator + word in bigram:
			bigram[prevWord + separator + word]=0

		bigram[prevWord + separator + word]+=1
		
		if not prevWord in total:
			total[prevWord]=0
		total[prevWord]+=1
		
		prevprevWord=prevWord
		prevWord = word


		if cut:
			if not prevprevWord + separator + prevWord + separator + lastString in trigram:
				trigram[prevprevWord + separator + prevWord + separator + lastString]=0
			trigram[prevprevWord + separator + prevWord + separator + lastString]+=1

			if not word + separator + lastString in bigram:
				bigram[word + separator + lastString]=0
			bigram[word + separator + lastString]+=1
			if not word in total:
				total[word]=0
			total[word]+=1
			
			if last != '.' and last != '!' and last != '?':
				prevprevWord = prevWord
				prevWord = lastString

			else:
				bigram["NAT_INT#NAT_INT"]+=1
				prevprevWord = startConstant
				prevWord = startConstant

trigram={}
bigram = {}
total = {}
allFiles = getFiles();

bigram["NAT_INT#NAT_INT"]=0

for filename in allFiles:
	processFile(filename, trigram, bigram, total, "NAT_INT", "#");

total["!"]=1
total["?"]=1
total["."]=1

# bigram["NAT_INT#NAT_INT"]=1

trigram_json = json.dumps(trigram, ensure_ascii = False)
bigram_json = json.dumps(bigram, ensure_ascii = False)
total_json = json.dumps(total, ensure_ascii = False)

# print trigram_json
#print bigram_json
#print total_json
trigramFile = open('trigram', 'w')
bigramFile = open('bigram', 'w')
totalFile = open('total', 'w')
trigramFile.write(trigram_json)
bigramFile.write(bigram_json)
totalFile.write(total_json)
bigramFile.close()
trigramFile.close()
totalFile.close()


'''
for word in total:
	count = 0
	for word2 in total:
		key = word + "#" + word2
		if key in bigram:
			count+=bigram[key]
	if total[word] != count:
		print total[word], count, word
'''


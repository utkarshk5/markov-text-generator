#!/usr/bin/python

import json
import random 

def getNextWord(prevWord, word, trigram, bigram, total, startConstant, separator):
	if word=="." or word == "?" or word == "!":
		return startConstant
	denom = bigram[prevWord + separator + word]
	# denom = total[word]
	rand = random.randint(1, denom)
	count = 0
	for nextWord in total:
		key = prevWord + separator + word + separator + nextWord
		if key in trigram:
			count += trigram[key]
			if count >= rand:
				return nextWord
	print "ERROR ", word, denom, count


def createSentence(trigram, bigram, total, startConstant, separator):
	prevprevWord = startConstant
	prevWord = startConstant
	sentence = ""
	while True:
		word = getNextWord(prevprevWord, prevWord, trigram, bigram, total, startConstant, separator)
		if word == startConstant:
			#print sentence
			return sentence
		if word.isalnum():
			sentence += " "
		#print word
		sentence += word
		prevprevWord=prevWord
		prevWord = word

def createDocument(trigram, bigram, total, startConstant, separator, totalWords):
	words = 0
	document = ""
	while words < totalWords:
		sentence = createSentence(trigram, bigram, total, startConstant, separator)
		document += sentence
		words += len(sentence.split())
	return document

trigramFile = open('trigram', 'r')
trigram = json.loads(trigramFile.read())
trigramFile.close()
bigramFile = open('bigram', 'r')
bigram = json.loads(bigramFile.read())
bigramFile.close()
totalFile = open('total', 'r')
total = json.loads(totalFile.read())

document = createDocument(trigram, bigram, total, "NAT_INT", "#", 80)
print document.title()



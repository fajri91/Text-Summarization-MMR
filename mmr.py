import os
import re
import sys
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import operator

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def load_stopWords():
	f = file('stopword.txt', 'r');
	return f.readlines()

stopwords = load_stopWords()	

def cleanData(sentence):
	#sentence = re.sub('[^A-Za-z0-9 ]+', '', sentence)
	#sentence filter(None, re.split("[.!?", setence))
	ret = []
	sentence = stemmer.stem(sentence)	
	for word in sentence.split():
		if not word in stopwords:
			ret.append(word)
	return " ".join(ret)


def getVectorSpace(cleanSet):
	vocab = {}
	for data in cleanSet:
		for word in data.split():
			vocab[data] = 0
	return vocab.keys()
	
def calculateSimilarity(sentence, doc):
	if doc == []:
		return 0
	vocab = {}
	for word in sentence:
		vocab[word] = 0
	
	docInOneSentence = '';
	for t in doc:
		docInOneSentence += (t + ' ')
		for word in t.split():
			vocab[word]=0	
	
	cv = CountVectorizer(vocabulary=vocab.keys())

	docVector = cv.fit_transform([docInOneSentence])
	sentenceVector = cv.fit_transform([sentence])
	return cosine_similarity(docVector, sentenceVector)[0][0]
	

data = file(sys.argv[1], 'r')
texts = data.readlines()

sentences = []
clean = []
originalSentenceOf = {}
	
import time
start = time.time()

#Data cleansing
for line in texts:
	parts = line.split('.')
	for part in parts:
		cl = cleanData(part)
		#print cl
		sentences.append(part)
		clean.append(cl)
		originalSentenceOf[cl] = part		
setClean = set(clean)
		
#calculate Similarity score each sentence with whole documents		
scores = {}
for data in clean:
	temp_doc = setClean - set([data])
	score = calculateSimilarity(data, list(temp_doc))
	scores[data] = score
	#print score


#calculate MMR
n = 20 * len(sentences) / 100
alpha = 0.5
summarySet = []
while n > 0:
	mmr = {}
	#kurangkan dengan set summary
	for sentence in scores.keys():
		if not sentence in summarySet:
			mmr[sentence] = alpha * scores[sentence] - (1-alpha) * calculateSimilarity(sentence, summarySet)	
	selected = max(mmr.iteritems(), key=operator.itemgetter(1))[0]	
	summarySet.append(selected)
	n -= 1

#rint str(time.time() - start)
	
print '\nSummary:\n'
for sentence in summarySet:
	print originalSentenceOf [sentence].lstrip(' ')
print

print '============================================================='
print '\nOriginal Passages:\n'
from termcolor import colored

for sentence in clean:
	if sentence in summarySet:
		print colored(originalSentenceOf[sentence].lstrip(' '), 'red')
	else:
		print originalSentenceOf[sentence].lstrip(' ')
	

############################################
# Project 2: Supervised Modeling Inference
############################################
from sup_model import *

# import sup_preprocessing after dic_preprocessing
# since both files have a function called lemma_stem_sentence
from dic_preprocessing import *
from sup_preprocessing import *
import datetime
import sys

# windowsize = 6
trainFileName = 'training_data.data'
outputFileName = 'supervised_test_output.py'
dic = parse_dictionary('dictionary-modified.xml')
num = 'num'
correctAnswer = []

# output the test result into a file
def decodeTestFile(testFileName, windowsize):
	print 'Begin decoding test file:', testFileName
	print 'Training began.'
	t1 = datetime.datetime.now()
	model = featureModel(trainFileName, windowsize)
	t2 = datetime.datetime.now()
	print 'Training finished.', t2-t1
	ftest = open(testFileName,'r')
	fout = open(outputFileName, "w")
	cnt = 0
	for line in ftest.readlines(): 
		fout.write(str(inferExample(line, model, windowsize)) + "\n")
		cnt += 1
		if cnt > 2:	sys.exit(0)
	fout.close()
	ftest.close()

# return MaxProbSenseID for one example
def inferExample(line, model, windowsize):
	# preprocessing
	words = line.split()
	word = words[0]
	senseID = words[2]
	correctAnswer.append(senseID)
	example = words[4:]
	useful = lemma_stem_sentence(" ".join(example))
	index = useful.index("%%")
	fv = useful[index-windowsize:index] + useful[index+3:index+windowsize+3]

	print 'word: ', word
	print 'correct ID: ', senseID
	print 'fv: ', fv

	# calculate the probability of each sense of the word
	maxSenseID = 0
	maxProb = 0.0
	numOfSense = dic[word][num]
	for i in range(1, numOfSense+1):
		prob = model.probSenseGivenFV(word, str(i), fv)
	if prob > maxProb:
		maxProb = prob
		maxSenseID = i
	if maxSenseID == 0:
		maxSenseID = model.defaultSense(word)
		print '************ DEFAULT ************'
	else:
		print '************ NOT DEFAUL ************'
	print 'maxProb:', maxProb
	print 'maxSenseID: ', maxSenseID
	return maxSenseID

# output accuracy
def evaluateValidFile(validFileName, windowsize):
	decodeTestFile(validFileName, windowsize)
	fout = open(outputFileName,'r')
	accurate = 0
	total = 0
	i = 0
	for line in fout.readlines():
		total += 1
		if int(line) == int(correctAnswer[i]):
			i += 1
			accurate += 1
	accuracy = (0.0+accurate) / total
	print 'accurate: ' + str(accurate)
	print 'total: ' + str(total)
	print 'accuracy: ' + str(accuracy)






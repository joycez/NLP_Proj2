############################################
# Project 2: Supervised Modeling Inference
############################################
from sup_model import *

# import sup_preprocessing after dic_preprocessing
# since both files have a function called lemma_stem_sentence
from dic_preprocessing import *
from sup_preprocessing import *

windowsize = 3
trainFileName = 'training_data.data'
outputFileName = 'supervised_test_output.py'
dic = parse_dictionary('dictionary-modified.xml')
num = 'num'
correctAnswer = []

# output the test result into a file
def decodeTestFile(testFileName):
	model = featureModel(trainFileName, windowsize)
	ftest = open(testFileName,'r')
	fout = open(outputFileName, "w")
	for line in ftest.readlines(): 
		fout.write(str(inferExample(line, model)) + "\n")
	fout.close()
	ftest.close()

# return MaxProbSenseID for one example
def inferExample(line, model):
	# preprocessing
	words = line.split()
	word = words[0]
	senseID = words[2]
	correctAnswer.append(senseID)
	example = words[4:]
	useful = lemma_stem_sentence(" ".join(example))
	index = useful.index("%%")
	fv = useful[index-windowsize:index] + useful[index+3:index+windowsize+3]

	# calculate the probability of each sense of the word
	maxSenseID = 0
	maxProb = 0.0
	numOfSense = dic[word][num]
	for i in range(1, numOfSense+1):
		prob = model.probSenseGivenFV(word, str(i), fv)
	if prob > maxProb:
		maxProb = prob
		maxSenseID = i
	return maxSenseID

# output accuracy
def evaluateValidFile(validFileName):
	decodeTestFile(validFileName)
	fout = open(outputFileName,'r')
	accurate = 0
	total = 0
	i = 0
	for line in fout.readlines():
		total += 1
		if int(line) == int(correctAnswer[i]): 
			accurate += 1
	accuracy = (0.0+accurate) / total
	print accurate
	print total
	print accuracy






#############################################################
# Project 2: Supervised Modeling
#############################################################
# simple feature vector used: array of the (#=windowsize)preceding words and
# (#=windowsize)following words
# example: (windowsize = 3)
# affect.v | 1 | ...make errors that could %% affect %% the security of Western Europe...
# feature vector: (make, errors, could, security, Western, Europe)
# Note: feature vector is chosen after lemmatizing

from collections import Counter
from sup_preprocessing import *

class featureModel:
	def __init__(self, trainFileName, windowsize):
                self.count = {}
                self.countFea = {}
                self.traindataSize = 0
                self.windowsize = windowsize
                self.traindata = parse_supervised(trainFileName, windowsize)
		self.trainModel(self.traindata, windowsize)
		             
 	def trainModel(self, traindata, windowsize):
                for word_n_ID, examples in traindata.items():
                        word = word_n_ID[0]
                        ID = word_n_ID[1]
                        for example in examples:
                                if (word, ID) in self.count:
                                        self.count[(word, ID)] += 1
                                else:
                                        self.count[(word, ID)] = 1
                                for featureword in example.split():
                                        if (word, ID, featureword) in self.countFea:
                                                self.countFea[(word, ID, featureword)] += 1
                                        else:
                                                self.countFea[(word, ID, featureword)] = 1
                
        def probSense(self, targetword, targetID):
                # prob P(s) = # of (word A, sense S) / # of (word A)
		number1 = 0
		number2 = 0

                # TODO:
                # a.
                # This is O(n), which makes evaluation a long process
                # try a constant alternative
                # try storing the counts as self.count[word][id]
                # then number2 = self.count[targetword][targetID]
                # For number1:
                # for id, cnt in self.count[targetword]:
                #       number1 += cnt
                # b.
                # Raise an exception instead of Printing an Error

		for (word, ID) in self.count:
                        if word == targetword:
                                number1 += self.count[(word, ID)]
                                if ID == targetID:
                                        number2 = self.count[(word, ID)]
                if number1 == 0:
                        print 'Error: No such word in the training data'
                        return
                prob = 1.0 * number2/number1
                return prob

	def probFeature(self, targetword, targetID, targetfea):
                # prob P(f|s) = # of (wordA, sense S, feature F) / # of (wordA, sense S)
                # TODO: BUG here
                # if (targetword, targetID, targetfea) is not an existed key
                # it raises an exception
                # I changed the codes as below, not sure if that's correct
                
                # if self.countFea[(targetword, targetID, targetfea)] == 0:
                        # print 'Error: No such context in the training data'
                        # return
                if (targetword, targetID, targetfea) not in self.countFea.keys():
                        prob = 0
                else:
		      prob = 1.0 * self.countFea[(targetword, targetID, targetfea)]/self.count[targetword, targetID]
                return prob

        
#########################################################################################################
        def probFeatureVector(self, targetword, targetID, fv):
                prob = 1.0
                for feature in fv:
                        prob *= self.probFeature(targetword, targetID, feature)
                return prob

        def probSenseGivenFV(self, targetword, targetID, fv):
                return self.probFeatureVector(targetword, targetID, fv) * self.probSense(targetword, targetID)

        

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
from collections import defaultdict
from sup_preprocessing import *

class featureModel:
	def __init__(self, trainFileName, windowsize):
                # 1-D, 2-D and 3-D dictionaries are used to store training data
                self.countWord = {}
                self.countWordID = defaultdict(dict)
                self.countFea = defaultdict(lambda: defaultdict(dict))
                self.traindataSize = 0
                self.windowsize = windowsize
                self.traindata = parse_supervised(trainFileName, windowsize)
		self.trainModel(self.traindata, windowsize)
		             
 	def trainModel(self, traindata, windowsize):
                for word_n_ID, examples in traindata.items():
                        word = word_n_ID[0]
                        ID = word_n_ID[1]
                        for example in examples:
                                if word in self.countWord:
                                        self.countWord[word] += 1
                                else:
                                        self.countWord[word] = 1
                                if word in self.countWordID.keys():
                                        if ID in self.countWordID[word].keys():
                                                self.countWordID[word][ID] += 1
                                        else:
                                                self.countWordID[word][ID] = 1
                                else:
                                        self.countWordID[word][ID] = 1
                                for featureword in example:
                                        if word in self.countFea.keys():
                                                if ID in self.countFea[word].keys():
                                                        if featureword in self.countFea[word][ID].keys():
                                                                self.countFea[word][ID][featureword] += 1
                                                        else:
                                                                self.countFea[word][ID][featureword] = 1
                                                else:
                                                        self.countFea[word][ID][featureword] = 1
                                        else:
                                                self.countFea[word][ID][featureword] = 1

        def probSense(self, targetword, targetID):
                # prob P(s) = # of (word A, sense S) / # of (word A)
		number1 = self.countWord[targetword]
		number2 = self.countWordID[targetword][targetID]

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
                
                # in what kind of cases could number1=0 happen? Python will raise key error if
                # there is no such entry in the dictionary
                if (targetword, targetID) not in self.countWordID.keys():
                        prob = 0
                else:
                        prob = 1.0 * number2/number1
                return prob
        
	def probFeature(self, targetword, targetID, targetfea):
                # prob P(f|s) = # of (wordA, sense S, feature F) / # of (wordA, sense S)
                # NOTE: targetword, targetID, targetfea must all be strings

                # TODO: BUG here
                # if (targetword, targetID, targetfea) is not an existed key
                # it raises an exception
                # I changed the codes as below, not sure if that's correct
                
                # if self.countFea[(targetword, targetID, targetfea)] == 0:
                        # print 'Error: No such context in the training data'
                        # return
                print targetword, targetID, targetfea
                print self.countWordID
                number1 = self.countWordID[targetword][targetID]
		number2 = self.countFea[targetword][targetID][targetfea]
                if (targetword, targetID, targetfea) not in self.countFea.keys():
                        prob = 0
                else:
                        prob = 1.0 * number2/number1
                return prob
        
        def probFeatureVector(self, targetword, targetID, fv):
                prob = 1.0
                for feature in fv:
                        prob *= self.probFeature(targetword, targetID, feature)
                return prob

        def probSenseGivenFV(self, targetword, targetID, fv):
                return self.probFeatureVector(targetword, targetID, fv) * self.probSense(targetword, targetID)

        def defaultSense(self, targetword):
                maxNum = 0
                maxID = ''
                for targetID in self.countWordID[targetword].keys():
                        if self.countWordID[targetword][targetID] > maxNum:
                                maxID = targetID
                                maxNum = self.countWordID[targetword][targetID]
                return maxID
                        

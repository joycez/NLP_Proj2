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
from dic_preprocessing import *
from sup_preprocessing import *
from math import log

class featureModel:
	def __init__(self, trainFileName, windowsize):
                self.WordTF_all = Counter()

                data=parse_supervised(trainFileName, windowsize)
                for word_n_ID, examples in data.items():
                        for example in examples:
                                for featureword in example:
                                        self.WordTF_all[featureword]+=1

                self.WordTF=Counter()
                print 'COMMON: ', self.WordTF_all.most_common(1000)[:5]
                for key,v in self.WordTF_all.most_common(1000):
                        self.WordTF[key]=v
                self.Ndict = len(self.WordTF)
                
                self.countWord = Counter()
                self.countWordID = defaultdict(Counter)
                self.countWordIDPair = defaultdict(Counter)
                self.countWordIDFea = defaultdict(lambda: defaultdict(Counter))
                self.countWordIDLocPair = defaultdict(lambda: defaultdict(Counter))
                self.countWordIDLocFea = defaultdict(lambda:defaultdict(lambda: defaultdict(Counter)))
                self.trainModel(data, windowsize)
                
                self.dic = parse_dictionary('dictionary-modified.xml')
                
 	def trainModel(self, traindata, windowsize):
                for word_n_ID, examples in traindata.items():
                        word = word_n_ID[0]
                        ID = word_n_ID[1]

                        for example in examples:
                                self.countWord[word] += 1
                                self.countWordID[word][ID] += 1
                                
                                for i in range(len(example)):
                                        featureword=example[i]
                                        if self.WordTF[featureword]>0:
                                                self.countWordIDPair[word][ID] += 1
                                                self.countWordIDFea[word][ID][featureword]+=1
                                                self.countWordIDLocPair[word][ID][i] +=1
                                                self.countWordIDLocFea[word][ID][i][featureword]+=1

                        
	def probSenseGivenFV(self, targetword, targetID, fv):
                prob = log(self.countWordID[targetword][targetID]+1)-log(self.countWord[targetword]+self.dic[targetword]['num'])
                for i in range(len(fv)):
                        feature=fv[i]
                        if self.WordTF[feature]>0:
                                prob += log(self.countWordIDFea[targetword][targetID][feature]+1)-log(self.countWordIDPair[targetword][targetID]+self.Ndict)
                                if (i>0 and i<3):
                                        prob += log(self.countWordIDLocFea[targetword][targetID][i][feature]+1)-log(self.countWordIDLocPair[targetword][targetID][i]+self.Ndict)
                return prob

        def defaultSense(self, targetword):
                maxNum = 0
                maxID = ''
                for targetID in self.countWordID[targetword].keys():
                        if self.countWordID[targetword][targetID] > maxNum:
                                maxID = targetID
                                maxNum = self.countWordID[targetword][targetID]
                return maxID
                        

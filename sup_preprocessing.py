#!/usr/bin/env python

from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter

import re
import xml.etree.ElementTree as ET

######################################################
# 		global variables
######################################################

glob_Lucene = ["a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"];

def parse_supervised(train_filename, windowsize):
    traindata = {}
    trainfile = open(train_filename,'r')
    #TODO:
    #Provide a sentence-level API that takes a single
    #entry as input and output (word, senseID, lemma_stem_sentence(" ".join(example))
    #see 'inference.py' line 31-37
    for line in trainfile.readlines():
        words = line.split()
        # only want the sentence starting from the 5th word in an entry 
        example = words[4:]
        useful = lemma_stem_sentence(" ".join(example))
        # find the target word
        index = useful.index('%%')
        prevCon = " ".join(useful[index-windowsize:index])
        nextCon = " ".join(useful[index+3:index+windowsize+3])
        useful = " ".join([prevCon, nextCon])
        # output dictionary: {word:[example1, example2,..]}
        if (words[0], words[2]) in traindata:
            traindata[(words[0], words[2])].append(useful)
        else:
            traindata[(words[0], words[2])] = []
            traindata[(words[0], words[2])].append(useful)
##    print traindata
    return traindata

def lemma_stem_sentence(sentence):
    lmtzr = WordNetLemmatizer()
    ls = LancasterStemmer()
    word_list = []
    # only keeps words aA-zZ0-9_ and %% 
    single_words = re.findall("\w+|%%",sentence)
    for single_word in single_words:
        lemmed = lmtzr.lemmatize(single_word)
        if not lemmed in glob_Lucene:
            word_list.append(lemmed)
    print word_list
    return word_list

if __name__ == '__main__':
##	parse_supervised("training_data.data")
	parse_supervised("sample.data", 3)


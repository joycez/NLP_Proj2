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
        entry = parse_entry(line, windowsize)
        # output dictionary: {word:[example1, example2,..]}
        if (entry[0], entry[1]) in traindata:
            traindata[(entry[0], entry[1])].append(entry[2])
        else:
            traindata[(entry[0], entry[1])] = []
            traindata[(entry[0], entry[1])].append(entry[2])
##    print traindata
    return traindata

def parse_entry(line, windowsize):
    # given an original tuple in the train.data, parse it into an entry (word, senseID, context)
    entry = []
    words = line.split()
    # only want the sentence starting from the 5th word in an entry
    example = words[4:]
    useful = lemma_stem_sentence(" ".join(example))
    # find the target word
    index = useful.index('%%')
    fv = useful[index-windowsize:index] + useful[index+3:index+windowsize+3]
    entry.append(words[0])
    entry.append(words[2])
    entry.append(fv)
    return entry

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
    return word_list

if __name__ == '__main__':
##	parse_supervised("training_data.data")
	parse_supervised("sample.data", 3)


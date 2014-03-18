#!/usr/bin/env python

import dic_preprocessing as dic_pre

def wsd_sense(cur_sense, target_word, word_context):
    consecutive_count = 0;
    hit_count = 0
    word_list = []
    for word_list_itm in cur_sense["examples"]:
        word_list += word_list_itm

    word_list += cur_sense["gloss"]
    # print word_list
    for word_itm in word_context:
        # print word_itm
        if word_itm != target_word and word_itm in word_list:
            hit_count += 1

    max_successive = find_max_match(cur_sense, word_context)
    return [hit_count,max_successive]

def find_max_match(cur_sense, word_context):
    word_len = len(word_context)
    for itm0 in xrange(0,word_len):
        cur_len = word_len - itm0
        for itm1 in xrange(0,itm0+1):
            cur_sense_list = word_context[itm1:itm1+cur_len]
            for word_list_itm in cur_sense["examples"]:
                if word_list_match(cur_sense_list, word_list_itm):
                    return cur_len
            if word_list_match(cur_sense_list, cur_sense["gloss"]):
                return cur_len

    return 0

def word_list_match(cur_word_list, sentence):
    cur_len = len(cur_word_list)
    sen_len = len(sentence)
    if cur_len > sen_len:
        return False
    for itm0 in xrange(0, sen_len-cur_len+1):
        is_match = True
        for itm1 in xrange(0,cur_len):
            if cur_word_list[itm1] != sentence[itm1+itm0]:
                is_match = False
                break

        if is_match:
            return True

    return False

def basic_score(dictionary, validation_list):
    match_count = 0

    for cur_val_dict in validation_list:
        cur_word = cur_val_dict["word"]
        cur_word_dict = dictionary.get(cur_word)
        best_match_sense_idx = -1
        best_match_data = None
        if cur_word_dict != None:
            for cur_sense in cur_word_dict["senses"]:
                cur_match_data = wsd_sense(cur_sense, cur_word.split(".")[0],cur_val_dict["sentence"])
                # print cur_match_data
                if (best_match_sense_idx == -1) or \
                (cur_match_data[1] > best_match_data[1]) or \
                (cur_match_data[1] == best_match_data[1] and cur_match_data[0] > best_match_data[0]):
                    best_match_sense_idx = cur_sense["id"]
                    best_match_data = cur_match_data

            if int(best_match_sense_idx) == -1:
                best_match_sense_idx = str(1)
            if int(best_match_sense_idx) == cur_val_dict["real_sense"]:
                match_count += 1

            # print best_match_sense_idx

    return match_count*1./len(validation_list)

######################################################
#       second best match
######################################################
def second_best_match(dictionary, validation_list):
    match_count = 0

    for cur_val_dict in validation_list:
        cur_word = cur_val_dict["word"]
        cur_word_dict = dictionary.get(cur_word)
        longest_consecutive_idx = -1
        longest_consecutive_data = None
        longest_counthit_idx = -1
        longest_counthit_data = None
        if cur_word_dict != None:
            for cur_sense in cur_word_dict["senses"]:
                cur_match_data = wsd_sense(cur_sense, cur_word.split(".")[0],cur_val_dict["sentence"])
                # print cur_match_data
                if (longest_consecutive_idx == -1) or \
                (cur_match_data[1] > longest_consecutive_data[1]):
                    longest_consecutive_idx = cur_sense["id"]
                    longest_consecutive_data = cur_match_data

                if (longest_counthit_idx == -1) or \
                (cur_match_data[0] > longest_counthit_data[0]):
                    longest_counthit_idx = cur_sense["id"]
                    longest_counthit_data = cur_match_data

            if int(longest_consecutive_idx) == -1 and int(longest_counthit_idx) == -1:
                longest_consecutive_idx = str(1)

            if int(longest_consecutive_idx) == cur_val_dict["real_sense"] or \
            int(longest_counthit_idx) == cur_val_dict["real_sense"]:
                match_count += 1


        # print str(longest_consecutive_idx) + " # " + str(longest_counthit_idx)

    return match_count*1./len(validation_list)

def new_score_match(dictionary, validation_list):
    match_count = 0

    for cur_val_dict in validation_list:
        cur_word = cur_val_dict["word"]
        cur_word_dict = dictionary.get(cur_word)
        longest_consecutive_idx = -1
        longest_consecutive_data = None
        longest_counthit_idx = -1
        longest_counthit_data = None
        if cur_word_dict != None:
            for cur_sense in cur_word_dict["senses"]:
                cur_match_data = wsd_sense(cur_sense, cur_word.split(".")[0],cur_val_dict["sentence"])
                # print cur_match_data
                if (longest_consecutive_idx == -1) or \
                (cur_match_data[1] > longest_consecutive_data[1]):
                    longest_consecutive_idx = cur_sense["id"]
                    longest_consecutive_data = cur_match_data

                if (longest_counthit_idx == -1) or \
                (cur_match_data[0] > longest_counthit_data[0]):
                    longest_counthit_idx = cur_sense["id"]
                    longest_counthit_data = cur_match_data

            if int(longest_consecutive_idx) == -1 and int(longest_counthit_idx) == -1:
                longest_consecutive_idx = str(1)

            if int(longest_consecutive_idx) == cur_val_dict["real_sense"]:
                match_count += 0.7
            elif int(longest_counthit_idx) == cur_val_dict["real_sense"]:
                match_count += 0.3


        # print str(longest_consecutive_idx) + " # " + str(longest_counthit_idx)

    return match_count*1./(len(validation_list)*0.7)

if __name__ == '__main__':

    dictionary = dic_pre.parse_dictionary(dic_pre.glob_dict_path)
    validation_list = dic_pre.parse_validation(dic_pre.glob_valid_path)
    # score is 0.488745980707
    # print basic_score(dictionary, validation_list)
    # score is 0.657020364416
    # print second_best_match(dictionary, validation_list)
    # score is 0.5835247282183673
    print new_score_match(dictionary, validation_list)
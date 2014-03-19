#!/usr/bin/env python

import dic_preprocessing as dic_pre
import os

glob_nums = [0]

def wsd_sense(cur_sense, target_word, word_context):
    consecutive_count = 0;
    hit_count = 0
    word_list = []
    """
    for word_list_itm in cur_sense["examples"]:
        print word_list_itm
    print word_context
    """
    for word_list_itm in cur_sense["examples"]:
        word_list += word_list_itm

    word_list += cur_sense["gloss"]

    for word_itm in word_context:

        if word_itm != target_word and word_itm in word_list:
            hit_count += 1

        """
        for itm2 in word_list:
            if itm2 == word_itm:
                hit_count += 1
        """
    """
    max_successive = find_max_match(cur_sense, word_context)
    return [hit_count,max_successive]
    """

    nums = find_match_num(cur_sense, word_context)
    """
    if nums[1] != 0:
        glob_nums[0] += 1
        print str(nums[1]) + "#"+ str(glob_nums[0])
    """
    return [hit_count, nums[0], nums[1]]

def data_comparasion(data1, data2):

    """
    if data1[2] - data2[2] >= 1:
        return True
    """
    if data1[1]**3 + data1[0] > data2[1]**3 + data2[0]:
        return True
    else:
        return False

def find_match_num(cur_sense, word_context):

    consecutive_num = 0
    max_len = 0
    word_len = len(word_context)
    for itm0 in xrange(0,word_len):
        cur_len = word_len - itm0

        if cur_len <= 1:
            return [consecutive_num , max_len]
        for itm1 in xrange(0,itm0+1):
            cur_sense_list = word_context[itm1:itm1+cur_len]
            for word_list_itm in cur_sense["examples"]:
                if word_list_match(cur_sense_list, word_list_itm):
                    if max_len == 0:
                        max_len = cur_len
                    consecutive_num += cur_len
            if word_list_match(cur_sense_list, cur_sense["gloss"]):
                if max_len == 0:
                    max_len = cur_len
                consecutive_num += cur_len

    return [consecutive_num, max_len]

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
    # print "cur_word_list " + str(cur_word_list)
    # print "setence " + str(sentence)
    if cur_len > sen_len:
        # print False
        return False
    for itm0 in xrange(0, sen_len-cur_len+1):
        is_match = True
        for itm1 in xrange(0,cur_len):
            if cur_word_list[itm1] != sentence[itm1+itm0]:
                is_match = False
                break

        if is_match:
            # print True
            return True
    # print False
    return False

def basic_score(dictionary, validation_list):
    try:
        os.remove("basic.csv")
    except OSError:
        pass
    
    with open("basic.csv", "a") as output_file:
        output_file.write("Id,Prediction\n")
        match_count = 0
        count_num = 0
        for cur_val_dict in validation_list:
            cur_word = cur_val_dict["word"]
            cur_word_dict = dictionary.get(cur_word)
            best_match_sense_idx = -1
            best_match_data = None
            if cur_word_dict != None:
                for cur_sense in cur_word_dict["senses"]:
                    cur_match_data = wsd_sense(cur_sense, cur_word.split(".")[0],cur_val_dict["sentence"])

                    if (best_match_sense_idx == -1) or \
                    data_comparasion(cur_match_data,best_match_data):
                        best_match_sense_idx = cur_sense["id"]
                        best_match_data = cur_match_data

                if int(best_match_sense_idx) == -1:
                    best_match_sense_idx = str(1)
                if int(best_match_sense_idx) == cur_val_dict["real_sense"]:
                    match_count += 1
            count_num += 1
            output_file.write("%d,%d\n"%(count_num, int(best_match_sense_idx)))
            # print best_match_sense_idx

    return match_count*1./len(validation_list)



######################################################
#       second best match 
######################################################
def second_best_match(dictionary, validation_list):
    try:
        os.remove("second_best_match.csv")
    except OSError:
        pass
    
    with open("second_best_match.csv","a") as output_file:
        output_file.write("Id,Prediction1,Prediction2\n")

        match_count = 0
        count_num = 0
        for cur_val_dict in validation_list:
            cur_word = cur_val_dict["word"]
            cur_word_dict = dictionary.get(cur_word)
            first_best_idx = -1
            first_best_data = None
            second_best_idx = -1
            second_best_data = None
            if cur_word_dict != None:
                for cur_sense in cur_word_dict["senses"]:
                    cur_match_data = wsd_sense(cur_sense, cur_word.split(".")[0],cur_val_dict["sentence"])
                    # print cur_match_data
                    if (first_best_idx == -1) or \
                    data_comparasion(cur_match_data,first_best_data):
                        if first_best_idx != -1:
                            second_best_idx = first_best_idx
                            second_best_data = first_best_data
                        first_best_idx = cur_sense["id"]
                        first_best_data = cur_match_data

                    if (second_best_idx == -1) or \
                    data_comparasion(cur_match_data, second_best_data):
                        if first_best_idx != cur_sense["id"]:
                            second_best_idx = cur_sense["id"]
                            second_best_data = cur_match_data

                if int(first_best_idx) == -1:
                    first_best_idx = str(1)

                if int(second_best_idx) == -1:
                    second_best_idx = str(1)

                if int(first_best_idx) == cur_val_dict["real_sense"] or \
                int(second_best_idx) == cur_val_dict["real_sense"]:
                    match_count += 1

            count_num += 1
            output_file.write("%d,%d,%d\n"%(count_num, int(first_best_idx), int(second_best_idx)))
        # print str(longest_consecutive_idx) + " # " + str(longest_counthit_idx)

    return match_count*1./len(validation_list)

def new_score_match(dictionary, validation_list):
    try:
        os.remove("new_score_match.csv")
    except OSError:
        pass

    with open("new_score_match.csv","a") as output_file:
        match_count = 0
        count_num = 0

        for cur_val_dict in validation_list:
            cur_word = cur_val_dict["word"]
            cur_word_dict = dictionary.get(cur_word)
            first_best_idx = -1
            first_best_data = None
            second_best_idx = -1
            second_best_data = None
            if cur_word_dict != None:
                for cur_sense in cur_word_dict["senses"]:
                    cur_match_data = wsd_sense(cur_sense, cur_word.split(".")[0],cur_val_dict["sentence"])
                    # print cur_match_data
                    if (first_best_idx == -1) or \
                    data_comparasion(cur_match_data,first_best_data):
                        if first_best_idx != -1:
                            second_best_idx = first_best_idx
                            second_best_data = first_best_data
                        first_best_idx = cur_sense["id"]
                        first_best_data = cur_match_data

                    if (second_best_idx == -1) or \
                    data_comparasion(cur_match_data, second_best_data):
                        if first_best_idx != cur_sense["id"]:
                            second_best_idx = cur_sense["id"]
                            second_best_data = cur_match_data

                if int(first_best_idx) == -1:
                    first_best_idx = str(1)

                if int(second_best_idx) == -1:
                    second_best_idx = str(1)

                if int(first_best_idx) == cur_val_dict["real_sense"]:
                    match_count += 0.7
                if int(second_best_idx) == cur_val_dict["real_sense"]:
                    match_count += 0.3

            # print str(longest_consecutive_idx) + " # " + str(longest_counthit_idx)
            count_num += 1
            output_file.write("%d,%d,%d\n"%(count_num, int(first_best_idx), int(second_best_idx)))
    return match_count*1./(len(validation_list)*0.7)

if __name__ == '__main__':

    dictionary = dic_pre.parse_dictionary(dic_pre.glob_dict_path)
    validation_list = dic_pre.parse_validation(dic_pre.glob_valid_path)
    # print dictionary
    # print validation_list
    # print basic_score(dictionary, validation_list)

    print second_best_match(dictionary, validation_list)

    # print new_score_match(dictionary, validation_list)
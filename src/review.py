#!/usr/bin/env python3

import os
from dotenv import  dotenv_values 
import random

vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    PROJECT_REVIEW_NAME=str(vals['PROJECT_REVIEW_NAME'])
except:
    PROJECT_REVIEW_NAME='.llm.review.txt'

ADD_TEXT = "*"
REM_TEXT = "*del"
ADD_AUTO = " **"

memory_review = []
sub_review = []
index_review = []
memory_final_index = []

identifiers_dict={'ai': 'jane'}

weight = {
    "a": {},
    "b": {}
}

score = {
    "a": 0,
    "b": 0
}

notsimilar = {
    "a": 0,
    "b": 0 
}

## set these outside module ##
remove_ai = True 
sample_len = 2 
add_auto = True 

def _is_weight_surprise(text_comparison, text_surprise):
    if isinstance(text_comparison, list):  
        k = ''
        for i in text_comparison:
            k += "\n " + i
        text_comparison = k.strip() 
        ## allow list input
    w = len(text_comparison.split("\n")) ## number of lines in comparison text.
    if w < 2:
        return False
    weight["a"].clear()
    weight["b"].clear()
    score["a"] = 0
    score["b"] = 0
    notsimilar["a"] = 0 
    notsimilar["b"] = 0

    weight["a"] = _weigh(text_comparison)
    weight["b"] = _weigh(text_surprise)

    len_a = len(text_comparison.strip().split(' '))
    len_b = len(text_surprise.strip().split(' '))
    score["a"] = len_a
    score["b"] = len_b
    j = {}
    notsimilar["b"] = 0
    for i in weight["b"]:
        if i not in weight["a"]:
            j[i] = weight["b"][i] ## <-- weight from surprising text??
            notsimilar["b"] += weight["b"][i]
    #print(j, notsimilar["b"] )
    m = {}
    notsimilar["a"] = 0
    for i in weight["a"]:
        if i not in weight["b"]:
            m[i] = weight["a"][i]
            notsimilar["a"] += weight["a"][i]
    #print(m, notsimilar["a"] )
    if notsimilar["b"] > notsimilar["a"] / w:
        return True
    else:
        return False

def _weigh(text):
    dict_out = {}
    tt = []
    t = text.strip().split()
    for i in t:
        if i.strip() != "":
            tt.append(i.strip())
    for i in tt:
        if i[:2] not in dict_out:
            dict_out[ i[:2] ] = 1
        dict_out[ i[:2] ] += len(i) - 1
    return dict_out

def _last_entries(user_list, ai_list):
    global remove_ai 
    global sample_len 
    num = sample_len
    last = []
    if num > len(user_list):
        num = len(user_list) 
    if len(user_list) == len(ai_list):
        for i in range(num):
            ii = num - (i  )
            #print(len(user_list) - ii)
            u_line = user_list[len(user_list) - ii]
            a_line = ai_list[len(ai_list) - ii]
            last.append(u_line)
            if not remove_ai:
                last.append(a_line)
    #print(last)
    return last 

def read_review( selection ):
    global memory_review 
    global sub_review 
    global index_review
    global memory_final_index 
    memory_review = []
    sub_review = []
    index_review = []
    memory_final_index = []

    name = PROJECT_REVIEW_NAME 
    path = os.path.expanduser("~") + "/" + name
    #print(path)
    if os.path.exists(path) == False:
        return
    f = open(path, 'r')
    rev = f.readlines()
    num = 0 
    for i in rev:
        #print(i)
        sub_review.append(i.strip())
        index_review.append(num)
        num += 1 
    f.close()
    if selection >= len(sub_review) :
        memory_review = sub_review
        return
    for i in range( selection ):
        x = random.randint(0, len(index_review) - 1)
        memory_final_index.append(index_review[x])
        #print(i, x, memory_final_index, index_review)
        del index_review[x]
        pass 
    memory_final_index.sort()
    for i in memory_final_index:
        memory_review.append(sub_review[i])

def find_marked_text( user_list, ai_list,  text, identifiers={'ai': 'jane'}):
    global memory_review
    global identifiers_dict 
    identifiers_dict = identifiers
    listx = _last_entries(user_list, ai_list )
    save = ''
    if REM_TEXT in text:
        for t in text.split('.'):
            if REM_TEXT in t:
                save = t
                break 
        save = _remove_bad_chars(save)
        save = save.replace(REM_TEXT, '')
        save = _return_without_name(save)
        _rem_matching_sentence(sub_review , save)
        # save all memory_review here and return
        return True 
        
    if not ADD_TEXT in text and add_auto:
        mark = _is_weight_surprise(listx, text)
        if mark:
            text += ADD_AUTO #" **"
        if not mark:
            return False
    if ADD_TEXT in text:
        for t in text.split('.'):
            if "*" in t:
                save = t
                break 
        save = _remove_bad_chars(save)
        save = save.replace(ADD_TEXT, '')
        save = _return_without_name(save)

        do_match = _check_words_do_match(memory_review, save)
        if do_match:
            return True## <-- we already have one !! 
            
        if len(save.strip()) > 0 :
            f = open(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME, "a")
            f.write(save.strip().lower() + "\n")
            f.close()
        return True

def _return_without_name(save):
    global identifiers_dict
    if ":" in save:
        ## trim name from 'save'
        s = save.split(":")
        if len(s[0].strip().split(' ')) == 1 or s[0].strip() in identifiers_dict.values():
            save = s[1]
    return save

def _check_words_do_match(memory, save):
    words_match = False
    for i in memory:
        j = i.lower().split(' ')
        k = save.lower().split(" ")
        ss = []
        for kk in k:
            if kk.strip() != "":
                ss.append(kk)
        k = ss 
        #j.sort()
        #k.sort()
        m = min(len(j), len(k))
        words_match = True
        for ii in range(m):
            if j[ii].lower() != k[ii].lower():
                words_match = False
        if words_match:
            return True
    ## <-- we already have one !! 
    return words_match

def _rem_matching_sentence(memory, save):
    words_match = False 
    line_skipped = False
    if os.path.exists(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak"):
        os.remove(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak")
    f = open(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak", "a")

    for i in memory:
        j = i.lower().split(' ')
        k = save.lower().split(" ")
        ss = []
        for kk in k:
            if kk.strip() != "":
                ss.append(kk)
        k = ss 
        #j.sort()
        #k.sort()
        m = min(len(j), len(k))
        #words_match = True
        for ii in range(m):
            if j[ii].lower() == k[ii].lower():
                words_match = True
            if not words_match:
                break 
        if (not words_match) or line_skipped:
            f.write(i + "\n")
        else:
            line_skipped = True

    f.close()
    if os.path.exists(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak"):
        os.rename(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak", os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME )

def _remove_bad_chars(save):
    save = save.replace(";", '') 
    save = save.replace("/", '')
    save = save.replace('\\', '')
    save = save.replace('!', '')
    save = save.replace(')', '')
    save = save.replace('(', '')
    return save

if __name__ == '__main__':
    read_review(50)
    #print(memory_review)
    #print(_weigh('some text me, you, i'))
    ## test find_marked_text() ##
    add_auto = True
    ai_list_test = ['hi', 'how are you?', 'that is good.']
    user_list_test = ['hello.', 'i am well.', 'thanks. I agree.']
    ai_text = " i'm  *del " 
    find_marked_text(user_list_test, ai_list_test, ai_text)

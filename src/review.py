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
REM_TEXT = "--"
ADD_AUTO = " **"

memory_review = []
sub_review = []
index_review = []
memory_final_index = []

identifiers_dict={'ai': 'jane'}

## set these outside module ##
remove_ai = True 
sample_len = 2 
add_auto = False
similarity_ratio = 0.8 

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

def _segment_text(txt):
    a = []
    for x in txt.split('\n'):
        for y in x.split('.'):
            a.append(y)
    return a 

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

def find_marked_text( user_list, ai_list, text, identifiers={'ai':'jane'} ):
    marked = False

    for t in text.split('\n'):
        #print('?',t)
        x = _proc_text(user_list, ai_list, t, identifiers)
        if x == True:
            marked = True
    return marked

def _proc_text( user_list, ai_list,  text, identifiers={'ai': 'jane'}):
    global memory_review
    global identifiers_dict 
    global sub_review 
    identifiers_dict = identifiers
    listx = _last_entries(user_list, ai_list )
    save = ''
    text = _prepare_for_segmenting(text)
    if (REM_TEXT in text and ADD_TEXT in text) or identifiers_dict['mem'] in text.split(':')[0]:
            return False
    if text.strip() == '':
        return False
    if REM_TEXT in text or identifiers_dict['mem'] in text.split(':')[0]:
        save = _remove_bad_chars(text)
        save = save.replace(REM_TEXT, '')
        save = _return_without_name(save)
        #save = save + REM_TEXT
        line_found = _rem_matching_sentence(sub_review , save)
        if not line_found:
            ## save line if not already saved!!
            save = save + ADD_TEXT
            pass 
        else:
            return True 
    ## does this take into account multiple sentences on one line?
    if (not ADD_TEXT in text) and add_auto:
        mark = False
        #for t in _segment_text(text): # text.split('.'):
        m = _is_weight_surprise(listx, text)
        #mark = _is_weight_surprise(listx, text)
        if m:
            text = text + ADD_AUTO 
            mark = True
        if not mark:
            return False
    if ADD_TEXT in text or identifiers_dict['mem'] in text.split(':')[0]:
        save = _remove_bad_chars(text)
        save = save.replace(ADD_TEXT, '')
        save = _return_without_name(save)
        print('[' , save, ']')
        #print('###>>', save)
        #print('---', sub_review, '---')
        do_match = _check_words_do_match(sub_review, save)
        if do_match:
            print('already have one', save)
            return True## <-- we already have one !! 
            
        if len(save.strip()) > 0 :
            print('???', save)
            f = open(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME, "a")# as f:
            f.write(save.strip().lower() + "\n")
            f.flush()
            f.close()
        return True
    return False

def is_skipable(text, identifiers):
    global identifiers_dict 
    identifiers_dict = identifiers 
    if REM_TEXT in text:
        return True
    name = text.split(':')[0].strip()
    name = _remove_bad_chars(name)
    if identifiers_dict['mem'] in name or identifiers_dict['user'] in name:
        return True
    return False

def _return_without_name(save):
    global identifiers_dict
    if ":" in save:
        ## trim name from 'save'
        s = save.split(":")
        if s[0].strip() in identifiers_dict.values():
            save = s[1]
        if len(s) > 1 and identifiers_dict['mem'] in s[0]:
            save = s[1]
    return save

def _check_words_do_match(memory, save):
    for i in memory:
        i = _remove_bad_chars(i)
        j = i.lower().split(' ')
        k = save.lower().split(" ")
        ss = []
        for kk in k:
            if kk.strip() != "":
                ss.append(kk)
        k = ss 
        #j.sort()
        #k.sort()
        if ' '.join(j) == ' '.join(k):
            print('match', j)
            return True
        ## ditch the rest!!
    print('no-match', save)
    return False

def _rem_matching_sentence(memory, save):
    words_match = False 
    line_skipped = False
    line_found = False
    if os.path.exists(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak"):
        os.remove(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak")
    f = open(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak", "a")

    for i in memory:
        i = _remove_bad_chars(i)
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
        num_matching_words = 0 
        for ii in range(m):
            if j[ii].lower() == k[ii].lower():
                words_match = True
                num_matching_words += 1 
            #if not words_match:
            #    break 
        if m == 0:
            m = 1
        if (not words_match and num_matching_words / float(m) <= similarity_ratio) or line_skipped:
            if len(i.strip()) > 0:
                f.write(i + "\n")
        else:
            line_skipped = True
            line_found = True
    f.close()
    if os.path.exists(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak"):
        os.rename(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME + ".bak", os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME )
    return line_found

def _remove_bad_chars(save):
    save = save.replace(";", '') 
    save = save.replace("/", '')
    save = save.replace('\\', '')
    #save = save.replace('!', '')
    save = save.replace(')', '')
    save = save.replace('(', '')
    save = save.replace('"', '')
    save = save.replace("'", '')
    save = save.replace(",", '')
    return save

def _prepare_for_segmenting(save):
    save = save.replace('!', '.')
    save = save.replace("?", '.')

    return save

if __name__ == '__main__':
    read_review(50)
    d = {'mem': 'memory'}
    #add_auto = True
    ai_list_test = ['hi', 'how are you?', 'that is good.']
    user_list_test = ['hello.', 'i am well.', 'thanks. I agree.']
    ai_text = '* memory: my name is jane with exclamation point \n  x is the word y is the word * '
    print('is_skipable', is_skipable(ai_text, d))
    print('find_marked_text', ai_text, find_marked_text(user_list_test, ai_list_test, ai_text, d))
    print("--")
    for i in sub_review:
        print(i)
    print("--")

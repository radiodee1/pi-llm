#!/usr/bin/env python3

import os
from dotenv import  dotenv_values 
import random

ADD_TEXT = "++"
REM_TEXT = "--"
ADD_AUTO = " ++"

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
skip_read_write = False
user_dir = os.path.expanduser('~')

vals = dotenv_values(user_dir + "/.llm.env")

try:
    PROJECT_REVIEW_NAME=str(vals['PROJECT_REVIEW_NAME'])
except:
    PROJECT_REVIEW_NAME='.llm.review.txt'


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
    else:
        if len(user_list) == 0 and len(ai_list) > 0:
            user_list = ai_list
        if num * 2 > len(user_list) :
            num = len(user_list) // 2
        for i in range(num * 2):
            ii = num * 2 - i 
            x = (len(user_list) - ii ) % 2 
            if len(user_list) - ii >= len(user_list) or len(user_list) - ii < 0:
                continue
            u_line = user_list[len(user_list) - ii]
            #a_line = user_list[len(user_list) - ii]
            if x == 0:
                last.append(u_line)
                pass 
            elif x == 1 and remove_ai:
                last.append(u_line)
    #print(last)
    return last 

def _segment_text(txt):
    a = []
    for x in txt.split('\n'):
        for y in x.split('.'):
            a.append(y)
    return a 

def set_user_dir(directory):
    global user_dir
    global vals 
    global PROJECT_REVIEW_NAME
    user_dir = directory
    vals = dotenv_values(user_dir + "/.llm.env")
    try:
        PROJECT_REVIEW_NAME=str(vals['PROJECT_REVIEW_NAME'])
    except:
        PROJECT_REVIEW_NAME='.llm.review.txt'


def read_review( selection ):
    global memory_review 
    global sub_review 
    global index_review
    global memory_final_index
    global PROJECT_REVIEW_NAME 

    global user_dir
    vals =  dotenv_values(user_dir + "/.llm.env")

    memory_review = []
    sub_review = []
    index_review = []
    memory_final_index = []


    name = PROJECT_REVIEW_NAME 
    path = user_dir + "/" + name
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

    for t in _segment_text(text): # text.split('\n'):
        #print('?',t)
        x = _proc_text(user_list, ai_list, t, identifiers)
        if x == True:
            marked = True
    return marked

def _proc_text( user_list, ai_list,  text, identifiers={'ai': 'jane'}):
    global memory_review ## <<-- not needed here??
    global identifiers_dict 
    global sub_review
    global PROJECT_REVIEW_NAME
    global user_dir

    identifiers_dict = identifiers
    listx = _last_entries(user_list, ai_list )
    save = ''
    text = _prepare_for_segmenting(text)
    if (REM_TEXT in text and ADD_TEXT in text): # or identifiers_dict['mem'] in text.split(':')[0]:
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
            text = save + ADD_TEXT
            pass 
        else:
            return True 
    ## does this take into account multiple sentences on one line?
    if (not ADD_TEXT in text) and add_auto:
        mark = False
        text = _remove_bad_chars(text)
        #for t in _segment_text(text): # text.split('.'):
        m = _is_weight_surprise(listx, text)
        #mark = _is_weight_surprise(listx, text)
        if m:
            text = text + ADD_AUTO 
            mark = True
        if not mark:
            return False
    if ADD_TEXT in text: # or identifiers_dict['mem'] in text.split(':')[0]:
        save = _remove_bad_chars(text)
        save = save.replace(ADD_TEXT, '')
        
        save = _return_without_name(save)
        #print('[' , save, ']')
        #print('###>>', save)
        #print('---', sub_review, '---')
        do_match = _check_words_do_match(sub_review, save)
        if do_match:
            #print('already have one', save)
            return True## <-- we already have one !! 
            
        if len(save.strip()) > 0 and not skip_read_write :
            #print('???', save)
            sub_review.append(save.strip().lower())
            f = open(user_dir + "/" + PROJECT_REVIEW_NAME, "a")# as f:
            f.write(save.strip().lower() + "\n")
            f.flush()
            f.close()
        return True
    return False

def is_skipable(text, identifiers):
    global identifiers_dict
    identifiers_dict = identifiers
    for i in text.split('\n'):
        text = i.strip().lower() 

        if REM_TEXT in text or ADD_TEXT in text:
            return True
        name = text.split(':')[0].strip()
        name = _remove_bad_chars(name)
        if identifiers_dict['mem'] in name: # or identifiers_dict['user'] in name:
            return True
    return False

def _return_without_name(save):
    global identifiers_dict
    save_out = save
    if ":" in save:
        ## trim name from 'save'
        s = save.split(":")
        print(s, 'list of input')
        if s[0].strip() in identifiers_dict.values():
            save = s[1:]#.strip()
        if len(s) > 1 and identifiers_dict['mem'] in s[0]:
            save = s[1:]#.strip()
        save_out = s[1].strip()
        for t in save:
            if len(t.strip()) > 0:
                save_out = t.strip()
                break 
    return save_out

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
        tt = []
        for jj in j:
            if jj.strip() != "":
                tt.append(jj)
        j = tt 
        if ' '.join(j) == ' '.join(k):
            return True
    return False

def _rem_matching_sentence(memory, save):
    global PROJECT_REVIEW_NAME
    global user_dir

    if skip_read_write:
        return True ## line_found
    words_match = False 
    line_skipped = False
    line_found = False
    if os.path.exists(user_dir + "/" + PROJECT_REVIEW_NAME + ".bak"):
        os.remove(user_dir + "/" + PROJECT_REVIEW_NAME + ".bak")
    f = open(user_dir + "/" + PROJECT_REVIEW_NAME + ".bak", "a")

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
    if os.path.exists(user_dir + "/" + PROJECT_REVIEW_NAME + ".bak"):
        os.rename(user_dir + "/" + PROJECT_REVIEW_NAME + ".bak", user_dir + "/" + PROJECT_REVIEW_NAME )
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
    save = save.strip('.')
    return save

def _prepare_for_segmenting(save):
    save = save.replace('!', '.')
    save = save.replace("?", '.')

    return save

if __name__ == '__main__':
    read_review(50)
    d = {'mem': 'memory'}
    #add_auto = True
    skip_read_write = False
    ai_list_test = ['hi', 'how are you?', 'that is good.']
    user_list_test = ['hello.', 'i am well.', 'thanks. I agree.']
    ai_text = ADD_TEXT + ' memory: my name is jane with exclamation point \n  x is the word y is the word ' + ADD_TEXT
    print('is_skipable', is_skipable(ai_text, d))
    print('find_marked_text', ai_text, find_marked_text(user_list_test, [], ai_text, d))
    print("--")
    for i in sub_review:
        print(i)
    print("--")

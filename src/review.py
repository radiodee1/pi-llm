#!/usr/bin/env python3

import os
from dotenv import  dotenv_values 


vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    PROJECT_REVIEW_NAME=str(vals['PROJECT_REVIEW_NAME'])
except:
    PROJECT_REVIEW_NAME='.llm.review.txt'

memory_review = []

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

def is_weight_surprise(text_comparison, text_surprise):
    if isinstance(text_comparison, list):  
        k = ''
        for i in text_comparison:
            k += "\n " + i
        text_comparison = k.strip() 
        ## allow list input
    w = len(text_comparison.split("\n")) ## number of lines in comparison text.
    if w < 2:
        return False
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
    print(j, notsimilar["b"] )
    m = {}
    notsimilar["a"] = 0
    for i in weight["a"]:
        if i not in weight["b"]:
            m[i] = weight["a"][i]
            notsimilar["a"] += weight["a"][i]
    print(m, notsimilar["a"] )
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
        if i[0] not in dict_out:
            dict_out[ i[0] ] = 1
        dict_out[ i[0] ] += len(i) - 1
    return dict_out

def _last_entries(user_list, ai_list, num = 4):
    last = []
    if num > len(user_list):
        num = len(user_list) 
    if len(user_list) == len(ai_list):
        for i in range(num):
            ii = num - (i  )
            print(len(user_list) - ii)
            u_line = user_list[len(user_list) - ii]
            a_line = ai_list[len(ai_list) - ii]
            last.append(u_line)
            last.append(a_line)
    print(last)
    return last 

def read_review():
    global memory_review 
    memory_review = []
    name = PROJECT_REVIEW_NAME 
    path = os.path.expanduser("~") + "/" + name
    print(path)
    if os.path.exists(path) == False:
        return
    f = open(path, 'r')
    rev = f.readlines()
    for i in rev:
        print(i)
        memory_review.append(i.strip())
    f.close()

def find_marked_text( user_list, ai_list,  text, identifiers={'ai': 'jane'}):
    global memory_review
    read_review()
    listx = _last_entries(user_list, ai_list, 2)
    save = ''
    if not '*' in text:
        mark = is_weight_surprise(listx, text)
        if mark:
            text += " **"
        if not mark:
            return False
    if '*' in text:
        for t in text.split('.'):
            if "*" in t:
                save = t
                break 
        save = save.replace("*", '')
        save = save.replace(";", '') 
        save = save.replace("/", '')
        save = save.replace('\\', '')
        save = save.replace('!', '')

        if ":" in save:
            ## trim name from 'save'
            s = save.split(":")
            if len(s[0].strip().split(' ')) == 1 or s[0].strip() in identifiers.values():
                save = s[1]

        for i in memory_review:
            j = i.split(' ')
            k = save.split(" ")
            ss = []
            for kk in k:
                if kk.strip() != "":
                    ss.append(kk)
            k = ss 
            j.sort()
            k.sort()
            m = min(len(j), len(k))
            words_match = True
            for ii in range(m):
                if j[ii].lower() != k[ii].lower():
                    words_match = False
                    break
            if words_match:
                return True## <-- we already have one !! 
            
        if len(save.strip()) > 0 :
            f = open(os.path.expanduser('~') + "/" + PROJECT_REVIEW_NAME, "a")
            f.write(save.strip().lower() + "\n")
            f.close()
        return True




if __name__ == '__main__':
    list_first =  ['here is some text', 'here is some more', 'finally here']
    list_second =  ['some things', 'some more', 'also things']
    surprise = "exactly the text x is the word"
    g = find_marked_text(list_first, list_second, surprise)
    print(g, 'g')


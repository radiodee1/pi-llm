#!/usr/bin/env python3


weight = {
        "a": {},
        "b": {}
        }

score = {
        "a": 0,
        "b": 0
        }

def get_weight(text_a, text_b):
    weight["a"] = weigh(text_a)
    weight["b"] = weigh(text_b)
    len_a = len(text_a.strip().split(' '))
    len_b = len(text_b.strip().split(' '))
    score["a"] = len_a
    score["b"] = len_b
    j = []
    for i in weight["b"]:
        if i not in weight["a"]:
            j.append(i)
    print(j)
    pass 

def weigh(text):
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

if __name__ == '__main__':
    get_weight("hello out there", "some other text")


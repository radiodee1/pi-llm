#!/usr/bin/env python3


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

def get_weight(text_a, text_b):

    weight["a"] = weigh(text_a)
    weight["b"] = weigh(text_b)
    len_a = len(text_a.strip().split(' '))
    len_b = len(text_b.strip().split(' '))
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
    if notsimilar["b"] > notsimilar["a"]:
        return True
    else:
        return False

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
    g = get_weight("hello out there", "some other text that's really surprising!")
    print(g)
    print(weight)
    print(score)
    print("---")
    g = get_weight("a b c d e f g h i j k l m n o p q r s t u v w x y z", "some other text that returns false.")
    print(g)

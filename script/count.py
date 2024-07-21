#!/bin/env python3

import argparse

blacklist = ['hello']
HIGH_LIMIT = 5 


class Kernel:

    def __init__(self):
        self.length = 0
        self.file = ''
        self.dict_words = {}

    def open_and_count(self):
        if self.file.strip() != "":
            f = open(self.file, 'r')
            x = f.readlines()
            f.close()
            for i in x:
                if ':' in i:
                    ii = i.split(':')[1].strip()
                    #print(ii)
                    for j in ii.split(' '):
                        if j.lower() not in self.dict_words:
                            self.dict_words[j.lower()] = 0
                        self.dict_words[j.lower()] += 1
        pass 

    def print_stats(self):
        high = 0
        key_record = ''
        count = 0
        total = len(self.dict_words)
        for _ in range(len(self.dict_words)):
            for key in self.dict_words:
                if self.dict_words[key] > high:
                    key_record = key
                    high = self.dict_words[key]
            if key_record not in blacklist and self.dict_words[key_record] > HIGH_LIMIT:
                print(key_record, self.dict_words[key_record])
                count += 1
            del self.dict_words[key_record]
            high = 0
            key_record = ''
        print(self.dict_words, count, total)
        pass 

if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM Output File Counter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', default=str, help="File name and path.")
    args = parser.parse_args()

    if args.file != None and args.file.strip() != "":
        k.file = args.file 
        k.open_and_count()
        k.print_stats()

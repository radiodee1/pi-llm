#!/bin/env python3

import argparse

blacklist = ['and', 'to', 'the', 'for', 'a', 'is', 'of', 'on']
HIGH_LIMIT = 0 

bad_characters = [ ',', '!', '.', '?' ]

class Kernel:

    def __init__(self):
        self.length = 0
        self.file = ''
        self.dict_words = {}
        self.num_sentences = 0
        self.num_words = 0

    def open_and_count(self):
        if self.file.strip() != "":
            f = open(self.file, 'r')
            x = f.readlines()
            f.close()
            for i in x:
                if ':' in i:
                    self.num_sentences += 1
                    for k in bad_characters:
                        i = i.replace(k, '')
                    ii = i.split(':')[1].strip()
                    #print(ii)
                    for j in ii.split(' '):
                        self.num_words += 1
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
                print(key_record + ',', self.dict_words[key_record])
                count += 1
            del self.dict_words[key_record]
            high = 0
            key_record = ''
        print('displayed:' , count, 'categories:', total, 'words:', self.num_words ,'sentence:', self.num_words / float(self.num_sentences))
        print('sentences:', self.num_sentences, 'exchanges:', self.num_sentences / 2)
        pass 

if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM Output File Counter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', default=str, help="File name and path.")
    parser.add_argument('--low', default=10, help="Threshold for displaying word frequency.")
    args = parser.parse_args()
    
    if args.low != None and int(args.low) >= -1:
        HIGH_LIMIT = int(args.low)

    if args.file != None and args.file.strip() != "":
        k.file = args.file 
        k.open_and_count()
        k.print_stats()

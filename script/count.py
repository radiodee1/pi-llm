#!/bin/env python3

import argparse

blacklist = ['and', 'to', 'the', 'for', 'a', 'is', 'of', 'on', '']
HIGH_LIMIT = 0 

bad_characters = [ ',', '!', '.', '?' ]

class Kernel:

    def __init__(self):
        self.length = 0
        self.file = ''
        self.file_list = []
        self.dict_words = {}
        self.num_sentences = 0
        self.num_words = 0
        self.num_restarts = 0
        self.count = -1 

    def open_and_count(self):
        if self.file.strip() != "":
            self.file_list.append(self.file.strip())
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
                    if ii == 'say something':
                        self.num_restarts += 1
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
                if count >= self.count and self.count != -1:
                    break 
                count += 1
            del self.dict_words[key_record]
            high = 0
            key_record = ''
        print()
        print('displayed:' , count, 'categories:', total, 'words:', self.num_words ,'sentence:', self.num_words / float(self.num_sentences))
        print('sentences:', self.num_sentences, 'exchanges:', self.num_sentences / 2, end=" ")
        print('restarts:', self.num_restarts, 'files:', self.file_list)
        pass 

if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM Output File Counter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('files', default='', nargs='+', help="File names and paths.")
    parser.add_argument('--low', default=10, help="Threshold for displaying word frequency.")
    parser.add_argument('--count', default=-1, help="Highest number of possible output.")
    args = parser.parse_args()
    
    print(args)

    if args.low != None and int(args.low) >= -1:
        HIGH_LIMIT = int(args.low)

    if args.count != None and int(args.count) != -1:
        k.count = int(args.count) - 1 

    if args.files != None and len(args.files) > 0:
        for i in args.files:
            k.file = i 
            k.open_and_count()
        k.print_stats()

#!/bin/env python3

import argparse

blacklist = ['and', 'to', 'the', 'for', 'a', 'is', 'of', 'on', '', ')', '(', 'i', '&']


bad_characters = [ ',', '!', '.', '?', "'", "’" ]

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
        self.combine = False
        self.save = False
        self.high_limit = 0

    def open_and_count(self):
        if self.file.strip() != "":
            #self.file_list.append(self.file.strip())
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
        has_written = False
        total = len(self.dict_words)
        for _ in range(len(self.dict_words)):
            for key in self.dict_words:
                if self.dict_words[key] > high:
                    key_record = key
                    high = self.dict_words[key]
            if key_record not in blacklist and self.dict_words[key_record] > self.high_limit :
                print(key_record + ',', self.dict_words[key_record])
                self.file_output(key_record + ", " + str(self.dict_words[key_record]))
                has_written = True 
                if count >= self.count and self.count != -1:
                    break 
                count += 1
            del self.dict_words[key_record]
            high = 0
            key_record = ''
        if not has_written:
            self.file_output("")
        print()
        print('displayed:' , count, 'categories:', total, 'words:', self.num_words ,'sentence:', self.num_words / float(self.num_sentences))
        print('sentences:', self.num_sentences, 'exchanges:', self.num_sentences / 2, end=" ")
        print('restarts:', self.num_restarts, 'files:', self.file_list)
        pass 

    def file_output(self, line_out=""):
        if not self.save:
            return
        name = self.file.split('/')[0:-1]
        n = self.file.split('/')[-1] 
        n = 'count-' + n[:-4] + '.count.txt'
        name = '/' + '/'.join(name)
        if self.combine:
            #print(self.file)
            name += '/count-llm.combine.count.txt'
        else:
            name = name + '/' + n 
            #name = name[:-4]

        #print("Name output:", name)
        f = open(name, 'a')
        f.write(line_out + "\n")
        f.close()
        pass 

if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM Output File Counter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('files', default='', nargs='+', help="File names and paths.")
    parser.add_argument('--low', default=-1, help="Threshold for displaying word frequency.")
    parser.add_argument('--count', default=-1, help="Highest number of possible output.")
    parser.add_argument('--combine', action="store_true", help="Singe output option.")
    parser.add_argument('--save', action="store_true", help="Store output to 'count.txt' file.")
    args = parser.parse_args()
    
    print(args)
    
    def setup_args(ll, ar):
        ll = Kernel()

        ll.combine = ar.combine
        ll.save = ar.save

        if ar.low != None and int(ar.low) >= -1:
            ll.high_limit = int(ar.low)

        if ar.count != None and int(ar.count) != -1:
            ll.count = int(ar.count) - 1 

        if ar.save != None:
            ll.save = ar.save

        #print("setup", ar)
        #print("object", ll)
        return ll 

    if args.files != None and args.combine and len(args.files) > 0:
        if args.combine:
            k = setup_args(k, args)
            for i in args.files:
                k.file = i
                if k.file.endswith(".count.txt"):
                    continue
                k.open_and_count()
            k.print_stats()
            exit()

    if args.files != None and not args.combine and len(args.files) > 0:
        for i in args.files:
            k = setup_args(k, args)
            k.file = i
            #print(k.file, 'i file')
            if not k.file.endswith(".count.txt"):
                k.open_and_count()
                k.print_stats()
        exit()



#!/bin/env python3

import argparse

class Kernel:

    def __init__(self):
        self.length = 0
        self.file = ''
        self.dict_words = {}

    def open_and_count(self):
        pass 

    def print_stats(self):
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

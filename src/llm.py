#!/usr/bin/python3

import argparse

test_txt = [ 
            'hi, my name is jane',
            'I like candy',
            'I like the color blue',
            'please dont be confused',
            'where are we?'
            ]


class Kernel:

    def __init__(self):
        self.verbose = True
        self.local = False
        self.remote = False
        self.test = False

    def loop(self):
        z = True
        x = 0 
        while z == True:
            print(test_txt[x])
            x += 1
            x = x % len(test_txt)
            g = input("say something (stop to quit) >> ")
            if g == "stop":
                z = False
        print("here")


if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--local', action="store_true", help="Use local LLM model")
    parser.add_argument('--remote', action="store_true", help="Use remote LLM model")
    parser.add_argument('--test', action="store_true", help="Use test data and no LLM")
    
    args = parser.parse_args()
    
    if args.local == True:
        k.local = True
        k.remote = False
        k.test = True

    if args.remote == True:
        k.local = False
        k.remote = True
        k.test = False

    k.test = args.test

    k.loop()


#!/usr/bin/env python3

import os 

class Prompt:

    def __init__(self, path='', identifiers={}) -> None:
        self.init_string = path
        self.mem = []
        self.optimal_size = -1 
        self.identifiers = identifiers 
        self.build_mem()
        pass

    def build_mem(self):
        for i in self.init_string.split(':'):
            if len(i.strip()) > 0:
                j = List(i.strip())
                j.modify_init()
                j.read_file()
                self.mem.append(j)

    def get_size(self):
        j = 0
        for i in self.mem:
            j += i.get_size()
        return j 

    def set_size(self, x):
        self.optimal_size = x 

    def add_pair(self, pair):
        if isinstance(pair, list) and len(pair) == 2:
            for i in self.mem:
                i.add_pair(pair)
        #self.mem.append(pair)
        pass 

    def add_single(self, single):
        if isinstance(single, str):
            for i in self.mem:
                i.add_single(single)
        #self.mem.append(single)
        pass 

    def output(self):
        return ''

    def json_output(self):
        return '{}'

    def set_identifiers(self, ident):
        self.identifiers = ident

    def get_identifiers(self):
        return self.identifiers

class List:

    def __init__(self, path='') -> None:
        self.init_string = path
        self.list = []
        self.growable = False
        self.shrinkable = False
        self.modify = False
        self.pairs = True
        self.size = -1 
        self.identifiers = {}
        self.identifiers_pair_a = ""
        self.identifiers_pair_b = ""
        self.identifiers_single = ""
        self.keywords = {}
        self.filenames = {}

        self.set_keywords()
        pass

    def set_keywords(self):
        self.keywords = {
            'growable': 'MEMORY,CONVERSATION',
            'shrinkable': 'MEMORY,CONVERSATION',
            'pairs': 'MEMORY,CONVERSATION',
            'modify': 'COMBINED'
        }
        self.filenames = {
            'growable': '',
            'shrinkable': '',
            'pairs': 'conversation.csv',
            'modify': '',
            'single': 'combined.csv'
        }

    def modify_init(self):
        for i in self.init_string.split(':'):
            if len(i.strip()) > 0:

                if i.strip().upper() in self.keywords['growable']:
                    self.growable = True
                if i.strip().upper() in self.keywords['shrinkable']:
                    self.shrinkable = True
                if i.strip().upper() in self.keywords['pairs']:
                    self.pairs = True

                p = i.strip()
                if os.path.exists(p):
                    p = p.split('/')[-1]
                    print(p)
                    if p in self.filenames['growable']:
                        self.growable = True
                    if p in self.filenames['shrinkable']:
                        self.shrinkable = True
                    if p in self.filenames['pairs']:
                        self.pairs = True
                    if p in self.filenames['single']:
                        self.pairs = False
                    if p in self.filenames['modify']:
                        self.modify = True


    def read_file(self):
        if os.path.exists(self.init_string):
            f = open(self.init_string, 'r')
            x = f.readlines()
            for i in x:
                if i.startswith('#') or len(i.strip()) == 0:
                    continue
                self.list.append(i.strip('\n'))
        pass 

    def set_identifiers(self, identifiers):
        self.identifiers = identifiers
        self.identifiers_pair_a = identifiers['user']
        self.identifiers_pair_b = identifiers['ai']
        self.identifiers_single = identifiers['mem']

    def get_identifiers(self):
        return self.identifiers

    def add_pair(self, pair):
        if self.pairs == True and self.growable == True:
            if isinstance(pair, list) and len(pair) == 2:
                self.list.extend(pair)

    def add_single(self, single):
        if self.pairs == False and self.growable == True:
            if isinstance(single, str):
                self.list.append(single)

    def mod_list(self):
        pass

    def mod_entry(self, line):
        print(line)
        pass 

    def shrink(self, size):
        if self.shrinkable:
            print(size)

    def output(self):
        return ''

    def json_output(self):
        return '{}'

    def get_size(self):
        return len(self.list)

if __name__ == '__main__':
    m = Prompt('MEMORY:review:../files/combined.csv', {'mem':'test', 'user':'me', 'ai': 'jane'})
    print(m, m.identifiers)
    print(m.mem)
    for i in m.mem:
        print(i.init_string, 'pairs', i.pairs)
        print(i.list)

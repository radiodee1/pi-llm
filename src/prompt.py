#!/usr/bin/env python3

class Prompt:

    def __init__(self, path='') -> None:
        self.init_string = path
        self.mem = []
        self.optimal_size = -1 
        self.identifiers = {}
        pass

    def get_size(self):
        return 0 

    def set_size(self, x):
        self.optimal_size = x 

    def add_pair(self, pair):
        self.mem.append(pair)

    def add_single(self, single):
        self.mem.append(single)

    def output(self):
        return ''

    def json_output(self):
        return '{}'

    def set_identifiers(self, ident):
        self.identifiers = ident

class List:

    def __init__(self, path='') -> None:
        self.init_string = path
        self.list = []
        self.growable = False
        self.shrinkable = False
        self.pairs = True
        self.size = -1 
        self.identifiers = {}
        self.identifiers_pair_a = ""
        self.identifiers_pair_b = ""
        self.identifiers_single = ""
        pass

    def set_identifiers(self, identifiers):
        self.identifiers = identifiers

    def add_pair(self, pair):
        if self.pairs == True:
            self.list.append(pair)

    def add_single(self, single):
        if self.pairs == False:
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

if __name__ == '__main__':
    m = Prompt('')
    print(m)

#!/usr/bin/env python3

import os 
import math
import datetime

class Prompt:

    def __init__(self, path='', identifiers={}) -> None:
        self.init_string = path
        self.mem = []
        self.optimal_size = -1 
        self.shrink_unit = 0
        self.identifiers = identifiers 
        self.build_mem()
        pass

    def build_mem(self):
        num = 0 
        for i in self.init_string.split(':'):
            if len(i.strip()) > 0:
                j = List(i.strip())
                j.set_identifiers(self.identifiers)
                j.modify_init()
                j.read_file()
                #j.shrink(2)
                j.set_index(num)
                self.mem.append(j)
                num += 1

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

    def output(self, question=''):
        duplicate = ''
        for i in self.mem:
            duplicate += i.output(question)
        return duplicate

    def json_output(self, question=''):
        duplicate = []
        for i in self.mem:
            duplicate += i.json_output(question)
        return duplicate

    def pc_output(self, question=''):
        duplicate = ''
        for i in self.mem:
            duplicate += i.pc_output(question)
        return duplicate

    def set_identifiers(self, ident):
        self.identifiers = ident

    def get_identifiers(self):
        return self.identifiers

    def shrink(self, num):
        self.shrink_unit = num
        s = 0
        for i in self.mem:
            if i.shrinkable:
                s += 1
        if num > 0 and s > 0:
            k = num // s 
            if k < 1:
                k = 1
            k = math.ceil(k)
            for i in self.mem:
                if i.shrinkable:
                    i.shrink(k)

    def get_index_from_name(self, name):
        for i in self.mem:
            if name.strip() in i.init_string:
                return i.index
        return -1 

    def set_show_from_name(self, name):
        for i in self.mem:
            if name.strip() in i.init_string:
                i.show = True
                return

    def set_hide_from_name(self, name):
        for i in self.mem:
            if name.strip() in i.init_string:
                i.show = False
                return

    def set_show(self, index, show):
        for i in self.mem:
            if index == i.index:
                i.show = show
                return 

    def replace_list(self, x, index):
        for i in self.mem:
            if index == i.index:
                i.replace_list(x, index)
                return
        pass 

    def get_recent(self):
        for i in self.mem:
            if i.growable and i.shrinkable:
                return i.get_recent()
        return ['','']

    def get_size_by_name(self, name):
        for i in self.mem:
            if name.strip() in i.init_string:
                return len(i.list)
        return 0 

class List:

    def __init__(self, path='') -> None:
        self.init_string = path
        self.list = []
        self.growable = False
        self.shrinkable = False
        self.shrink_unit = 0
        self.modify = False
        self.pairs = True
        self.size = -1 
        self.show = True      
        self.replace = False
        self.index = -1

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
            'modify': 'COMBINED,REVIEW',
            'single': 'REVIEW,RULES,INSTRUCTIONS',
            'replace': 'REVIEW,RULES,INSTRUCTIONS'
        }
        self.filenames = {
            'growable': '',
            'shrinkable': '', # 'conversation.txt',
            'pairs': 'conversation.txt',
            'modify': 'review-instructions.txt,combined.txt',
            'single': 'review-instructions.txt,combined.txt'
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
                if i.strip().upper() in self.keywords['single']:
                    self.pairs = False
                if i.strip().upper() in self.keywords['replace']:
                    self.replace = True
                if i.strip().upper() in self.keywords['modify']:
                    self.modify = True

                p = i.strip()

                if not os.path.exists(p):
                    i = p.strip().split('/')[-1]
                    if os.path.exists('/app/'):
                        p = '/app/' + i 

                if os.path.exists(p):
                    p = p.split('/')[-1]
                    #print(p)
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
        if not os.path.exists(self.init_string):
            i = self.init_string.strip().split('/')[-1]
            if os.path.exists('/app/'):
                self.init_string = '/app/' + i 
        
        #print(self.init_string)

        if os.path.exists(self.init_string):
            f = open(self.init_string, 'r')
            x = f.readlines()
            for i in x:
                if i.startswith('#') or len(i.strip()) == 0:
                    continue
                self.list.append(i.strip('\n'))
            f.close()
        self.size = len(self.list)

    def set_identifiers(self, identifiers):
        self.identifiers = identifiers
        self.identifiers_pair_a = identifiers['user']
        self.identifiers_pair_b = identifiers['ai']
        self.identifiers_single = identifiers['mem']

    def get_identifiers(self):
        return self.identifiers

    def add_pair(self, pair, index = -1):
        if index == -1 or self.index == -1 or self.index == index:
            if self.pairs == True and self.growable == True:
                if isinstance(pair, list) and len(pair) == 2:
                    self.list.extend(pair)

    def add_single(self, single, index = -1):
        if index == -1 or self.index == -1 or self.index == index:
            if self.pairs == False and self.growable == True:
                if isinstance(single, str):
                    self.list.append(single)

    def replace_list(self, x, index = -1):
        if (index == -1 or self.index == -1 or self.index == index) and self.replace == True:
            if isinstance(x, list):
                if len(x) == 2 and isinstance(x[0], list): 
                    if len(x[0]) == 2 and isinstance(x[0][0], str) and isinstance(x[0][1], str) :
                        self.list = [] 
                        for i in x:
                            if isinstance(i, list) and len(i) == 2:
                                self.list.append(i[0])
                                self.list.append(i[1])
                else:
                    self.list = x 
            self.size = len(self.list)


    def mod_list(self):
        duplicate = []
        for i in self.list:
            if self.modify:
                duplicate.append(self.mod_entry(i))
            else:
                duplicate.append(i)
        return duplicate

    def mod_entry(self, line):
        if line.strip() == 'time':
            now = datetime.datetime.now()
            return 'The Time is ' + now.strftime("%H:%M") 
        if line.strip() == 'date':
            now = datetime.datetime.now()
            return 'The Date is ' + now.strftime("%A, %b %d, %Y") 
        if line.strip() == 'location':
            return 'The location is New York'
        if line.strip() == 'occupation':
            return 'My occupation is "Student"'
        #print(line, '<---')
        return line 

    def shrink(self, size):
        if self.shrinkable:
            self.shrink_unit = size
            if self.pairs:
                x = size % 2
                if x != 0:
                    self.shrink_unit += 1 
            print(self.shrink_unit, 'shrink')

    def output(self, question='', index= -1):
        if not self.show:
            return ''
        d_list = self.mod_list()
        duplicate = ''
        for i in range(len(d_list) ):
            if self.shrinkable:
                j = self.shrink_unit  
            else:
                j = 0 
            y =  i + j 
            if (y < 0 or y >= len(d_list)): 
                continue
            if self.pairs:
                x = (y) % 2
                if x == 0:
                    duplicate += self.identifiers_pair_a + ': ' + d_list[y] + '\n'
                else:
                    duplicate += self.identifiers_pair_b + ': ' + d_list[y] + '\n'
            else:
                duplicate += self.identifiers_single + ': ' + d_list[y] + '\n'

        if question.strip() != "" and self.growable: # and index == self.index:
            duplicate += self.identifiers_pair_a + ': ' + question.strip() + '\n'

        return duplicate

    def format_json(self, user, text):
        user = user.lower().split(' ')[0]
        user = user.replace('\'', "\"")
        text = text.strip()
        text = text.replace('\'', '"')
        if user == self.identifiers['ai'].lower() :
            t = 'assistant'
        else:
            t = 'user'

        x = { 'role' : t, 'content': user + " : " + text }
        return x 

    def json_output(self, question = '', index= -1):
        if not self.show:
            return []
        d_list = self.mod_list()
        duplicate = []
        for i in range(len(d_list) ):
            if self.shrinkable:
                j = self.shrink_unit  
            else:
                j = 0 
            y =  i + j 
            if (y < 0 or y >= len(d_list)): 
                continue
            if self.pairs:
                x = (y) % 2
                if x == 0:
                    duplicate += [self.format_json( self.identifiers_pair_a, d_list[y] )]
                else:
                    duplicate += [self.format_json( self.identifiers_pair_b, d_list[y] )] 
            else:
                duplicate += [self.format_json( self.identifiers_single, d_list[y] )]

        if question.strip() != "" and self.growable: # and index == self.index:
            duplicate += [ self.format_json( self.identifiers_pair_a , question.strip() )]

        return duplicate

    def pc_output(self, question='', index= -1):
        if not self.show:
            return ''
        d_list = self.mod_list()
        duplicate = ''
        for i in range(len(d_list) ):
            if self.shrinkable:
                j = self.shrink_unit  
            else:
                j = 0 
            y =  i + j 
            if (y < 0 or y >= len(d_list)): 
                continue
            duplicate +=  (  d_list[y] + '\n')

        if question.strip() != "" and self.growable: # and index == self.index:
            duplicate += question.strip() + '\n'
        return duplicate

    def get_size(self):
        return len(self.list)

    def set_size(self, size):
        self.size = size

    def set_index(self, i):
        self.index = i 

    def get_recent(self):
        if self.growable and self.shrinkable and len(self.list) % 2 == 0:
            return [ self.list[ -2 ], self.list[ -1 ] ]
        else:
            return ['', '']
        pass 

    def set_show(self, index, show):
        if self.index == index:
            self.show = show

if __name__ == '__main__':
    m = Prompt('INSTRUCTIONS:RULES:REVIEW:../files/combined.txt:../files/conversation.txt:MEMORY', {'mem':'storage', 'user':'user', 'ai': 'jane'})
    m.add_pair(['hi','howdy'])
    m.add_pair(['whazzup', 'nothing'])
    print(m.get_recent())
    print('====')
    print(m.pc_output())
    print(m.get_size_by_name('conversation'))

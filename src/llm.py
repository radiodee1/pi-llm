#!/usr/bin/env python3

import argparse
from dotenv import  dotenv_values 
import os
import speech_recognition as sr
from gtts import gTTS 
from playsound import playsound
import multiprocessing as mp 
import time
import requests
import json

vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    TEST_SIX=int(vals['TEST_SIX']) 
except:
    TEST_SIX = 8 # 32 

try:
    TEST_NINE=int(vals['TEST_NINE']) 
except:
    TEST_NINE = 16

try:
    MICROPHONE_INDEX=int(vals['MICROPHONE_INDEX'])
except:
    MICROPHONE_INDEX=-1

try:
    OPENAI_API_KEY=str(vals['OPENAI_API_KEY'])
except:
    OPENAI_API_KEY='abc'

try:
    OPENAI_ORGANIZATION=str(vals['OPENAI_ORGANIZATION'])
except:
    OPENAI_ORGANIZATION=""

try:
    OPENAI_PROJECT_ID=str(vals['OPENAI_PROJECT_ID'])
except:
    OPENAI_PROJECT_ID=""

try:
    OPENAI_MODEL=str(vals['OPENAI_MODEL'])
except:
    OPENAI_MODEL="gpt-3.5-turbo"

try:
    OPENAI_URL=str(vals['OPENAI_URL'])
except:
    OPENAI_URL="https://api.openai.com/v1/chat/completions"

test_txt = [ 
            'hi, my name is jane',
            'I like candy',
            'I like the color blue',
            'please dont be confused',
            'where are we?',
            'if ' + str(TEST_SIX) + ' were ' + str(TEST_NINE)
            ]

prompt_txt = [
        [ 'hi', 'hello' ],
        [ 'what is your name?', 'my name is Jane' ],
        [ 'tell me about yourself', 'i am a student' ],
        [ 'what is your favorite color?', 'i like the color blue' ],
        [ 'how old are you?', 'I am thirty three years old' ],
        [ 'what is your favorite food', 'I like pizza']
            ]

identifiers = { 'user':'user', 'ai':'Jane' }

test_text = [ 'here', 'is', 'some', 'text' ]
test_speech = [ 'here', 'is', 'some', 'text', 'plus' , 'some']

class Kernel:

    def __init__(self):
        self.verbose = False
        self.local = False
        self.remote = False
        self.test = False
        self.truncate = False
        self.loop_wait = False
        self.no_check = False
        self.x_iter = 1 ## start at 1
        self.q = mp.Queue()
        self.prompt = ""
        self.reply = ""
        self.memory_ai = []
        self.memory_user = []
        self.y_iter = 0 

    def loop(self):
        z = True
        x = 0
        rr = []
        tt = "hello."
        skip_say_text = False
        while z == True:
            #if not skip_say_text:
            self.p("ai here")
            if x == 0:
                pass 
                #rr = "say something".split(' ')
            self.empty_queue()
            shadow_say_text = True
            if not self.no_check:
                p = mp.Process(target=self.recognize_audio, args=(shadow_say_text,))
                p.start()
            rr.clear()
            time.sleep(2) 
            self.say_text(tt)
            ## try join here!! remove sleep !!
            if not self.no_check:
                p.join()
                while self.q.qsize() > 0:
                    rx = self.q.get(block=False)
                    self.p('rx', rx)
                    rr.append(rx) 
                self.p(rr)

                if self.is_match(tt.split(' '), rr):
                    self.p('no interruption!')
                    #rr.clear()
                    skip_say_text = False
                else:
                    self.p('interruption!')
                    #sleep_time2 = 0 
                    #rr = self.prune_interrupted(tt.split(' '), rr)
            tt = ""
            rr.clear()
            sleep_time_2 = 1.75 
            self.empty_queue()
            x += 1
            x = x % len(test_txt)
            ### second process ###
            if self.loop_wait:
                num = 0 
                while len(rr) == 0 and num < 100:
                    rr.clear()
                    shadow_say_text = False 
                    #self.recognize_audio(shadow_say_text)
                    p2 = mp.Process(target=self.recognize_audio, args=(shadow_say_text,))
                    p2.start()
                    self.p("start")
                    p2.join()
                    self.p("join")
                    #time.sleep(sleep_time_2)   
                    self.p("len q:", self.q.qsize()) 
                    while not self.q.empty():
                        rx = self.q.get(block=False)
                        self.p('rx2', rx)
                        rr.append(rx)
                    self.p("len q:", self.q.qsize(), 'rr:', len(rr), 'num:', num)
                    num += 1 
            else:
                rr.clear()
                shadow_say_text = False
                self.recognize_audio(shadow_say_text)
                time.sleep(sleep_time_2)   
                self.p("len q:", self.q.qsize()) 
                while not self.q.empty():
                    rx = self.q.get(block=False)
                    self.p('rx2', rx)
                    rr.append(rx)
                self.p("len q:", self.q.qsize(), 'rr:', len(rr) )

            if len(rr) == 0:
                rr = ['say' , 'something,' ]
                #skip_say_text = True

            self.p("ai here ", rr)
            
            self.prompt = self.make_prompt()

            self.modify_prompt_before_model("", ' '.join(rr) )
            
            tt = self.model()

            if self.truncate:
                tt = self.prune_input(tt) # + '.'

            self.p(tt, "<<<", "\n====")
            self.p(self.prompt, "\n=====")
            self.p(self.memory_user, '\n---')
            self.p(self.memory_ai)

            self.modify_prompt_after_model(tt, ' '.join(rr))
            
            rr.clear()

    def list_microphones(self):
        for k, v in enumerate(sr.Microphone.list_microphone_names()):
            print(k, v)
        print("---")
        for k, v in enumerate(sr.Microphone.list_working_microphones()):
            print(k,v)
        print("---")
        print(MICROPHONE_INDEX)

    def recognize_audio(self, shadow_say_text=False):
        if self.test:
            if shadow_say_text:
                return
            ret = input("test input here: ")
            ret = ret.strip()
            self.p("+" + ret + "+")
            for i in ret.split(' '):
                if i.strip() != "":
                    self.q.put(i, block=False)
            return

        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            timeout = 10 
            phrase_time_limit = 5
            #r = sr.Recognizer()
            if not shadow_say_text:
                print("say something!")
            audio = r.listen(source, timeout, phrase_time_limit)
            #audio = r.listen(source)
            self.p("processing.")

        try:
            ret = r.recognize_google(audio)
            self.p("speech recognition: " + ret)
            
            #if True:
            for i in ret.split(' '):
                self.p('sr', i)
                #self.q.put(i)
                self.q.put(i, block=False)
                #self.q.task_done() 
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return

        self.p('iter', self.x_iter)
        self.x_iter += 1
        return

    def say_text(self, txt):
        if self.test:
            self.p(txt)
            return
        if len(txt) == 0:
            return
        tts = gTTS(text=txt, lang='en')
        filename = '.output.mp3'
        tts.save(filename)
        playsound(filename)
        self.p('say this: ', txt)
        pass 

    def is_match(self, text, speech):
        if abs(len(text) - len(speech)) >= 2:
            self.p('len is off:', text, speech)
            return False
        for i in range(len(text)):
            if i < len(text) and i < len(speech):
                t = text[i].lower()[0:2]
                s = speech[i].lower()[0:2]
                #print(t, text[i], s, speech[i])
                if t != s:
                    self.p('individual words dont compare...')
                    return False
        return True

    def empty_queue(self):
        while not self.q.empty():
            self.q.get_nowait()

    def prune_interrupted(self, text, speech):
        output = []
        found = False
        for i in range(len(speech)):
            #print (speech[i])
            found = False
            for ii in range(len(text)):
                #print(text[ii])
                if text[ii] == speech[i]:
                    found = True
                    continue
            if found:
                continue
            else:
                output.append(speech[i])
        #print(output, '<<<')
        return output

    def make_prompt(self):
        ret = ""
        for i in prompt_txt:
            u = i[0]
            a = i[1]
            ret += identifiers['user'] + ": " + u 
            ret += '\n'
            ret += identifiers['ai'] + ": " + a 
            ret += '\n\n'
        if len(self.memory_ai) == len(self.memory_user):
            for i in range(len(self.memory_ai)):
                a = self.memory_ai[i]
                u = self.memory_user[i]
                if len(a) == 0 or len(u) == 0:
                    continue
                ret += identifiers['user'] + ": " + u 
                ret += '\n'
                ret += identifiers['ai'] + ": " + a 
                ret += '\n\n'
        return ret 

    def modify_prompt_before_model(self, tt, rr):
        self.prompt += identifiers['user'] + ': ' + rr + "\n" 
        self.prompt += identifiers['ai'] + ': '

    def modify_prompt_after_model(self, tt, rr):
        self.memory_user.append(rr)
        self.memory_ai.append(tt) ## <-- temporary...
        pass 

    def prune_input(self, text):
        self.p(text, '<<< unmodified')
        text = text.split('?')[0]
        text = text.split('.')[0]
        text = text.split('!')[0]
        return text

    def model(self):
        z_args = {
            "Authorization" : "Bearer " + OPENAI_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "model" : OPENAI_MODEL,
            "messages": [{'role': 'user', 'content': self.prompt }],
            "temperature": 0.01
        }
        r = requests.post(OPENAI_URL, headers=z_args, json=data)
        r = json.loads(r.text)
        self.reply = r['choices'][0]['message']['content']
        self.p(self.reply)
        
        return self.reply

    def p(self, *text):
        if self.verbose:
            print(*text)

if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--local', action="store_true", help="Not implemented")
    parser.add_argument('--verbose', action="store_true", help="Use verbose mode.")
    parser.add_argument('--test', action="store_true", help="Use test data and no LLM")
    parser.add_argument('--truncate', action="store_true", help="truncate model output.")
    parser.add_argument('--loop_wait', action="store_true", help="loop until input is detected.")
    parser.add_argument('--no_check', action="store_true", help="cancel interruption check.")
    ## NOTE: local is not implemented!! 

    args = parser.parse_args()
    
    if args.local == True:
        k.local = True
        k.remote = False
        k.test = True

    if args.truncate == True:
        k.truncate = True

    k.test = args.test
    k.verbose = args.verbose
    k.loop_wait = args.loop_wait
    k.no_check = args.no_check

    k.loop()


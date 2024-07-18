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

try:
    GOOGLE_SPEECH_RECOGNITION_API_KEY=str(vals['GOOGLE_SPEECH_RECOGNITION_API_KEY'])
except:
    GOOGLE_SPEECH_RECOGNITION_API_KEY=None

try:
    PROJECT_LAUNCH_ARGS=str(vals['PROJECT_LAUNCH_ARGS'])
except:
    PROJECT_LAUNCH_ARGS='' #'--no_check'


prompt_txt = [
        [ 'hi', 'hello' ],
        [ 'what is your last name?', 'my last name is Smith' ],
        [ 'tell me about yourself', 'i am a student' ],
        [ 'what is your favorite color?', 'i like the color blue' ],
        [ 'how old are you?', 'I am thirty three years old' ],
        [ 'what is your favorite food', 'I like pizza']
            ]

identifiers = { 'user':'user', 'ai':'Jane' }


class Kernel:

    def __init__(self):
        self.verbose = False
        self.local = False
        self.remote = False
        self.test = False
        self.truncate = False
        self.loop_wait = False
        self.no_check = False
        self.offset = 0.0
        self.file = False
        self.file_num = 0
        self.temp = 0.001
        self.timeout = 3.0 
        self.window = 35 
        self.x_iter = 1 ## start at 1
        self.q = mp.Queue()
        self.prompt = ""
        self.reply = ""
        self.memory_ai = []
        self.memory_user = []
        self.y_iter = 0 

    def loop(self):
        time.sleep(self.offset)
        z = True
        x = 0
        rr = []
        start = time.time()
        end = time.time()
        tt = "hello."
        skip_say_text = False
        while z == True:
            self.p("ai here")
            if x == 0:
                ## not used ##
                pass 
            self.empty_queue()
            shadow_say_text = True
            if not self.no_check:
                p = mp.Process(target=self.recognize_audio, args=(shadow_say_text,))
                p.start()
                time.sleep(2)
            rr.clear()
            #time.sleep(2) 
            self.say_text(tt)
            ## try join here!! remove sleep !!
            if not self.no_check:
                p.join()
                while self.q.qsize() > 0:
                    rx = self.q.get(block=False)
                    self.p('rx', rx)
                    rr.append(rx) 
                self.p(rr)

                ## does nothing !! ##
                if self.is_match(tt.split(' '), rr) or rr == []:
                    self.p('no interruption!')
                else:
                    self.p('interruption!')
                    self.save_file(0, '---\ninterruption\n---')
            tt = ""
            #rr.clear() ## <-- keep or not keep??
            sleep_time_2 = 1.75 
            self.empty_queue()
            x += 1
            x = x % len(prompt_txt)
            ### second process ###
            if self.loop_wait:
                num = 0 
                high = 1000
                start = time.time()
                while num < high:
                    rr.clear()
                    shadow_say_text = False
                    self.p("say something.")
                    self.recognize_audio(shadow_say_text)
                    end = time.time()
                    self.p("len q:", self.q.qsize(), 'rr:', len(rr), 'num:', num, 'elapsed:', end - start)
                    if self.q.qsize() > 0:
                        break 
                    if (end - start)  > self.timeout * 60:
                        self.p("elapsed:", (end - start), 'timeout:', self.timeout * 60 )
                        rr = ['say', 'something']
                        break
                    if num == high - 1 :
                        rr = [ 'say', 'something' ]
                        break
                    num += 1 
                ###############
                self.p("len q:", self.q.qsize())
                #using_thread = not self.no_check
                while self.q.qsize() > 0:
                    rx = self.q.get(block=True) ## don't really know <--
                    self.p('rx2', rx)
                    rr.append(rx)
                end = time.time()
                self.p("len q:", self.q.qsize(), 'rr:', len(rr), 'num:', num, 'elapsed:', end - start)

            else:
                rr.clear()
                shadow_say_text = False
                self.p("say something.")
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

            self.save_file(  end - start )
            rr.clear()

    def list_microphones(self):
        for k, v in enumerate(sr.Microphone.list_microphone_names()):
            print(k, v)
        print("---")
        return
        '''
        for k, v in enumerate(sr.Microphone.list_working_microphones()):
            print(k,v)
        print("---")
        print(MICROPHONE_INDEX)
        '''
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
        
        if MICROPHONE_INDEX != -1:
            mic = sr.Microphone(device_index=MICROPHONE_INDEX)
        else:
            mic = sr.Microphone()

        with mic as source:
            timeout = 10 
            phrase_time_limit = 5
            #r = sr.Recognizer()
            audio = r.listen(source) #, timeout=timeout) #, phrase_time_limit)
            self.p("processing.")

        try:
            #self.p(GOOGLE_SPEECH_RECOGNITION_API_KEY)
            ret = r.recognize_google(audio) #,  key=GOOGLE_SPEECH_RECOGNITION_API_KEY)
            self.p("speech recognition: " + ret)
            
            #if True:
            for i in ret.split(' '):
                self.p('sr', i)
                #self.q.put(i)
                self.q.put(i, block=False)
                #self.q.task_done() 
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            #self.empty_queue()
            return 
        except sr.RequestError as e:
            #self.empty_queue()
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
        for i in range(len(prompt_txt) + len(self.memory_ai) - self.window, len(prompt_txt)):
            if i < 0:
                continue
            u = prompt_txt[i][0]
            a = prompt_txt[i][1]
            ret += identifiers['user'] + ": " + u 
            ret += '\n'
            ret += identifiers['ai'] + ": " + a 
            ret += '\n\n'
        if len(self.memory_ai) == len(self.memory_user):
            for i in range(len(self.memory_ai) - self.window ,len(self.memory_ai)):
                if i < 0:
                    continue
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
            "temperature": self.temp
        }
        r = requests.post(OPENAI_URL, headers=z_args, json=data)
        r = json.loads(r.text)
        self.reply = r['choices'][0]['message']['content']
        self.p(self.reply)
        
        return self.reply

    def p(self, *text):
        if self.verbose:
            print(*text)

    def save_file(self,  time, heading=""):
        if self.file:
            f = open(os.path.expanduser('~') + '/llm.txt', 'a')
            
            if heading.strip() != "":
                f.write(str(heading) + '\n')
                f.close()
                return

            f.write(str(self.file_num) + '\n')
            #for i in range(len(self.memory_user) -1, len(self.memory_user)):
                
            f.write(identifiers['user'] + " : "+ str(self.memory_user[-1]) + "\n")
            f.write(identifiers['ai'] + " : " + str(self.memory_ai[-1]) + "\n")
            #f.write(str(prompt) + "\n")
            if self.loop_wait:
                f.write("---\n")
                f.write(str(time) + "\n")
            f.write("+++\n")

            f.close()
            self.file_num += 1
        pass 

if __name__ == '__main__':
    k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--local', action="store_true", help="Not implemented")
    parser.add_argument('--verbose', action="store_true", help="Use verbose mode.")
    parser.add_argument('--test', action="store_true", help="Use test data and no LLM")
    parser.add_argument('--truncate', action="store_true", help="truncate model output.")
    parser.add_argument('--loop_wait', action="store_true", help="loop until input is detected.")
    parser.add_argument('--no_check', action="store_true", help="cancel interruption check.")
    parser.add_argument('--name', type=str, help="define new name.")
    parser.add_argument('--offset', type=float, help="time in seconds to offset on startup.")
    parser.add_argument('--mics', action="store_true", help="display microphone data and quit.")
    parser.add_argument('--file', action="store_true", help="save statistics in text file.")
    parser.add_argument('--temp', type=float, default=0.001, help="temperature for LLM operation.")
    parser.add_argument('--timeout', type=float, default=3.0, help="minutes to timeout.")
    parser.add_argument('--window', type=int, default=35, help="number of memory units used in input.")
    ## NOTE: local is not implemented!! 
    
    args = parser.parse_args()
    if len(PROJECT_LAUNCH_ARGS.strip()) > 0:
        print(PROJECT_LAUNCH_ARGS.strip())
        args = parser.parse_args(PROJECT_LAUNCH_ARGS.strip().split(" "))
    #parser.parse_args(PROJECT_LAUNCH_ARGS.split(" "))
   
    print(args)
    if args.mics == True:
        k.list_microphones()
        exit()

    if args.offset != None and args.offset != 0.0:
        k.offset = args.offset

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

    if args.name != None and args.name.strip() != "":
        identifiers['ai'] = args.name.strip()

    if args.file != None:
        k.file = args.file 

    if args.temp != 0:
        k.temp = args.temp

    if args.timeout != 0:
        k.timeout = args.timeout
    
    if args.window != 0:
        k.window = args.window

    k.save_file(0, str(args))

    k.loop()


#!/usr/bin/env python3

import argparse
from dotenv import  dotenv_values 
import os
import speech_recognition as sr
from gtts import gTTS 
from playsound import playsound
import multiprocessing as mp 
import time

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

test_txt = [ 
            'hi, my name is jane',
            'I like candy',
            'I like the color blue',
            'please dont be confused',
            'where are we?',
            'if ' + str(TEST_SIX) + ' were ' + str(TEST_NINE)
            ]


class Kernel:

    def __init__(self):
        self.verbose = True
        self.local = False
        self.remote = False
        self.test = False
        self.x_iter = 1 ## start at 1
        self.q = mp.Queue()

    def loop(self):
        z = True
        x = 0 
        while z == True:
            print("ai here")
            tt = test_txt[x]
            self.q = mp.Queue()
            p = mp.Process(target=self.recognize_audio)
            p.start()
            rr = []
            time.sleep(2) 
            self.say_text(tt)
            sleep_time = 0.75 * len(tt.split(" ")) 
            print(sleep_time)
            time.sleep(sleep_time)

            while not self.q.empty():
                rx = self.q.get()
                print('rx', rx)
                rr += [rx] 
            print(rr)
            ## kill here ##
            p.kill()
            #p.close()
            #p.kill()
            if self.is_match(tt.split(' '), rr):
                print( 'no interruption!' )
                rr = []
                self.q = mp.Queue()
            else:
                print( 'interruption!' )
            x += 1
            x = x % len(test_txt)
            ### second process ###
               
            #time.sleep(5)

            self.recognize_audio()
            
            while not self.q.empty():
                rx = self.q.get()
                print('rx2', rx)
                rr += [rx]
            
            print("ai here")

    def list_microphones(self):
        for k, v in enumerate(sr.Microphone.list_microphone_names()):
            print(k, v)
        print("---")
        for k, v in enumerate(sr.Microphone.list_working_microphones()):
            print(k,v)
        print("---")
        print(MICROPHONE_INDEX)

    def recognize_audio(self):

        #self.list_microphones()
        r = sr.Recognizer()
        #self.r.energy_threshold = 100
        
        with sr.Microphone() as source:
            #r = sr.Recognizer()
            print("Say something!")
            audio = r.listen(source)
            #audio = r.listen(source)
            print("processing.")

        try:
            ret = r.recognize_google(audio)
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("speech recognition: " + ret)
            
            for i in ret.split(' '):
                print('sr', i)
                self.q.put(i)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        print('iter', self.x_iter)
        self.x_iter += 1
        return

    def say_text(self, txt):
        tts = gTTS(text=txt, lang='en')
        filename = '.output.mp3'
        tts.save(filename)
        playsound(filename)
        print('say this: ', txt)
        pass 

    def is_match(self, text, speech):
        if abs(len(text) - len(speech)) >= 1:
            print('len is off:', text, speech)
            return False
        for i in range(len(text)):
            if i < len(text) and i < len(speech):
                t = text[i].lower()[0:2]
                s = speech[i].lower()[0:2]
                #print(t, text[i], s, speech[i])
                if t != s:
                    print('individual words dont compare...')
                    return False
        return True

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


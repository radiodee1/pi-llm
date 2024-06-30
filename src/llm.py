#!/usr/bin/env python3

import argparse
from dotenv import  dotenv_values 
import os
import speech_recognition as sr
from gtts import gTTS 
from playsound import playsound

vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    TEST_SIX=int(vals['TEST_SIX']) 
except:
    TEST_SIX = 8 # 32 

try:
    TEST_NINE=int(vals['TEST_NINE']) 
except:
    TEST_NINE = 16

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
        #self.engine = pyttsx3.init()

    def loop(self):
        z = True
        x = 0 
        while z == True:
            print(test_txt[x])
            t = self.separate_words(test_txt[x])
            r = self.recognize_audio()
            print(t, r)
            self.say_text(t[0])
            x += 1
            x = x % len(test_txt)
            g = input("say something (stop to quit) >> ")
            if g == "stop":
                z = False
        print("here")

    def separate_words(self, line):
        return line.split(" ")

    def recognize_audio(self):

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            ret = r.recognize_google(audio)
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + ret)
            return ret 
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def say_text(self, txt):
        tts = gTTS(text=txt, lang='en')
        filename = '.output.mp3'
        tts.save(filename)
        playsound(filename)
        #os.system(f'start {filename}')
        pass 

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


#!/usr/bin/env python3

import argparse
from math import floor
import string
import sys
from types import NoneType
from wave import Error
from dotenv import  dotenv_values 
import os
from google.auth import default
import speech_recognition as sr
from gtts import gTTS 
from google.cloud import texttospeech

from playsound import playsound
import multiprocessing as mp 
import time
import requests
import json
#import hashlib

import review
import stt 
import prompt

identifiers = { 'user':'user', 'ai':'jane', 'mem': 'storage' }

voice_gender = { 'male': 'en-US-Neural2-D', 'female': 'en-US-Neural2-F' }

wake = [ 'hello', 'wake', 'wakeup' ]

class Kernel:

    def __init__(self, user_dir):
        self.verbose = False
        self.local = False
        self.remote = False
        self.test = False
        self.truncate = False
        self.loop_wait = False
        self.loop_wait_saved = False
        self.no_check = False
        self.offset = 0.0
        self.file = False
        self.file_num = 0
        self.temp = 0.001
        self.timeout = 3.0 
        self.window = 35
        self.acceptable_pause = 15 
        self.window_mem = 0 
        self.window_chat = 0 
        self.window_ratio = 1.0 / 2.0 
        self.window_mem_ratio = 1 
        self.window_line_count = 0 
        self.size_trim = 0 ## number of lines to trim from prompt. Always increasing.
        self.size_goal = 0 ## number of TOKENS inside context-area to use. User input.
        self.size_const = 5 ## number_of_lines to pad in context-area. Magic number.
        self.cloud_stt = False
        self.cloud_tts = False
        self.json = False
        self.mic_timeout = -1 
        self.voice = ""
        self.x_iter = 1 ## start at 1
        self.q = mp.Queue()
        self.prompt = ""
        self.reply = ""
        #self.memory_ai = []
        #self.memory_user = []
        self.y_iter = 0 
        self.questions = -1
        self.questions_list = []
        self.questions_num = 0
        self.checkpoint_num = 0 
        self.pc = False
        self.gemini = False
        self.review = False
        self.review_skip = -1 
        self.review_skip_high = 1 
        self.review_just_skipped = False
        self.test_review = -1
        self.tokens_recent = 0
        self.recognize_audio_error = False
        self.wake_words = []
        self.sleep_wake = False
        self.sleep = False 
        self.user_dir = user_dir
        self.m = None 

        if self.user_dir.strip() == '':
            self.user_dir = os.path.expanduser('~')
        vals = dotenv_values(self.user_dir + "/.llm.env")

        try:
            self.TEST_SIX=int(vals['TEST_SIX']) 
        except:
            self.TEST_SIX = 8 # 32 

        try:
            self.TEST_NINE=int(vals['TEST_NINE']) 
        except:
            self.TEST_NINE = 16

        try:
            self.MICROPHONE_INDEX=int(vals['MICROPHONE_INDEX'])
        except:
            self.MICROPHONE_INDEX=-1

        try:
            self.OPENAI_API_KEY=str(vals['OPENAI_API_KEY'])
        except:
            self.OPENAI_API_KEY='abc'

        try:
            self.OPENAI_ORGANIZATION=str(vals['OPENAI_ORGANIZATION'])
        except:
            self.OPENAI_ORGANIZATION=""

        try:
            self.OPENAI_PROJECT_ID=str(vals['OPENAI_PROJECT_ID'])
        except:
            self.OPENAI_PROJECT_ID=""

        try:
            self.OPENAI_MODEL=str(vals['OPENAI_MODEL'])
        except:
            self.OPENAI_MODEL="gpt-3.5-turbo"

        try:
            self.OPENAI_URL=str(vals['OPENAI_URL'])
        except:
            self.OPENAI_URL="https://api.openai.com/v1/chat/completions"

        try:
            self.OPENAI_EMBEDDING_URL=str(vals['OPENAI_EMBEDDING_URL'])
        except:
            self.OPENAI_EMBEDDING_URL="https://api.openai.com/v1/embeddings"

        try:
            self.OPENAI_EMBEDDING_NAME=str(vals['OPENAI_EMBEDDING_NAME'])
        except:
            self.OPENAI_EMBEDDING_NAME="text-embedding-3-large"


        try:
            self.OPENAI_CHECKPOINTS=str(vals['OPENAI_CHECKPOINTS'])
        except:
            self.OPENAI_CHECKPOINTS=""

        try:
            self.GOOGLE_SPEECH_RECOGNITION_API_KEY=str(vals['GOOGLE_SPEECH_RECOGNITION_API_KEY'])
        except:
            self.GOOGLE_SPEECH_RECOGNITION_API_KEY=None

        try:
            self.PROJECT_LAUNCH_ARGS=str(vals['PROJECT_LAUNCH_ARGS'])
        except:
            self.PROJECT_LAUNCH_ARGS='' #'--no_check'

        self.GOOGLE_CLOUD_SPEECH_CREDENTIALS=''

        try:
            self.PROJECT_REVIEW_NAME=str(vals['PROJECT_REVIEW_NAME'])
        except:
            self.PROJECT_REVIEW_NAME='.llm.review.txt'

        try:
            self.PROJECT_PROMPT_ORDER=str(vals['PROJECT_PROMPT_ORDER'])
        except:
            self.PROJECT_PROMPT_ORDER="INSTRUCTIONS:RULES:REVIEW:../files/combined.txt:../files/conversation.txt:MEMORY"

        try:
            self.GOOGLE_APPLICATION_CREDENTIALS=str(vals['GOOGLE_APPLICATION_CREDENTIALS'])
        except:
            self.GOOGLE_APPLICATION_CREDENTIALS=''

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.GOOGLE_APPLICATION_CREDENTIALS

        try:
            self.GOOGLE_GEMINI_URL=(vals['GOOGLE_GEMINI_URL'])
        except:
            self.GOOGLE_GEMINI_URL='https://generativelanguage.googleapis.com/v1beta/models/'

        try:
            self.GOOGLE_GEMINI_API_KEY=(vals['GOOGLE_GEMINI_API_KEY'])
        except:
            self.GOOGLE_GEMINI_API_KEY=''

        try:
            self.GOOGLE_GEMINI_MODEL=(vals['GOOGLE_GEMINI_MODEL'])
        except:
            self.GOOGLE_GEMINI_MODEL='gemini-2.0-flash'


    def loop(self):
        if self.review:
            review.set_user_dir(self.user_dir)
        if self.cloud_stt:
            stt.set_user_dir(self.user_dir)

        time.sleep(self.offset)
        z = True
        x = 0
        rr = []
        start = time.time()
        end = time.time()
        tt = "hello."
        # skip_say_text = False
        while z == True:
            self.p("ai here")
            self.empty_queue()
            #shadow_say_text = True
            if (not self.review_skip >= 0) and (self.questions == -1):
                rr.clear()
            self.say_text(tt)
            if (self.needs_restart()):
                return 
            ## try join here!! remove sleep !!
            tt = ""
            self.empty_queue()
            x += 1
            x = x % (self.m.get_size_by_name('conversation') // 2 )# len(prompt_txt)
            ### second process ###
            if self.loop_wait and self.questions == -1 :
                num = 0 
                high = 1000
                start = time.time()
                basetime = start 
                wake_word_found = False
                while num < high:
                    if int(self.review_skip) < 0 and (not self.test):
                        pass 
                        rr.clear()
                    #shadow_say_text = False
                    self.p("say something in loop-wait.")
                    self.recognize_audio()
                    end = time.time()
                    if self.q.qsize() > 0 or self.recognize_audio_error:
                        break 
                    if (end - start)  > self.timeout * 60 :
                        self.p("elapsed:", (end - start), 'timeout:', self.timeout * 60 )
                        #rr = ['say', 'something']
                        rr = self.long_pause_statement(not int(self.questions) > -1, (end - start))
                        break
                    if num == high - 1  :
                        #rr = [ 'say', 'something' ]
                        rr = self.long_pause_statement(not int(self.questions) > -1, (end - start))
                        break
                    num += 1 
                ###############
                while self.q.qsize() > 0 and self.review_skip < 0:
                    rx = self.q.get(block=True) ## <--
                    if rx.strip() != '':
                        if (self.find_wake_word(rx.strip())):
                            wake_word_found = True
                        rr.append(rx.strip())
                end = time.time()
                if ((not wake_word_found) and (end - basetime)  > self.acceptable_pause):# and end - start > self.acceptable_pause:
                    self.p('not wake_word_found in loop-wait', num )
                    #rr.clear()
                    continue
                else:
                    self.p('wake_word_found in loop-wait', num)
                    num = 0 
                    basetime = end

            else : #if self.questions:
                if (not self.review_skip >= 0): # or self.questions == -1:
                    rr.clear() ## DO THIS??
                    #self.p('clear here...')
                    pass 
                if self.questions > -1:
                    self.empty_queue()
                    #rr.clear()
                   
                self.p("len q:", self.q.qsize(), 'say something outside loop-wait.')

                use_block =  self.questions > -1   or  self.cloud_stt
                self.p(use_block, 'use_block')
                if self.review_skip < 0 :
                    #self.empty_queue()
                    self.recognize_audio()
                    self.p('after recognize_audio')
                    while ( self.q.qsize() > 0 ): 
                        rx = self.q.get(block=use_block) ## False usually !!
                        if rx.strip() != '':
                            self.p('c-rr', rx)
                            rr.append(rx.strip())

                if len(rr) == 0 and self.questions == -1:
                    #rr = ['say' , 'something' ]
                    end = time.time()
                    rr = self.long_pause_statement(False, (end - start))
                    #skip_say_text = True

            if self.review:
                review.read_review(self.window_mem)

            self.resize_prompt() ## <-- redo

            #self.prompt = self.make_prompt()
            self.make_prompt()

            self.modify_prompt_before_model("", ' '.join(rr) )
            
            tt = self.model()
            
            tt = self.review_vars(tt)

            tt = self.prune_input(tt) # + '.'

            self.modify_prompt_after_model(tt, ' '.join(rr))

            self.p("====\n", self.prompt, "\n====")

            self.save_file(  end - start )

            if int(self.questions) > -1:
                self.questions_num += 1 
                if self.questions_num >= int(self.questions): # len(self.questions_list):
                    return 

    def review_vars(self, tt):
        if self.test and self.review_skip == -1:
            tt = 'reply to question ' + str(self.questions_num)
            
        if self.review:
            if int(self.test_review) != -1:
                tt = tt.replace(review.ADD_TEXT, '')
                tt = tt.replace(review.REM_TEXT, '')
                for i in identifiers.values():
                    tt = tt.replace(i, '')
                if self.questions_num == int(self.test_review):
                    tt = tt + " " + review.ADD_TEXT 
                self.p(tt)
            review.find_marked_text(self.m.pc_output(), [], tt, identifiers)
            skip = review.is_skipable(tt, identifiers)
            tt = review._return_without_name(tt)

            #self.p('1>>>', tt, skip, self.review_skip, self.test_review, self.questions_num)
            
            if self.review_skip >= 0: ## countdown maintenence
                self.review_skip = -1 # -= 1 #  -= 1
                if self.review_skip == -1:
                    self.loop_wait = self.loop_wait_saved
                self.p('<<<1')
            elif (self.review_skip < 0 and skip): #  start skipping 
                self.review_skip = self.review_skip_high ## magic number 1?? 
                self.loop_wait = False
                self.p('<<<2')

            self.p('1>>>', tt, skip, self.review_skip, self.test_review, self.questions_num)
        return tt 

    def list_microphones(self):
        for k, v in enumerate(sr.Microphone.list_microphone_names()):
            if k - 1 >= 0:
                print(k - 1, v)
        print("---")
        return

    def recognize_audio(self ):
        
        if self.review and self.review_skip >= 0:
            return

        self.recognize_audio_error = False

        if int(self.questions) > -1:
            self.p(self.questions_num, self.questions_num % len(self.questions_list), len(self.questions_list))
            ret = self.questions_list[self.questions_num % len(self.questions_list)]
            ret = ret.strip()
            self.p(ret, '<---', self.questions, self.questions_num)
            self.empty_queue()
            for i in ret.split(' '):
                if i.strip() != "":
                    self.q.put(i, block=True)
            time.sleep(2)
            return
        
        if self.cloud_stt:
            stt.time_start = 0 
            stt.time_last_output = 0 
            stt.time_end = 0
            stt.counted_responses = 0 
            stt.starting_timeout = -1
            stt.overall_timeout = self.mic_timeout
            stt.wake_words = self.wake_words
            stt.sleep = self.sleep
            x = stt.main()
            ret = x.strip().strip(',')
            self.empty_queue()
            for i in ret.split(' '):
                if i.strip() != "":
                    self.p('d-rr', i)
                    #self.q.put(i)
                    self.q.put(i.strip(), block=True)
                #self.q.task_done()
            self.sleep = self.sleep_wake 
            return 


        r = sr.Recognizer()
        
        if self.MICROPHONE_INDEX != -1:
            mic = sr.Microphone(device_index=self.MICROPHONE_INDEX)
        else:
            mic = sr.Microphone()
        
        
        try:
            with mic as source:
                timeout = self.mic_timeout 
                phrase_time_limit = self.mic_timeout
                #r = sr.Recognizer()
                if self.mic_timeout != -1:
                    try:
                        audio = r.listen(source , timeout=timeout , phrase_time_limit=phrase_time_limit)
                        self.p("processing with timeout") 
                    except Exception as e:
                        self.p("an exception occured")
                        if e == KeyboardInterrupt:
                            exit()
                        return
                        
                else:
                    audio = r.listen(source)
                self.p("processing.")

        except AttributeError:
            self.p('attribute error - mic is NoneType??')
            self.empty_queue()
            self.recognize_audio_error = True
            self.x_iter += 1 
            return
        

        try:
            ret = ''
            #self.p(GOOGLE_SPEECH_RECOGNITION_API_KEY)
            if self.cloud_stt == False:
                ret = r.recognize_google(audio) 
            #elif self.cloud_stt == True:
            #    ret = str(r.recognize_google_cloud(audio, self.GOOGLE_APPLICATION_CREDENTIALS))

            self.p("speech recognition: " + ret)
            
            #if True:
            for i in ret.split(' '):
                if i.strip() != "":
                    self.p('d-rr', i)
                    #self.q.put(i)
                    self.q.put(i.strip(), block=True)
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

        if int(self.questions) > -1:
            self.p(txt, '- questions mode')
            return
        if len(txt) == 0:
            return
        if self.review and self.review_skip >= 0:
            #if  review.REM_TEXT in txt:
            return
            #return

        filename =  '.output.mp3'

        if not self.cloud_tts:
            tts = gTTS(text=txt, lang='en')
            tts.save(filename)

        if self.cloud_tts:
            client = texttospeech.TextToSpeechClient()
            
            if txt == None or txt.strip() == "":
                return
            
            try:
                synthesis_input = texttospeech.SynthesisInput(text=txt)

                voice = texttospeech.VoiceSelectionParams( 
                    name=self.voice, language_code="en-US" 
                )

                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )

                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

            except  Error as e:
                print('speech to text error', e)
                return 

            with open(filename, "wb") as out:
                # Write the response to the output file.
                out.write(response.audio_content)
                print('Audio content written to file "' + filename + '"')        

            pass 

        playsound(filename)
        self.p('say this: ', txt)
        pass 


    def empty_queue(self):
        while not self.q.empty():
            #self.q.get_nowait()
            self.q.get(block=True)


    def find_wake_word(self, text):
        text = text.strip().lower()
        if text in identifiers.values():
            return True
        else:
            return False

    def long_pause_statement(self, show, time):
        time = floor(time)
        a = [ 'say', 'something' ]
        b = [ 'long', 'pause', str(time) , 'sec' ]
        if show and time > 0 :
            return b
        return a 

    def resize_prompt(self):
        if self.window_line_count > self.tokens_recent or self.review_skip != -1:
            return
        if self.window_line_count == 0:
            self.window_line_count =  self.m.get_size_by_name('conversation') ##len(prompt_txt) * 2  
        line_size = self.tokens_recent / self.window_line_count 
        can_trim = False
        ## set size of self.window_chat here.
        if self.window <= 0:
            self.window_chat = len(self.prompt) - floor(self.window_ratio * self.size_trim) 
            self.window_mem = floor( (self.window_chat * self.window_mem_ratio) / self.window_ratio)
            self.p('window_mem', self.window_mem)
        ## set size of self.size_trim here.
        if self.window <= 0 and self.tokens_recent > self.size_goal:
            number_of_lines = (self.size_goal - (line_size * self.size_const)) / line_size
            if self.size_trim + floor(number_of_lines) < self.window_line_count :
                self.size_trim += floor(number_of_lines)
                can_trim = True
        self.p("++++ tokens:", self.tokens_recent,'line_count:', self.window_line_count , 'size_trim:', self.size_trim, 'can_trim:', can_trim, "++++")
        return

    def make_prompt(self):
        #self.window_line_count = 0 
        rule_instruct = ['You are a ficticious person named ' + identifiers['ai'] + '. Use your imagination to answer all questions in English.' ]
        
        index = self.m.get_index_from_name('RULES')
        self.p(index, 'index')
        self.m.replace_list([], index)
        self.m.set_hide_from_name('RULES')

        index = self.m.get_index_from_name('INSTRUCTIONS')
        self.p(index, 'index2')
        self.m.replace_list(rule_instruct, index)
        self.m.set_show_from_name('INSTRUCTIONS')
 
        if self.review and self.review_skip == -1:
            instructions = str(' Say anything with the "' + review.ADD_TEXT + '" characters as a flag to save any marked sentence permanently. Use your intuition to mark sentences. ' +
                ' Repeat anything out loud with the "' + review.REM_TEXT + '" characters as a flag to delete any marked sentence from the memory list permanently.')

            index = self.m.get_index_from_name('RULES')
            self.m.replace_list([ instructions ], index)
            self.m.set_show_from_name('RULES')
            
        if self.review: ## ???
            index = self.m.get_index_from_name('REVIEW')
            self.m.replace_list( review.memory_review, index )
            self.m.set_show_from_name('REVIEW')
            
        return

    def modify_prompt_before_model(self, tt, rr):
        if self.review and self.review_skip >= 0:
            #return
            pass 
        self.m.shrink(self.size_trim)

        if self.json:
            if not self.gemini:
                self.prompt = self.m.json_output(rr)

            if self.gemini:
                self.prompt = json.dumps(self.m.json_output(rr))
            return
        if self.pc:

            self.prompt = self.m.pc_output(rr)
            return
        self.prompt = self.m.output(rr)

    def modify_prompt_after_model(self, tt, rr):
        if self.review and self.review_skip >= 0:
            return
        if 'time' in tt or 'time' in rr:
            #return
            pass 
        self.m.add_pair([rr, tt])
        pass 

    def prune_input(self, text):
        if self.test:
            return text

        self.p(text, '<<< unmodified')
        if self.gemini and self.json:
            text = text['content'].strip()

        if self.json:
            t = text.strip().split(':')
            if self.review:
                if review.ADD_TEXT in t[0] and len(t) > 1:
                    t[0] = t[0].replace(review.ADD_TEXT, '')
                    t[1] += review.ADD_TEXT
                if review.REM_TEXT in t[0] and len(t) > 1:
                    t[0] = t[0].replace(review.REM_TEXT, '')
                    t[1] += review.REM_TEXT

            if len(t) > 1 and t[0].strip() in identifiers.values():
                text = ':'.join(t[1:])
            if len(t) == 1 and t[0].strip() in identifiers.values():
                text = 'pause'
        #text = text.replace(':', ' ')
        #text = text.replace('-', ' ')
        text = text.replace(';', ' ')
        text = text.replace('"', '')
        text = text.replace("'", '')
        text = text.replace("?", '.')
        text = text.replace("!", '.')
        text = text.replace("\n", '')
        if ':' in text:
            t = text.strip().split(':')
            if (len(t) == 2 or t[0].strip() in [identifiers['mem']]) and self.review:
                text += review.REM_TEXT #' '.join(t[1:])
            elif len(t) == 2 and t[0].strip() in identifiers.values():
                text = ':'.join(t[1:])


        if '\n' in text:
            text = text.split('\n')[0]
        if self.truncate:
            old_text = text
            text = old_text.split('.')[0]
            if len(text.strip().split(' ')) == 1 and len(old_text.strip().split('.')) > 1:
                pass 
                text = old_text.split('.')[0].strip() + '. ' + old_text.split('.')[1].strip()
        return text

    def model(self):
        if self.review_skip > -1 and not self.test:
            #return ''
            pass 
        if self.test:
            self.reply = 'reply to question ' + str(self.questions_num)
            return self.reply

        url = self.OPENAI_URL
        z_args = {
            "Authorization" : "Bearer " + self.OPENAI_API_KEY,
            "Content-Type": "application/json"
        }
        data = {}

        if not self.json:
            data = {
                "model" : self.OPENAI_MODEL,
                "messages": [{'role': 'user', 'content': self.prompt }],
                "temperature": self.temp
            }
        if self.json:
            data = {
                "model" : self.OPENAI_MODEL,
                "messages":   self.prompt  ,
                "temperature" : self.temp
            }
        
        if self.pc:
            model = self.OPENAI_MODEL
            if 'chat' in url:
                url = url.replace('chat/', '')
            #prompt_txt =  json.dumps(self.prompt)
            #prompt_txt = ' '.join( x for x in prompt_txt) #.split('\n') )
            data = {
                "model" : model,
                "prompt": self.prompt,
                "temperature" : self.temp
            }

        if self.gemini:
            url = self.GOOGLE_GEMINI_URL.strip() + self.GOOGLE_GEMINI_MODEL.strip() + ':generateContent?key=' + self.GOOGLE_GEMINI_API_KEY.strip()
            z_args = {
                "Content-Type": "application/json"
            }
            data = {
                "contents": [{
                    "parts":[{
                        "text": self.prompt
                    }]
                }]
                ##
                ,
                'generationConfig': {
                    'temperature': self.temp
                }
                ##
            }

        r = requests.post(url, headers=z_args, json=data)
       
        if self.gemini:

            if r.status_code == 200:
                self.p("Response received successfully:")
                self.reply = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                self.p(self.reply)
                if self.json:
                    
                    count = self.reply.count('"')
                    if count == 8: ## magic number 
                        self.reply = json.loads(self.reply)

                try:
                    self.tokens_recent = r.json()["usageMetadata"]['totalTokenCount']
                except:
                    self.tokens_recent = 0 

            else:
                self.p(f"Error: {r.status_code}")
                self.p(r.text)

            return self.reply

        self.p(r.text)
        r = json.loads(r.text)
        self.p(r)
 

        try:
            self.reply = r['choices'][0]['message']['content']
        except:
            self.reply = ""
        
        try:
            self.tokens_recent = r['usage']['total_tokens']
        except:
            self.tokens_recent = 0 

        if self.pc:
            try:
                self.reply = r['choices'][0]['text']
            except:
                self.reply = ""

        self.p(self.reply)
        
        return self.reply

    def count_tokens(self, txt):
        r = ""
        try:
            if type(txt) != 'str':
                txt = json.dumps(txt)

            url = self.OPENAI_EMBEDDING_URL 
            headers = {
                "Authorization" : "Bearer " + self.OPENAI_API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "input" : txt,
                "model" : self.OPENAI_EMBEDDING_NAME 
            }
            # self.p(url, headers, data)
            r = requests.post(url, headers=headers, json=data)
            r = json.loads(r.text)
            # self.p(r)
            num = r['usage']['total_tokens']
            num = int(num)
        except Exception as e:
            print(r)
            print(e)
            num = -1
        return num


    def p(self, *text):
        if self.verbose:
            print(*text)

    def save_file(self,  time, heading=""):
        if self.file:

            if self.review and self.review_skip >= 0:
                return
                pass 
            name = '/llm.'
            if int(self.questions) > -1:
                num = ('0000' + str(self.checkpoint_num ))[-3:]
                name += 'CHECKPOINT_' + num + '.'
            
            try:
                file = self.OPENAI_MODEL.strip()
                if self.gemini:
                    file = self.GOOGLE_GEMINI_MODEL.strip()

                f = open(self.user_dir + name + file +'.txt', 'a')
                if heading.strip() != "":
                    f.write(str(heading) + '\n')
                    f.close()
                    return

                f.write(str(self.file_num) + '\n')
                pair = self.m.get_recent()
                f.write(identifiers['user'] + " : "+ str(pair[0]) + "\n")
                f.write(identifiers['ai'] + " : " + str(pair[1]) + "\n")
                #f.write(str(prompt) + "\n")
                if self.loop_wait:
                    f.write("---\n")
                    f.write(str(time) + "\n")
                f.write("+++\n")

                f.close()
                self.file_num += 1
            except:
                self.p('Save file failed')

        pass 

    def read_questions(self):
        if int(self.questions) > -1:
            try:
                f = open('../files/questions.txt', 'r')
            except:
                f = open('/app/questions.txt', 'r')
                self.p('look for questions.txt inside flatpak')

            c = f.readlines()
            f.close()
            self.questions_list.clear()
            for i in c:
                ii = ""
                if i.strip() != "" and not i.strip().startswith('#'):
                    for j in i.strip():
                        if j != '#' and j != '\n':
                            ii += j 
                        else:
                            break
                    self.questions_list.append(ii.strip())
            self.p(self.questions_list)
            # exit()
        pass 

    def needs_restart(self):
        out = False
        file = self.user_dir + "/" + ".llm.restart"
        if os.path.exists(file):
            out = True
            os.remove(file)
            if os.path.exists(file):
                exit()
        return out
        

################### end class ########################################

def do_args(parser, k):

    #print(k.PROJECT_LAUNCH_ARGS, '<<before<<')
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            k.PROJECT_LAUNCH_ARGS += ' ' + i 
    #print(k.PROJECT_LAUNCH_ARGS,'<<after<<')

    args = parser.parse_args()
    if len(k.PROJECT_LAUNCH_ARGS.strip()) > 0:
        print(k.PROJECT_LAUNCH_ARGS.strip())
        launch_args = []
        for i in k.PROJECT_LAUNCH_ARGS.strip().split(' '):
            if len(i.strip()) > 0:
                launch_args.append(i.strip())
        args = parser.parse_args(launch_args) 
   
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

    if args.user_dir.strip() != '':
        k.user_dir = args.user_dir
    k.test = args.test
    k.verbose = args.verbose
    k.loop_wait = args.loop_wait
    k.loop_wait_saved = args.loop_wait
    k.no_check = not args.check
    k.cloud_stt = args.cloud_stt 
    k.cloud_tts = args.cloud_tts
    k.pc = args.pc 
    k.gemini = args.google_gemini
    k.review = args.review
    k.test_review = args.test_review
    if k.cloud_stt:
        k.loop_wait = False
        k.loop_wait_saved = False
    if k.review:
        review.skip_read_write = k.test 


    if args.voice == 'male' or args.voice == 'female':
        args.voice = voice_gender[args.voice]
    k.voice = args.voice

    if args.name != None and args.name.strip() != "":
        identifiers['ai'] = args.name.strip().lower()

    if args.file != None:
        k.file = args.file 

    if args.temp != 0:
        k.temp = args.temp
        if k.OPENAI_MODEL.startswith('o') or '4' in k.OPENAI_MODEL:
            if not args.google_gemini:
                ## set temp == 1.0 for advanced OPENAI_MODEL
                k.temp = 1 

    if args.timeout != 0:
        k.timeout = args.timeout
    
    if not k.review:
        k.window_ratio = 1 

    k.size_goal = args.size

    k.m = prompt.Prompt(k.PROJECT_PROMPT_ORDER, identifiers)
    if args.window > 0 and floor( args.window * k.window_ratio ) >= k.m.get_size_by_name('conversation') : #len(prompt_txt) * 2:
        k.window = args.window
        k.window_mem_ratio = 1 - k.window_ratio
        k.window_chat = floor(k.window * k.window_ratio )
        k.window_mem = k.window - k.window_chat 
        k.size_trim = 0 
    if args.window <= 0 :
        k.window = args.window
        k.window_mem_ratio  = 1 - k.window_ratio 
        k.window_chat = k.m.get_size_by_name('conversation')# len(prompt_txt) * 2 
        k.window_mem = floor( (k.window_chat * k.window_mem_ratio) / k.window_ratio)
        k.size_trim = 0
        pass 
    k.p(k.window_mem, k.window_chat, k.window_ratio, 'window')

    if args.json != None and args.json == True:
        k.json = args.json

    if args.mic_timeout != None and args.mic_timeout > -1:
        k.mic_timeout = args.mic_timeout
        if args.cloud_stt and args.mic_timeout <= 0:
            k.mic_timeout = 20 

    k.sleep_wake = args.sleep_wake
    k.wake_words = []
    if args.sleep_wake:
        k.wake_words = wake
        for i in identifiers.values():
            if i.strip() not in k.wake_words:
                k.wake_words.append(i.strip())
        if len(args.wake_words) > 0:
            for i in args.wake_words:
                if i.strip() not in k.wake_words:
                    k.wake_words.append(i.strip())

    if int(args.questions) != -1:
        k.checkpoint_num = 0 
        k.questions = args.questions
        k.read_questions()
        if k.OPENAI_CHECKPOINTS.strip() != "":
            for i in k.OPENAI_CHECKPOINTS.strip().split(','):
                if i.strip() != "":
                    k.file_num = 0 
                    k.memory_ai = []
                    k.memory_user = []
                    OPENAI_MODEL = i
                    k.questions_num = 0 
                    k.checkpoint_num += 1  
                    k.save_file(0, str(args))
                    k.loop()  # do many times
        else:
            k.checkpoint_num = 1 
            k.save_file(0, str(args))
            k.loop() # do once
        exit()

    return args 


if __name__ == '__main__':
    #k = Kernel()
    parser = argparse.ArgumentParser(description="Pi LLM - containerized LLM for raspberry pi", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--local', action="store_true", help="Not implemented")
    parser.add_argument('--verbose', action="store_true", help="Use verbose mode.")
    parser.add_argument('--test', action="store_true", help="Use test data and no LLM")
    parser.add_argument('--truncate', action="store_true", help="truncate model output.")
    parser.add_argument('--loop_wait', action="store_true", help="loop until input is detected.")
    parser.add_argument('--check', action="store_true", help="use interruption checking.")
    parser.add_argument('--name', type=str, help="define new name.")
    parser.add_argument('--offset', type=float, help="time in seconds to offset on startup.")
    parser.add_argument('--mics', action="store_true", help="display microphone data and quit.")
    parser.add_argument('--mic_timeout', type=int, default=20, help="mic timeout in seconds.")
    parser.add_argument('--file', action="store_true", help="save statistics in text file.")
    parser.add_argument('--temp', type=float, default=0.001, help="temperature for LLM operation.")
    parser.add_argument('--timeout', type=float, default=0.5, help="minutes to timeout.")
    parser.add_argument('--window', type=int, default=35, help="number of memory units used in input. (Use -1 for 'always-growing'.)")
    parser.add_argument('--cloud_stt', action="store_true", help="Google Cloud Speech Recognition. Disables --loop_wait")
    parser.add_argument('--cloud_tts', action="store_true", help="Google Cloud Text to Speech.")
    parser.add_argument('--json', action="store_true", help="use json for model prompt with OpenAI model.")
    parser.add_argument('--voice', type=str, default="en-US-Journey-F", help="Google Cloud TTS Voice Code.") ## en-US-Journey-D en-US-Journey-F
    parser.add_argument('--questions', type=int, default=-1, help="Simulate two parties with preset question list. Specify number of simulated questions. Must disable loop_wait.")
    parser.add_argument('--pc', action="store_true", help="use prompt-completion for prompt.")
    parser.add_argument('--review', action="store_true", help="use review * function.")
    parser.add_argument('--test_review', type=int, default=-1, help="test review fn at different indexes.")
    parser.add_argument('--wake_words', nargs='+', type=str, default=['wake', 'hello'], help="list of useable wake words. (Minimally implemented)")
    parser.add_argument('--sleep_wake', action="store_true", help="Enable sleep/wake type operation for --cloud_stt.")
    parser.add_argument('--size', type=int, default=2048, help="Number of TOKENS to use from context-area.")
    parser.add_argument('--user_dir', type=str, default='', help="Override user dir. Set from command line, not environment file.")
    parser.add_argument('--google_gemini', action="store_true", help="Use Google Gemini model.")
    ## NOTE: local is not implemented!! 
    args = parser.parse_args()
    user_dir = args.user_dir

    while True:
        k = Kernel(user_dir)
        args = do_args(parser, k)
        k.save_file(0, str(args))
        k.loop()
        if int(k.questions) > -1:
            break 
        k.p("interrupt here")


#!/usr/bin/env python3

import argparse
from math import floor
import string
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

prompt_txt = [
        [ 'hi', 'hello' ],
        [ 'what is your last name?', 'my last name is Smith' ],
        [ 'tell me about yourself', 'i like to talk about cooking.' ],
        [ 'what is your favorite color?', 'i like the color blue' ],
        [ 'how old are you?', 'I am thirty three years old' ],
        [ 'what is your favorite food', 'I like pizza']
            ]

identifiers = { 'user':'user', 'ai':'jane', 'mem': 'memory' }

voice_gender = { 'male': 'en-US-Neural2-D', 'female': 'en-US-Neural2-F' }


class Kernel:

    def __init__(self):
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
        self.acceptable_pause = 5 
        self.window_mem = 0 
        self.window_chat = 0 
        self.window_ratio = 1.0 / 2.0 
        self.window_line_count = 0 
        self.cloud_stt = False
        self.cloud_tts = False
        self.json = False
        self.mic_timeout = -1 
        self.voice = ""
        self.x_iter = 1 ## start at 1
        self.q = mp.Queue()
        self.prompt = ""
        self.reply = ""
        self.memory_ai = []
        self.memory_user = []
        self.y_iter = 0 
        self.questions = -1
        self.questions_list = []
        self.questions_num = 0
        self.checkpoint_num = 0 
        self.pc = False
        self.review = False
        self.review_skip = 0 
        self.review_skip_high = 3  
        self.tokens_recent = 0

        vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

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
            self.GOOGLE_APPLICATION_CREDENTIALS=str(vals['GOOGLE_APPLICATION_CREDENTIALS'])
        except:
            self.GOOGLE_APPLICATION_CREDENTIALS=''

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.GOOGLE_APPLICATION_CREDENTIALS


    def loop(self):
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
            shadow_say_text = True
            if not self.review_skip > 0:
                rr.clear()
            self.say_text(tt)
            if (self.needs_restart()):
                return 
            ## try join here!! remove sleep !!
            tt = ""
            self.empty_queue()
            x += 1
            x = x % len(prompt_txt)
            ### second process ###
            if self.loop_wait and self.questions == -1 :
                num = 0 
                high = 1000
                start = time.time()
                #self.recognize_audio(shadow_say_text)
                wake_word_found = False
                while num < high:
                    rr.clear()
                    shadow_say_text = False
                    self.p("say something in loop-wait.")
                    self.recognize_audio(shadow_say_text)
                    end = time.time()
                    if self.q.qsize() > 0:
                        break 
                    if (end - start)  > self.timeout * 60 :
                        self.p("elapsed:", (end - start), 'timeout:', self.timeout * 60 )
                        rr = ['say', 'something']
                        break
                    if num == high - 1  :
                        rr = [ 'say', 'something' ]
                        break
                    num += 1 
                ###############
                while self.q.qsize() > 0:
                    rx = self.q.get(block=True) ## <--
                    if rx.strip() != '':
                        if (self.find_wake_word(rx.strip())):
                            wake_word_found = True
                        rr.append(rx.strip())
                end = time.time()
                if not wake_word_found and num > self.acceptable_pause:
                    self.p('not wake_word_found in loop-wait', num )
                    #rr.clear()
                    continue
                else:
                    self.p('wake_word_found in loop-wait', num)

            else : #if self.questions:
                if not self.review_skip > 0:
                    rr.clear()
                sleep_time_2 = 1.75 
                shadow_say_text = False
                #self.p("say something.")
                self.recognize_audio(shadow_say_text)
                time.sleep(sleep_time_2)   
                self.p("len q:", self.q.qsize(), 'say something outside loop-wait.') 
                while (not self.q.empty()) and (not self.review_skip > 0):
                    rx = self.q.get(block=False)
                    if rx.strip() != '':
                        #self.p('c-rr', rx)
                        rr.append(rx.strip())

                if len(rr) == 0:
                    rr = ['say' , 'something,' ]
                    #skip_say_text = True

            review.read_review(self.window_mem)
            self.prompt = self.make_prompt()
            self.modify_prompt_before_model("", ' '.join(rr) )
            tt = self.model()
            
            if self.review:
                skip = review.find_marked_text(self.memory_user, self.memory_ai, tt, identifiers)
                skip = (skip and review.REM_TEXT in tt)
                if self.review_skip <= 0 and skip:
                    self.review_skip = self.review_skip_high ## magic number 1?? 
                    self.loop_wait = False
                if not skip:
                    self.review_skip = 0
                    self.loop_wait = self.loop_wait_saved
                if self.review_skip > 0:
                    self.review_skip -= 1
                    self.p("review here ..." , self.review_skip)

            tt = self.prune_input(tt) # + '.'

            self.p("====\n", self.prompt, "\n====")
            self.p("++++", self.tokens_recent, self.window_line_count , "++++")
            #self.p("++++", self.count_tokens(self.prompt), self.tokens_recent, "++++")

            self.modify_prompt_after_model(tt, ' '.join(rr))

            self.save_file(  end - start )
            if (not self.review_skip > 0) :
                rr.clear()

            if int(self.questions) > -1:
                self.questions_num += 1 
                if self.questions_num >= int(self.questions): # len(self.questions_list):
                    return 

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

        if int(self.questions) > -1:
            ret = self.questions_list[self.questions_num % len(self.questions_list)]
            ret = ret.strip()
            for i in ret.split(' '):
                if i.strip() != "":
                    self.q.put(i, block=False)
            return
        
        if self.review and self.review_skip > 0:
            return

        r = sr.Recognizer()
        
        if self.MICROPHONE_INDEX != -1:
            mic = sr.Microphone(device_index=self.MICROPHONE_INDEX)
        else:
            mic = sr.Microphone()

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

        try:
            ret = ''
            #self.p(GOOGLE_SPEECH_RECOGNITION_API_KEY)
            if self.cloud_stt == False:
                ret = r.recognize_google(audio) #,  key=GOOGLE_SPEECH_RECOGNITION_API_KEY)
            elif self.cloud_stt == True:
                ret = str(r.recognize_google_cloud(audio, self.GOOGLE_APPLICATION_CREDENTIALS))

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
        if self.test:
            self.p(txt)
            return
        if int(self.questions) > -1:
            self.p(txt, '- questions mode')
            return
        if len(txt) == 0:
            return
        if self.review and self.review_skip > 0:
            if  review.REM_TEXT in txt:
                return
            #return
            pass 

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
            #self.q.get_nowait()
            self.q.get(block=True)

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

    def find_wake_word(self, text):
        text = text.strip().lower()
        if text in identifiers.values():
            return True
        else:
            return False


    def format_json(self, user, text):
        user = user.lower().split(' ')[0]
        user = user.replace('\'', "\"")
        text = text.strip()
        text = text.replace('\'', '"')
        #x = "{'role' :'" + user + "', 'content' : '" + text +"'}"
        #print(user, text , '++++')
        if user == identifiers['ai'].lower() :
            t = 'assistant'
        else:
            t = 'user'

        x = { 'role' : t, 'content': user + " : " + text }
        return x 



    def _pre_prompt_ai(self, i):
        for j in range(len(review.memory_review)):
            a = review.memory_review[j]
            a = a.replace(";", "")
            #i[0]['content'] += " " + a 
            #if j < len(self.memory_review) - 1 or True:
            #    i[0]['content'] += "\n" #";"
            i += [ self.format_json( identifiers['mem'], a) ]
            self.window_line_count += 1 
        return i

    def _pre_prompt_ret(self, i):
        for a in review.memory_review:
            a = a.replace(";", '')
            i += identifiers['mem'] + ": " + a + "\n" # ";"
            self.window_line_count += 1 
        i = i.strip()
        i = i.strip(';')
        i += "\n"
        return i 

    def make_prompt(self):
        self.window_line_count = 0 
        ret = ""
        ai = [ 
            { 'role': 'system', 'content': 'You are a ficticious person named ' + identifiers['ai'] + 
             '. Use your imagination to answer all questions in English.' 
            } 
        ]
        if self.review:
            instructions = str(' Say anything with the "*" character as a flag to save any marked sentence permanently. Use your intuition to mark sentences. ' +
                ' Repeat anything out loud with the "' + review.REM_TEXT + '" characters as a flag to delete any marked sentence from the memory list permanently.')
            ai[0]['content'] += instructions 
            ret += instructions + '\n'
            
            if not self.json:
                ret = self._pre_prompt_ret(ret)
            if self.json:
                ai  = self._pre_prompt_ai(ai)

        pc = ""
        for i in range(len(prompt_txt) + len(self.memory_ai) - self.window_chat, len(prompt_txt)):
            if i < 0:
                continue
            u = prompt_txt[i][0]
            a = prompt_txt[i][1]
            self.window_line_count += 2 
            if self.json:
                ai += [self.format_json(identifiers['user'], u) ]
                ai += [self.format_json(identifiers['ai'], a) ]
                continue
            if self.pc:
                pc +=  u + '\n' + a + '\n'
                continue
            ret += identifiers['user'] + ": " + u 
            ret += '\n'
            ret += identifiers['ai'] + ": " + a 
            ret += '\n\n'
        if len(self.memory_ai) == len(self.memory_user):
            for i in range(len(self.memory_ai) - self.window_chat ,len(self.memory_ai)):
                if i < 0:
                    continue
                a = self.memory_ai[i]
                u = self.memory_user[i]
                self.window_line_count += 2 
                if len(a) == 0 or len(u) == 0:
                    continue
                if self.json:
                    ai += [self.format_json(identifiers['user'], u) ]
                    ai += [self.format_json(identifiers['ai'], a) ]
                    continue 
                if self.pc:
                    pc += u + '\n' + a + '\n'
                    continue
                ret += identifiers['user'] + ": " + u 
                ret += '\n'
                ret += identifiers['ai'] + ": " + a 
                ret += '\n\n'
        if self.json:
            return ai 
        if self.pc:
            return pc 
        return ret 

    def modify_prompt_before_model(self, tt, rr):
        if self.json:
            self.window_line_count += 2 
            self.prompt += [self.format_json(identifiers['user'], rr) ]# + "\n"
            self.prompt += [self.format_json(identifiers['ai'], "") ]
            return
        if self.pc:
            self.window_line_count += 1 
            self.prompt +=  rr + '\n'#, 'completion': ''}]
            return
        self.prompt += identifiers['user'] + ': ' + rr + "\n" 
        self.prompt += identifiers['ai'] + ': '
        self.window_line_count += 2 

    def modify_prompt_after_model(self, tt, rr):
        if self.review and self.review_skip > 0:
            return
        self.memory_user.append(rr)
        self.memory_ai.append(tt) 
        pass 

    def prune_input(self, text):
        self.p(text, '<<< unmodified')
        if self.json:
            t = text.strip().split(':')
            if self.review:
                if '*' in t[0] and len(t) > 1:
                    t[0] = t[0].replace('*', '')
                    t[1] += '*'
            if len(t) > 1:
                text = ' '.join(t[1:])
            if len(t) == 1 and t[0].strip() in identifiers.values():
                text = ''
        #text = text.replace(':', ' ')
        #text = text.replace('-', ' ')
        text = text.replace(';', ' ')
        text = text.replace('"', '')
        text = text.replace("'", '')
        text = text.replace("?", '.')
        text = text.replace("!", '.')
        if self.review:
            text = text.replace(review.ADD_TEXT, '')
            #text = text.replace(review.REM_TEXT, '')
        if ':' in text:
            t = text.strip().split(':')
            if len(t) == 2 or t[0].strip() in identifiers.values():
                text = ' '.join(t[1:])


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

        r = requests.post(url, headers=z_args, json=data)

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

            if self.review and self.review_skip > 0:
                return

            name = '/llm.'
            if int(self.questions) > -1:
                num = ('0000' + str(self.checkpoint_num ))[-3:]
                name += 'CHECKPOINT_' + num + '.'
            f = open(os.path.expanduser('~') + name + self.OPENAI_MODEL.strip() +'.txt', 'a')
            if heading.strip() != "":
                f.write(str(heading) + '\n')
                f.close()
                return

            f.write(str(self.file_num) + '\n')
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

    def read_questions(self):
        if int(self.questions) > -1:
            try:
                f = open('../files/questions.txt', 'r')
            except:
                f = open('/app/bin/questions.txt', 'r')
                self.p('look for questions.txt inside flatpak')

            c = f.readlines()
            f.close()
            for i in c:
                ii = ""
                if i.strip() != "" and not i.strip().startswith('#'):
                    for j in i.strip():
                        if j != '#' and j != '\n':
                            ii += j 
                        else:
                            break
                    self.questions_list.append(ii.strip())
            #print(self.questions_list)
            # exit()
        pass 

    def needs_restart(self):
        out = False
        file = os.path.expanduser("~") + "/" + ".llm.restart"
        if os.path.exists(file):
            out = True
            os.remove(file)
            if os.path.exists(file):
                exit()
        return out
        

################### end class ########################################

def do_args(parser, k):
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

    k.test = args.test
    k.verbose = args.verbose
    k.loop_wait = args.loop_wait
    k.loop_wait_saved = args.loop_wait
    k.no_check = not args.check
    k.cloud_stt = args.cloud_stt 
    k.cloud_tts = args.cloud_tts
    k.pc = args.pc 
    k.review = args.review

    if args.voice == 'male' or args.voice == 'female':
        args.voice = voice_gender[args.voice]
    k.voice = args.voice

    if args.name != None and args.name.strip() != "":
        identifiers['ai'] = args.name.strip().lower()

    if args.file != None:
        k.file = args.file 

    if args.temp != 0:
        k.temp = args.temp

    if args.timeout != 0:
        k.timeout = args.timeout
    
    if not k.review:
        k.window_ratio = 1 

    if args.window != 0:
        k.window = args.window
    k.window_chat = floor(k.window * k.window_ratio )
    k.window_mem = k.window - k.window_chat 
    #k.p(k.window_mem, k.window_chat, k.window_ratio, 'window')

    if args.json != None and args.json == True:
        k.json = args.json

    if args.mic_timeout != None and args.mic_timeout > -1:
        k.mic_timeout = args.mic_timeout
        #k.p(k.mic_timeout, ' mic_timeout ')


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
    parser.add_argument('--window', type=int, default=35, help="number of memory units used in input.")
    parser.add_argument('--cloud_stt', action="store_true", help="Google Cloud Speech Recognition.")
    parser.add_argument('--cloud_tts', action="store_true", help="Google Cloud Text to Speech.")
    parser.add_argument('--json', action="store_true", help="use json for model prompt.")
    parser.add_argument('--voice', type=str, default="en-US-Journey-F", help="Google Cloud TTS Voice Code.") ## en-US-Journey-D en-US-Journey-F
    parser.add_argument('--questions', type=int, default=-1, help="Simulate two parties with preset question list. Specify number of simulated questions. Must disable loop_wait.")
    parser.add_argument('--pc', action="store_true", help="use prompt-completion for prompt.")
    parser.add_argument('--review', action="store_true", help="use review * function.")
    ## NOTE: local is not implemented!! 
    
    while True:
        k = Kernel()
        args = do_args(parser, k)
        k.save_file(0, str(args))
        k.loop()
        if int(k.questions) > -1:
            break 
        k.p("interrupt here")


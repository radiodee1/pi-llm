#!/usr/bin/env python3

import queue
import re
import sys

from google.cloud import speech

import pyaudio

from dotenv import  dotenv_values 
import os
import time

vals = dotenv_values(os.path.expanduser('~') + "/.llm.env")

try:
    MICROPHONE_INDEX=int(vals['MICROPHONE_INDEX'])
except:
    MICROPHONE_INDEX=-1

try:
    GOOGLE_APPLICATION_CREDENTIALS=str(vals['GOOGLE_APPLICATION_CREDENTIALS'])
except:
    GOOGLE_APPLICATION_CREDENTIALS=''

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

#print(GOOGLE_APPLICATION_CREDENTIALS)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

time_start = 0
time_last_output = 0
time_end = 0 
counted_responses = 0
starting_timeout = 6 ## seconds
overall_timeout = 8 ## seconds
separator = ", "

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        """The audio -- and generator -- is guaranteed to be on the main thread."""
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self: object) -> object:
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
            input_device_index=MICROPHONE_INDEX,
        )

        self.closed = False

        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> None:
        """Closes the stream, regardless of whether the connection was lost or not."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        frame_count: int,
        time_info: object,
        status_flags: object,
    ) -> object:
        """Continuously collect data from the audio stream, into the buffer.

        Args:
            in_data: The audio data as a bytes object
            frame_count: The number of frames captured
            time_info: The time information
            status_flags: The status flags

        Returns:
            The audio data as a bytes object
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        """Generates audio chunks from the stream of audio data in chunks.

        Args:
            self: The MicrophoneStream object

        Returns:
            A generator that outputs audio chunks.
        """
        global time_start 
        time_start = time.time()
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            if should_exit():
                return
            data = [chunk]
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)


def listen_print_loop(responses: object) -> str:
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.

    Args:
        responses: List of server responses

    Returns:
        The transcribed text.
    """
    global time_end, time_start, time_last_output, counted_responses, separator 
    
    num_chars_printed = 0

    collect_characters = ""
    #time_start = time.time()

    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            collect_characters += separator + transcript.strip() 
            num_chars_printed = 0

            if len(transcript.strip()) > 0:
                counted_responses += 1 
                time_end = time.time()

    return collect_characters ## transcript

def should_exit() -> bool:
    global counted_responses, time_last_output, time_end, time_start, starting_timeout, overall_timeout 
    time_last_output = time.time()
    #overall_timeout = min(8, counted_responses + 2)
    if counted_responses > 0 and time_last_output > 0 and  time_last_output - time_end  > counted_responses + 2:
        print("Exiting...")
        print('loop time', time_end - time_start,  time_last_output - time_end, counted_responses)
        return True
    if counted_responses == 0 and time_last_output - time_start > starting_timeout:
        return True
    if time_end > 0 and time_last_output - time_end > overall_timeout:
        return True
    return False

def main() -> str:
    """Transcribe speech from audio file."""
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "en-US"  # a BCP-47 language tag
    collected_values = ""
    global time_start , counted_responses

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    time_start = time.time()

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        # Now, put the transcription responses to use.
        collected_values +=  listen_print_loop(responses)
    
    return collected_values

if __name__ == "__main__":
    x = main()
    print('xx', x.strip().strip(','), 'xx')

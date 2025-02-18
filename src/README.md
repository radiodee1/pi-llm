# source files - `src`

All the methods needed for basic operation of the program are found in the `llm.py` file. Everything associated with the `review` functionality can be found in the `review.py` file. If you don't need the `review` methods the entire `review.py` file can be omitted. If you want to do this, do not enable `--review` in the launch arguments, and comment out the `import review` line in the `llm.py` file. Review code is largely untested.

The concept for the review code is the implementation of a system where the AI tends to its own memory. Since it is a concept that has not been tested by me, the code for the functionality is put together in a haphazard way. It is a work in progress and is more or less scraped together. If the concept can be shown to work, then the review code could be - might be - rewritten more succinctly. As things are at the time of this writing, the review code is disorganized and not streamlined. 

## `llm.py`

This file handles all the methods necessary for a chatbot that can perform headlessly and use Speech-to-text and Text-to-speach. This file also handles all input argument parsing. It contains the main loop of the program, and the part of the code that connects to or makes requests of other online services.

## `review.py`

I was reading about methods employed to enhance gpt models. One concern was the ability of the models to recall important information. This was related to the context size. The other concern was for problem solving. Problem solving seems to demand an inner monologue. Sometimes this monologue is achieved through token manipulation, and sometimes it seems to be achieved through a recurrent mechanism like that used in RNNs. I had some ideas concerning what I was reading, especially the Long Term Memories, and I tried to implement them in the `review` code.

- Long Term Memory - asking the model to curate its own set of facts or phrases that it can go back to later. This would all happen at test time.

- Saved Memories - curated phrases are saved in a simple text file and are reloaded every time the prompt is generated. I'm calling the list the 'Review List'. It's saved in the user's `/home` directory.

- Automatic Phrase Saving - at test time, the program will, if enabled, test phrases to see if they contain uncommon text. If they contain uncommon text the `review` mechanism will save the phrase. This automatic sub-system uses a programmatic algorithm for deciding if text is novel. The system does not rely on output from the LLM.

- Add and Remove - the model is supplied with functions for adding a phrase and similarly for removing a phrase. These are very simple functions that the gpt model can call on to curate the review list.

- Problem Solving - we have no special mechanism for enhancing the problem solving abilities of these gpt models. Most Problem Solving ideas are implemented in the gpt architecture, and are not issues at test time. 




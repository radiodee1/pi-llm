# source files

All the methods needed for basic operation of the program are found in the `llm.py` file. Everything associated with the `review` functionality can be found in the `review.py` file. If you don't need the `review` methods the entire `review.py` file can be omitted. Review code is largely untested.

## llm.py
This file handles all the methods necessary for a chatbot that can perform headlessly and use Speech-to-text and Text-to-speach. This method also handles all input argument parsing.

## review.py

I was reading about methods employed to enhance gpt models. One concern was the ability of the models to recall important information. This was related to the context size. The other concern was for problem solving. Problem solving seems to demand an inner monologue. I had some ideas concerning what I was reading, and I tried to implement them in the `review` code.

- Long Term Memory - asking the model to curate its own set of facts or phrases that it can go back to later.

- Saved Memories - curated phrases are saved in a simple text file and are reloaded every time the prompt is generated.

- Automatic Phrase Saving - at test time, the program will, if enabled, test phrases to see if they contain uncommon text. If they contain uncommon text the `review` mechanism will save the phrase. This automatic save system uses a programmatic algorithm for deciding if text is novel. The system does not rely on output from the LLM.

- Add and Remove - the model is supplied with functions for adding a phrase and similarly for removing a phrase. These are very simple functions that the gpt model can call on to curate the review list.

- Problem Solving - we have no special mechanism for enhancing the problem solving abilities of these gpt models.




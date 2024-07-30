# gpt-3.5-turbo result overview

In the file `~/.llm.env`, the environment file, the value for `OPENAI_MODEL` was un set or modified to read:

```
OPENAI_MODEL=gpt-3.5-turbo
```

This changed the model that the open ai service connects you to. As before we set up two computers and had them talk to each other for 15 minutes. The gpt-3.5-turbo model insisted on talking to you and continuously asked what you wanted to ask it about.

Then to get the graphs there are two steps. Firstly you must count the words and their frequency.

```
cd pi-llm/script 
./count.py llm.05a.txt > pi-llm/png/35-turbo/test.llm.05a.txt
```

This copies the output of the count.py script and puts it in a file called `test.llm.05a.txt`. Then you prune the file so that there are only 15 or 16 words. Then you plot the file using the `plot.py` script.

```
cd pi-llm/script 
./plot.py --file ../png/35-turbo/test.llm.05a.txt --bin ../../GoogleNews-vectors-negative300.bin --output nonrandom --topn 5
```

This plots the graphs in 2D. They are bigger plots than the 'random' plot, and smaller plots than the '4o-mini' plot.

The x axes go from -100 to 100, and the y axes go from -100 to 150. That's 200 x 250, which is 50,000.

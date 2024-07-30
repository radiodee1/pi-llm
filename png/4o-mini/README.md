# gpt-4o-mini result overview

In the file `~/.llm.env`, the environment file, the value for `OPENAI_MODEL` was set or modified to read:

```
OPENAI_MODEL=gpt-4o-mini
```

This changed the model that the open ai service connects you to. As before we set up two computers and had them talk to each other for 15 minutes. While the gpt-3.5-turbo model insisted on talking to you and continuously asked what you wanted to ask it about, the gpt-4o-mini model just thanks you over and over again for chatting with it.

Then to get the graphs there are two steps. Firstly you must count the words and their frequency.

```
cd pi-llm/script 
./count.py llm.gpt-4o-mini_a.txt llm.gpt-4o-mini_b.txt > pi-llm/png/4o-mini/test.gpt-4o-mini.txt
```

This copies the output of the count.py script and puts it in a file called `test.gpt-4o-mini.txt`. Then you prune the file so that there are only 15 or 16 words. In my case I had to remove 9 words from the bottom of the list. Then you can run the plot script.

```
cd pi-llm/script 
./plot.py --file ../png/4o-mini/test.gpt-4o-mini.txt --bin ../../GoogleNews-vectors-negative300.bin --output larger_size_nonrandom --topn 5
```

This plots the graphs in 2D. The size of the graphs is slightly larger than the previous graphs. This is what we wanted to show.

The graph axis is -800 to 700 in the x coordinate, and -800 to 600 in the y coordinate. That's 1500 by 1400.

# SCRIPT files

There are two basic scripts in this folder. One is `count.py` and the other is `plot.py`. They are obviously important for plotting the output of the models. There are several support scripts in the folder. They illustrate the steps taken to use the `count.py` and `plot.py`. You don't have to use the scripts. Instead you can use them as a reminder for how to go about getting plots.

- Start by downloading the embeddings file. The url for downloading is found in the `do_00_download.sh` script. You can probably download the embeddings anywhere on your computer, then unpack them. Put them in the directory beside the `pi-llm` folder.
- At some point you must run the llm models against each other. This is the only way to get the recorded log from the conversation.
- Take the recorded conversation and use the `count.py` script on it. When you do this you will see a list on the screen that shows the most used words. To continue with the next step you must catinate the output into a text file.
- Take the output file and run it through the `plot.py` script. This will yeald a `png` file.



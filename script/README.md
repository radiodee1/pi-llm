# SCRIPT files

There are two basic scripts in this folder. One is `count.py` and the other is `plot.py`. They are obviously important for plotting the output of the models. There are several support scripts in the folder. They illustrate the steps taken to use the `count.py` and `plot.py`. You don't have to use the scripts. Instead you can use them as a reminder for how to go about getting plots.

- Start by downloading the embeddings file. The url for downloading is found in the `do_00_download.sh` script. You can probably download the embeddings anywhere on your computer, then unpack them. Put them in the directory beside the `pi-llm` folder.
- At some point you must consider running the llm models against each other. This is one way to get the recorded log from the conversation. The other option is to run the program using `--question` mode. You can change the `questions.txt` file but every time you do you must build the flatpak again or run the `llm.py` program from the command line.
- Take the recorded conversation and use the `count.py` script on it. When you do this you will see a list on the screen that shows the most used words. To continue with the next step you must pipe the output into a text file. You can also use the `--save` option and the `--answers_only` option.
- Take the output file and run it through the `plot.py` script. This will yield a `png` file. You may set `--p` to 1 and `--topn` to 1 as well. 
- Output from the `plot.py` program is placed in the project's `png` folder. Output from the `count.py` program is placed in the file that contains the input file.
- You can run the `plot` program and the `count` program on multiple files specidied with the `*` command line argument. Also, if you are using the numbered scripts, you can specify a single file on the command line as the first argument on the command line.



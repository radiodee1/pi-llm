#!/bin/bash 

echo "plot the points from the 'count.py' stage."
echo "this uses the GoogleNews data."

read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

./plot.py --file ../txt/llm.dialogue.count.txt --bin ../../GoogleNews-vectors-negative300.bin --output ../png/llm.dialogue


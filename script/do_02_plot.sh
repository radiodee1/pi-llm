#!/bin/bash 

PLOTINPUT="../txt/count-llm.dialogue.count.txt"

if [ $# -eq '1' ]; then
    PLOTINPUT=$1
fi 

echo ""
echo "The input file is specified as the first"
echo "argument on the command line."

echo ""

echo "The input file is currently set to " $PLOTINPUT
echo ""

echo "Use this script to plot the points from the "
echo "'count.py' stage."
echo ""
echo "This uses the GoogleNews data and takes some time."
echo ""
echo "The output of this script is ../png/llm.dialogue.png"
echo "You will probably want to rename it."
echo ""

read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

./plot.py $PLOTINPUT --bin ../../GoogleNews-vectors-negative300.bin --p 1 --topn 1


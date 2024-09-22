#!/bin/bash 

PLOTINPUT="../txt/llm.dialogue.count.txt"

if [ $# -eq '1' ]; then
    PLOTINPUT=$1
fi 

echo ""
echo "the input file is specified as the first"
echo "argument on the command line."

echo ""

echo "the input file is currently set to " $PLOTINPUT
echo ""

echo "use this script to plot the points from the "
echo "'count.py' stage."
echo ""
echo "this uses the GoogleNews data and takes some time."
echo ""
read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

./plot.py --file $PLOTINPUT --bin ../../GoogleNews-vectors-negative300.bin --output ../png/llm.dialogue


#!/bin/bash 

PLOTINPUT="../txt/count-llm.dialogue.count.txt"

echo ""
echo "The input file is specified as the first"
echo "argument on the command line."

echo ""

if [ $# -gt '0' ]; then

    echo "The output file is currently " $@

else
    echo "The output file is currently called " $PLOTINPUT

fi 


echo ""
echo "Run the script by pressing any key, or abort by"
echo "pressing [Ctl-c] ..."
echo ""
read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

if [ $# -gt '0' ]; then
    ./plot.py $@ --bin ../../GoogleNews-vectors-negative300.bin --p 1 --topn 1 --words 10
else
    ./plot.py $PLOTINPUT --bin ../../GoogleNews-vectors-negative300.bin --p 1 --topn 1 --words 10 

fi 





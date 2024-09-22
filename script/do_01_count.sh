#!/bin/bash 

COUNTOUTPUT="../txt/llm.dialogue.count.txt"

if [ $# -eq '1' ]; then

    COUNTOUTPUT=$1
fi 


echo "setup two instances of the flatpak on two different computers..."
echo "have the instances exchange dialogue for 15 minutes or so."
echo ""
echo "put the dialogue file (located in the '/home' folder on each machine)"
echo "in the 'txt' folder on this computer in this git repository."
echo ""
echo "use the name of the output file as the first argument on the "
echo "command line with this script."

echo ""

echo "the output file is currently called " $COUNTOUTPUT
echo ""
echo "run the script by pressing any key, or abort by"
echo "pressing [Ctl-c] ..."
echo ""
read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

./count.py ../txt/llm.dialogue.txt --count 25 --low 10 > $COUNTOUTPUT #../txt/llm.dialogue.count.txt




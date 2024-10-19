#!/bin/bash 

COUNTINPUT="../txt/llm.dialogue.txt"

echo "Setup two instances of the flatpak on two different computers..."
echo "Have the instances exchange dialogue for 15 minutes or so."
echo ""
echo "Put the dialogue file (located in the '/home' folder on each machine)"
echo "in the 'txt' folder on this computer in this git repository."
echo ""
echo "Use the name of the output file as the first argument on the "
echo "command line with this script."

echo ""


if [ $# -gt '0' ]; then

    echo "The output file is currently " $@

else
    echo "The output file is currently called " $COUNTINPUT

fi 


echo ""
echo "Run the script by pressing any key, or abort by"
echo "pressing [Ctl-c] ..."
echo ""
read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

if [ $# -gt '0' ]; then

    ./count.py $@ --count 25 --low 3 --save --answers_only

else
    ./count.py $COUNTINPUT --count 25 --low 3 --save --answers_only
fi 





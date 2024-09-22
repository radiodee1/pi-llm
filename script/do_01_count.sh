#!/bin/bash 

echo "setup two instances of the flatpak on two different computers..."
echo "have the instances exchange dialogue for 15 minutes or so."

echo "put the dialogue file (located in the '/home' folder on each machine)"
echo "in the 'txt' folder on this computer in this git repository."
echo "call the file 'llm.dialogue.txt'"

echo "run the following command"

read  -n 1 -p "Continue/Break(Ctl-c):" xinput

echo $xinput

./count.py ../txt/llm.dialogue.txt --count 25 --low 10 > ../txt/llm.dialogue.count.txt




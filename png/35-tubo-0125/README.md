# Train gpt-3.5-turbo-0125 and plot results

- ckpt 1 is the unmodified `gpt-3.5-turbo-0125` model before fine-tuning.
- ckpt 2, and 3 are the checkpoint files from during fine-tuning. 
- ckpt 4 is the final model file.

```
cd script/
./count.py ../png/35-turbo-0125/llm.ckpt01.gpt-3.5-turbo-0125.txt --count 25 --low 10 > ../png/35-turbo-0125/llm.count.35-turbo-ckpt01.txt 
## count for checkpoint 1 ##

./plot.py --bin ../../GoogleNews-vectors-negative300.bin --file ../png/35-turbo-0125/llm.count.35-turbo-ckpt01.txt --output ../png/35-turbo-0125/llm.35-turbo-ckpt01 
## plot for checkpoint 1 ##
```

| | ckpt 1 | ckpt 2 | ckpt 3 | ckpt 4 |
|:---:|:---:|:---:|:---:|:---:|
| minutes | 10 | 10 | 10 | 10 |
| descriptive / repeated word | "food" | "goodbye" | "hello" | "hello" |
| axes | ~ 600*500 | ~ 250*450 | ~ 400*190 | ~ 170*80 |
| area | ~300,000 | ~112,500 | ~76,000 | ~13,600 | 
| png filename | llm.35-turbo-ckpt01.png | llm.35-turbo-ckpt02.png | llm.35-turbo-ckpt03.png | llm.35-turbo-ckpt04.png |



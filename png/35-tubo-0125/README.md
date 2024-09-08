# Train gpt-3.5-turbo-0125 and plot results

- ckpt 1 is the unmodified gpt-3.5-turbo-0125 model before fine-tuning.
- ckpt 2, and 3 are the checkpoint files from during fine-tuning. 
- ckpt 4 is the final model file.

| | ckpt 1 | ckpt 2 | ckpt 3 | ckpt 4 |
|:---:|:---:|:---:|:---:|:---:|
| minutes | 10 | 10 | 10 | 10 |
| descriptive / repeated word | "food" | "goodbye" | "hello" | "hello" |
| axes | ~ 600*500 | ~ 250*450 | ~ 400*190 | ~ 170*80 |
| volume | ~300,000 | ~112,500 | ~76,000 | ~13,600 | 



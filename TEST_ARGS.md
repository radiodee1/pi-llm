# pi-llm
Containerized llm for rapberry-pi.

## Early tests

This doc does not explain 'tests' in the common programming sense, but instead some flags or arguments that I've written to help in programming. Early tests were mostly composed of replacing the speech recognition functions with functions that took typed text as input. These were replaced over time.

## Current tests

There are two components for testing presently, the `--questions` argument and the `--test` argument.

1. First we will consider `--questions`.

- `--questions` takes one input value, an integer between 0 and some larger number we will call n.
- `--questions` uses a file called 'questions.txt', located in the repository at 'files/questions.txt'.
- `--questions` code uses the first n sentences from the questions.txt file and uses them as input.
- `--questions` uses an iterator referred to as the 'questions' iterator. It keeps track of the code's position in the questions.txt file.
- `--questions` code halts execution when the n sentences have been used.
- `--questions` does not allow for the input of audio using speech recognition.
- `--questions` code can use any sentences at all, as long as they are recorded in the 'files/questions.txt' file.
- `--questions` code will repeat the sentences in 'files/questions.txt' if the number n is larger than the number of sentences in 'files/questions.txt'.

2. Below is a rundown of the `--test` code. This code performs two tasks.

- `--test` takes one input value, an input between 0 and some larger number less then or equal to the number specified in `--questions`.
- `--test` disables the model input and output, essentially removing the model from the processing loop.
- `--test` replaces model output with a single sentence. The sentence is constructed from the number of the reply and the text string 'reply to question n' where 'n' is the loop number.
- `--test` uses the 'questions' iterator for the 'n' number specified above. This means the `--test` code works better with the `--questions` code.
- `--test` uses a timer to space out the replies from the code by about two seconds for each iteration through the loop.
- `--test` checks the contents of the 'questions' iterator, and when the value matches the `--test` value the `review` test functions are triggered.
- `--test` will work without `--questions` but it will not trigger the `review` test function.

3. Here is some `--test_review` info.

- `--test_review` takes a single integer as an argument. This integer should be smaller than the input value from the '--questions' argument.
- `--test_review` specifies the point where 'review' is tested. At that index the program adds the string '++' to the model output line.
- `--test_review` then processes the input as if it were issued by the model and meant for the 'review' process. 
- `--test_review` then has the program then skip a line of input so that the model can consider the most recent line from the user. 
- `--test_review` is used to watch the skipping process and to finish it correctly.

4. Notes on `--test` flag.

- `--test` takes no argument.
- `--test` makes sure that the program operates without asking for real audio output from the user.
- `--test` also disables the file operations in the `review` code because the `--test_review` function is not using true model output for it's '++' operation.

## Example Configuration 

To see the current tests work, put the following in your `~/.llm.env` file along side of your other configurations.

```
PROJECT_LAUNCH_ARGS='--file  --voice female --name Jane  --verbose --temp 0.95 --timeout 2.5 --mic_timeout 0 --wake_words hi jane cosmo --cloud_stt --cloud_tts --truncate --questions 6 --test_review 2 --review --test '
```

The part of the environment variable that specifies the testing is `--questions 6 --test_review 2 --review --test`. 

## Example File Contents 

1. `file/questions.txt`

```
# arbitrary upper case
Question0 num zero here
Question1 num one here
Question2 num two here
question3 num three here
question4 num four here
question5 num five here
question6 num six here 
question7 num seven here
```

Note that upper case text is totally arbitrary.

2. `~/llm.CHECKPOINT_001.gpt-3.5-turbo.txt`

```
Namespace(local=False, verbose=True, test=True, truncate=True, loop_wait=False, check=False, name='Jane', offset=None, mics=False, mic_timeout=0, file=True, temp=0.95, timeout=2.5, window=35, cloud_stt=True, cloud_tts=True, json=False, voice='en-US-Neural2-F', questions=6, pc=False, review=True, test_review=2, wake_words=['hi', 'jane', 'cosmo'], loop_wait_test=-1)
0
user : Question0 num zero here
jane : reply to question 0
+++
1
user : Question1 num one here
jane : reply to question 1
+++
2
user : Question2 num two here
jane : reply to question 3
+++
3
user : question4 num four here
jane : reply to question 4
+++
4
user : question5 num five here
jane : reply to question 5
+++
```

Note that `reply to question 2` is skipped. This is because `--test_review` is set to `2`.

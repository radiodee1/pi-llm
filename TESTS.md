# pi-llm
Containerized llm for rapberry-pi.

## Early tests

Early tests were mostly composed of replacing the speech recognition functions with functions that took typed text as input.

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


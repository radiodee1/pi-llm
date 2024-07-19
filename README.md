# pi-llm
containerized llm for raspberry pi

Put key values in a file called `~/.llm.env`. An example follows.

```bash
# Test values...
TEST_SIX=6
TEST_NINE=9

OPENAI_API_KEY=abc

GOOGLE_SPEECH_RECOGNITION_API_KEY=abc

MICROPHONE_INDEX=-1
PROJECT_LAUNCH_ARGS=''

GOOGLE_APPLICATION_CREDENTIALS=/path-to-json-file/file.json

```

Below are some test arguments for the PROJECT_LAUNCH_ARGS variable.

```
PROJECT_LAUNCH_ARGS='--no_check --file --loop_wait --verbose --name Bob --offset 20 --timeout 5 '
```

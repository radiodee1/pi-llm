# pi-llm
containerized llm for raspberry pi

Put key values in a file called `~/.llm.env`. An example follows.

```bash
# Test values...
TEST_SIX=6
TEST_NINE=9

OPENAI_API_KEY=abc
# OPENAI_MODEL=abc

GOOGLE_SPEECH_RECOGNITION_API_KEY=abc

MICROPHONE_INDEX=-1
PROJECT_LAUNCH_ARGS=''

# For Google Cloud Speech...
GOOGLE_APPLICATION_CREDENTIALS=/path-to-json-file/file.json

```

Below are some test arguments for the PROJECT_LAUNCH_ARGS variable.

```
PROJECT_LAUNCH_ARGS='--file --loop_wait --verbose --name Bob --offset 20 --timeout 5 --cloud'
```

- Collision checking does not work well. Do not use `--check`. 

- Cloud speech recognition, `--cloud`, works well but is largely untested. 

- Remember that background noise is allways a problem. The microphone will hang if there's too much background noise and the end of input text will not be detected.

If you leave the OPENAI_MODEL unset, the default will be used, which is "gpt-3.5-turbo".

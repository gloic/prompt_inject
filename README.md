# Prompt Inject

## Description

This is an extension for https://github.com/oobabooga/text-generation-webui

It permits to use __name__ syntax to inject the content of one or more text files in your prompt.

## Usage

- Add a new file named ```something.txt``` in extensions/prompt-inject/prompts/
- Edit and write the text you want to inject (For example: "world")
- Inject the content of the file in your prompt : ```Hello __something__```
- The model will receive "```Hello world```"

## Compatibility
TODO

## Extension config
Not yet

## Usage through API
TOD

## Other

This extension is inspired by https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards


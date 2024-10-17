# Prompt Inject

## Description

This is an extension for https://github.com/oobabooga/text-generation-webui

It permits to use ```__name__``` syntax to inject the content of one or more text files in your prompt.

## Usage

### Quickstart

- Add a new file named ```something.txt``` in extensions/prompt-inject/prompts/
- Edit and write the text you want to inject (For example: "world")
- Add the wildcard in your prompt : ```Hello __something__```
- The model will receive "```Hello world```"

### Inner wildcard

A prompt can contains another wildcard

- Add a new file named ```parent.txt``` containing ```A parent __child__```
- Add a new file named ```child.txt``` containing ```and its child```
- The model will receive "```A parent and its child```"

### Sub folders

Prompts files can be stored in sub folders.

- Add a new file named ```story of.txt``` containing "```Tell me a long and beautiful story about the given character```"
- In a sub folder "**char**", add a new file named ```bob.txt``` containing ```Bob is a man, he is working in a spaceship...```
- Use it with:
  ```
  __story of__
  __char/bob__
  ```

### Specials

Specials wildcards are : "!", "?" and "&"
They permit to quickly inject a prompt before another wildcard or your prompt. Their values are located in ```specials/exclamation_mark.txt```, ```specials/question_mark.txt``` etc...
Each special file contain an example but you can replace by what you want.

- Add a new file named ```who.txt``` containing ```Who are you ?```
- The file ```specials/ampersand.txt``` contains "```Think step by step, use the <thinking...</thinking> format...\n```"
- If your prompt is "```&who```" the model will receive :
  ```
     Think step by step, use the <thinking...</thinking> format...
     Who are you ? 
- It works too with a special alone : "```__&__```"
- and multiple specials : ```__&!__```"

## Compatibility

TODO

## Extension config

Not yet

## Usage through API

TODO. I don't think this plugin is called from the API.

### GUI

TODO

## Other

This extension is inspired by https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards


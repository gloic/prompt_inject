# Prompt Inject

## Description

This is an extension for https://github.com/oobabooga/text-generation-webui

It permits to use ```__name__``` syntax to inject the content of one or more text files in your prompt.

## Usage

### Quickstart

- Create a file named ```something.txt``` in extensions/prompt-inject/prompts/
- Edit and write the text you want to inject (For example: "world")
- Add the wildcard in your prompt : ```Hello __something__```
- The model will receive "```Hello world```"

### Sub folders

Prompts files can be stored in sub folders.

Syntax: ```folder/something``` or ```sub/sub1/other```

<details>
  <summary>Example</summary>

  - Create a file named ```story of.txt``` containing "```Tell me a long and beautiful story about the given character\n\n```"
  - In a sub folder "**char**", Create a file named ```bob.txt``` containing ```Bob is a man, he is working in a spaceship...```
  - Use it with:
    ```
    __story of__
    __char/bob__
    ```
  - THe model will receive 
    ```
    Tell me a long and beautiful story about the given character
    
    Bob is a man, he is working in a spaceship...
    ```
</details>

### Inner wildcard

A prompt can contains another wildcard, allowing to use a common prompt 

Syntax: ```

<details>
  <summary>Example</summary>

- Create a file named ```parent.txt``` containing ```A parent __child__```
- Create a file named ```child.txt``` containing ```and its child```
- The model will receive "```A parent and its child```"
</details>


### Specials

Specials wildcards permit to quickly inject a prompt before another wildcard or in your prompt.

- ```__!__``` -> ```specials/exclamation_mark.txt```
- ```__?__``` -> ```specials/question_mark.txt```
- ```__&__``` -> ```specials/ampersand.txt```

_Syntax:_ ```__!__``` or ```__!something__```

<details>
  <summary>Example</summary>

  - Create a file named ```who.txt``` containing ```Who are you ?```
  - The file ```specials/ampersand.txt``` contains ```Think step by step, use the <thinking...</thinking> format...\n```
  - If your prompt is "```&who```" the model will receive :
    ```
      Think step by step, use the <thinking...</thinking> format...
      Who are you ?
    ``` 
</details>

### Combos
    
Use combos to combine or pick randomly one prompt.

- "AND" Syntax: ```__promptA&&promptB``` or ```__promptA && promptB``` will concat promptA and promptB
- "OR" Syntax: ```__promptA||promptB``` or ```__promptA || promptB``` will pick either promptA or promptB

<details>
  <summary>Example</summary>

  #### AND Combo
  - Create a file named ```part1.txt``` containing ```This is Part 1 ```
  - Create a file named ```part2.txt``` containing ```and this is Part 2```
  - If your prompt is "```__part1||part2__```"
  - The model will receive ```This is Part 1 and this is Part 2```

  #### OR Combo
  - Create a file named ```odd.txt``` containing ```It's odd```
  - Create a file named ```even.txt``` containing ```It's even```
  - If your prompt is "```__odd||even__```"
  - The model will receive randomly ```It's odd``` or ```It's even```
</details>

## Going further

  You can combine and create a hierarchy to organize yours prompts to create dynamics prompts.

<details>
  <summary>Example</summary>

  - Create ```places/kitchen.txt``` containing ```You are in a vaste kitchen...```
  - Create ```places/bedroom.txt``` containing ```You are in the bedroom, the light is off```
  - 
  - Create ```choices/choice1.txt``` containing ```You take your shoe as a weapon and face to your fears```
  - Create ```choices/choice1.txt``` containing ```You hear something weird```
  - Create ```choices.txt``` containing ```__choices/choice1 || choices/choice2__```
  - 
  - Create ```rp/describe.txt``` containing ```Describe what happen in this scene```
  - Create ```rp/details.txt``` containing ``` and add a lot of details.```
  - Create ```instructions.txt``` containing:
  ```
  __place/kitchen || place/bedroom__
  __choices__
  
  __rp/describe && __rp/details__
  ```
  - The file ```specials/exclamation_mark.txt``` contains ```Be careful, you are a very weak adventurer, you are already hurt and afraid. Please make a good choice.\n\n```
  - If your prompt is "```__!instructions__```"
  - The model will receive randomly a composition of the prompts 
  ```
  Be careful, you are a very weak adventurer, you are already hurt and afraid. Please make a good choice.
  
  You are in the bedroom, the light is off
  You hear something weird
  
  Describe what happen in this scene and add a lot of details.
  ```
</details>


  

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


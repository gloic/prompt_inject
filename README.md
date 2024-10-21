# Prompt Inject

## Description

This is an extension for https://github.com/oobabooga/text-generation-webui

It permits to use ```__name__``` syntax to inject the content of one or more text files in your prompt.

## Usage

### Quickstart

- In "extensions/prompt-inject/prompts/", create a file named ```something.txt``` containing the text ```world``` 
- When the prompt is ```Hello __something__```
- The model receives ```Hello world```

### Sub folders

Prompts files can be stored in sub folders.

Syntax: ```__folder/something__``` or ```__sub/sub1/other__```

<details>
  <summary>Example</summary>

  - Create a file named ```story of.txt``` containing ```Tell me a long and beautiful story about the given character\n\n```
  - In a sub folder "**/char**", create a file named ```bob.txt``` containing ```Bob is a man, he is working in a spaceship...```
  - When the prompt is:
    ```
    __story of__
    __char/bob__
    ```
  - The model receives:
    ```
    Tell me a long and beautiful story about the given character
    
    Bob is a man, he is working in a spaceship...
    ```
</details>

### Nested wildcards

A prompt can contains another wildcards, allowing to nest multiples wildcards in the prompt.

<details>
  <summary>Example</summary>

  - Create a file named ```parent.txt``` containing ```A parent __child__```
  - Create a file named ```child.txt``` containing ```and its child```
  - When the prompt is ```__parent__```
  - The model receives ```A parent and its child```
</details>


### Specials

Specials wildcards permit to quickly inject a prompt before another wildcard or in your prompt.

- ```__!__``` : ```specials/exclamation_mark.txt```
- ```__?__``` : ```specials/question_mark.txt```
- ```__&__``` : ```specials/ampersand.txt```

_Syntax:_ ```__!__``` or ```__!something__```

<details>
  <summary>Example</summary>

  - Create a file named ```who.txt``` containing ```Who are you ?```
  - The file ```specials/ampersand.txt``` contains ```Think step by step, use the <thinking...</thinking> format...\n```
  - When the prompt is ```__&who__```
  - The model receives :
    ```
      Think step by step, use the <thinking...</thinking> format...
      Who are you ?
    ``` 
</details>

### Combos
    
Use combos to combine or pick randomly one prompt.

- "AND" Syntax: ```__promptA&&promptB__``` or ```__promptA && promptB__``` will concat promptA and promptB
- "OR" Syntax: ```__promptA||promptB__``` or ```__promptA || promptB__``` will pick either promptA or promptB

<details>
  <summary>Example</summary>

  #### AND Combo
  - Create a file named ```part1.txt``` containing ```This is Part 1 ```
  - Create a file named ```part2.txt``` containing ```and this is Part 2```
  - When the prompt is ```__part1||part2__```
  - The model receives ```This is Part 1 and this is Part 2```

  #### OR Combo
  - Create a file named ```odd.txt``` containing ```It's odd```
  - Create a file named ```even.txt``` containing ```It's even```
  - Create a file named ```prime.txt``` containing ```It's prime```
  - When the prompt is ```__odd||even||prime__```
  - The model receives randomly ```It's odd``` or ```It's even``` or ```It's prime```
</details>

## Going further

  You can combine and create a hierarchy to organize yours prompts to create dynamics prompts.

<details>
  <summary>Example</summary>

  - Create ```places/kitchen.txt``` containing ```You are in a vaste kitchen...```
  - Create ```places/bedroom.txt``` containing ```You are in the bedroom, the light is off```
  - 
  - Create ```events/event1.txt``` containing ```You take your shoe as a weapon and face to your fears```
  - Create ```events/event2.txt``` containing ```You hear something weird```
  - Create ```events.txt``` containing ```__events/event1 || events/event2__```
  - 
  - Create ```rp/describe.txt``` containing ```Describe what happen in this scene```
  - Create ```rp/details.txt``` containing ``` and add a lot of details.```
  - Create ```instructions.txt``` containing:
  ```
  __places/kitchen || places/bedroom__
  __events__
  
  __rp/describe && __rp/details__
  ```
  - The file ```specials/exclamation_mark.txt``` contains ```Be careful, you are a very weak adventurer, you are already hurt and afraid.\n\n```
  - When the prompt is ```__!instructions__```
  - The model receive randomly a composition of the prompts: 
    ```
    Be careful, you are a very weak adventurer, you are already hurt and afraid.
      
    You are in the bedroom, the light is off
    You hear something weird
      
    Describe what happen in this scene and add a lot of details.
    ```
</details>

## Multilanguage

You can have the same prompt in different languages and use them either by default or when needed.

Configuration parameter: ```suffix_language```

When specified, the extension will look for files suffixed by the value of the parameter. 

*Notes:* 
  - Any suffix can be used: ```salutations-anything.txt``` is valid
  - If _suffix_language_ is not configured, it's still possible to manually use a wildcard of another language: ```__salutation-fr__``` will look for the file ```salutations-fr.txt```

<details>
  <summary>Example</summary>
    
  - Create ```salutations-fr.txt``` containing ```Bonjour```
  - Parameter ```suffix_language``` contains ```fr```
  - When the prompt is ```__salutations__```
  - The model receives ```Bonjour```
  
</details>

## Compatibility

TODO

## Extension config

- _is_model_warning_: if enabled an error message is injected in the prompt when a wildcard cannot be resolved, allowing the model to warn the user.
- _error_wildcard_not_found_: error message sent to the model when a wildcard cannot be resolved (depends on _is_model_warning_)
- _suffix_language_: look for files suffixed by this value. See "Multilanguage" section for more information

## Other

This extension is inspired by https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards


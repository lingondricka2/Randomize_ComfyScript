## About The Project
The infinite monkey method of creating your perfect workflow for ComfyUI. My first project and it's a work in progress so keep expectations low.

## Prerequisites
* ComfyScript, install instructions at https://github.com/Chaoses-Ib/ComfyScript
* WAS Node Suite, install via Comfy-manager or https://github.com/WASasquatch/was-node-suite-comfyui
* AutomaticCFG, install via Comfy-manager or https://github.com/Extraltodeus/ComfyUI-AutomaticCFG
* Dynamic prompts, https://github.com/adieyal/dynamicprompts

  ```sh
  pip install dynamicprompts
  pip install "dynamicprompts[magicprompt]"
  ```

## Installation
Put randomize.py and randomize.yml in a subfolder of ComfyScript
e.g ComfyUI\custom_nodes\ComfyScript\scripts\Randomizer

## Usage
Edit the yaml file to make it use your models, use:
```sh
python randomizer.py list
```
to get a list of all models, useful when editing the yaml file.
```sh
python randomizer.py
```
To run the randomizer.

## Examples
Cherry picked from 200 generated images

https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0002.png
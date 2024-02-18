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
To run the randomizer. The resulting images can be loaded in ComfyUI web-ui.

## Examples
Cherry picked from 200 generated images using prompt "monkey typing on a typewriter"

![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0002.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0003.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0005.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0006.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0010.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0014.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0015.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0018.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0028.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0031.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0034.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0037.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0040.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0041.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0047.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0050.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0054.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0057.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0058.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0065.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0066.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0070.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0072.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0076.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0080.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0083.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0087.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0088.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0094.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0095.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0098.png)
![alt text](https://github.com/lingondricka2/Stuff/blob/main/randomizer_images/ComfyUI_0099.png)

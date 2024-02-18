## About The Project
The infinite monkey method of creating your perfect workflow for ComfyUI. My first project and it's a work in progress so keep expectations low. As it is now the yaml file can be confusing and a pain to edit, probably should have some experience with python/yaml and patience.

So what are the advantages of using this over the web-ui? I know a lot of randomizing can be done in the web-ui, but probably not everything that is done here, haven't tried it myself though. One big advantage is that the resulting workflow is a lot cleaner using this script. Another advantage for me at least is better memory management, I can merge 6 checkpoints no problem where as in the web-ui it would have crashed my computer.

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
to get a list of all models, useful when editing the yaml file. The settings in the yaml file is rather conservative right now to avoid images that have artifacts and are too out there, but that can be changed of course.
```sh
python randomizer.py
```
To run the randomizer. The resulting images can be loaded in ComfyUI web-ui.

## TODO
* A GUI for the settings would be great, but probably not going to happen.
* Random shape/gradients blending (almost done)
* Random regional prompts using color segmentation, maybe
* Other small things like random VAE and image save options
* Upscaler version of this script

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

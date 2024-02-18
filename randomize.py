import sys
import os
import datetime
import random
import yaml
#import numpy as np

from dynamicprompts.generators import RandomPromptGenerator
from dynamicprompts.generators.feelinglucky import FeelingLuckyGenerator
from dynamicprompts.generators.magicprompt import MagicPromptGenerator


#sys.path.insert(0, 'src')
#from comfy_script.runtime import *
#load()
#from comfy_script.runtime.nodes import *

from comfy_script.runtime.real import *
load()
#load(args=ComfyUIArgs(['--highvram']))
#load(args=ComfyUIArgs(['--lowvram']))
#load(args=ComfyUIArgs(['--force-fp32']))

from comfy_script.runtime.real.nodes import *


sys.path.insert(0, '../../')
import folder_paths

import comfy.model_management
import torch

####################
# Randomize script #
####################

# TODO
# use SAG with delayed activation together with self-scaling CFG
# https://www.reddit.com/r/comfyui/comments/1aqoj9w/i_tried_my_hand_at_a_selfrescaling_cfg_what_do/?sort=new
# wait for merge

#Calculate max CFG based on negative token weights to avoid artifacts
# have seperate foreground/background prompts?
# use embedding keyword instead of full path
# https://github.com/Jordach/comfy-plasma
# multi regional prompt using colors
# force garbage collection
# https://civitai.com/models/140552/comfyui-detailed-ksampler
# use tome patch model, hypertile and perpneg?
# sigmas_tools_and_the_golden_scheduler?
# image save options in yaml
# gui?? probably not
# random vae?
# control what model the clip is coming from

yaml_file = 'randomize.yml'

# load and get settings from yaml file
yaml_path = os.path.realpath(os.path.join(os.getcwd(), yaml_file))
with open(yaml_path, 'r') as file:
    try:
        data = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)

#files
checkpoints = [x for x in folder_paths.get_filename_list("checkpoints")]
loras = [x for x in folder_paths.get_filename_list("loras")]
embeddings = [x for x in folder_paths.get_filename_list("embeddings")]

# prints all files to console, useful for copying and pasting to yaml file
if len(sys.argv) >= 2 and sys.argv[1] == 'list':
    print ('checkpoints:')
    [print("    " + x) for x in checkpoints]
    print ('loras:')
    [print("    " + x) for x in loras]
    print ('embeddings:')
    [print("    " + x) for x in embeddings]
    sys.exit()

def apply_weights_positive_prompt(prompt, primary_prompt):
    tokens = prompt.split(", ")
    weighted_tokens = ""
    for token in tokens:
        if primary_prompt in token:
            token_weighting_values = data['positive_prompt']['primary_prompt_weight_values'] 
        else:
            token_weighting_values = data['positive_prompt']['token_weighting_values']
        weighted_tokens += "(" + token + ":" + str(get_float_from_value_string(token_weighting_values)) + "), "
    return weighted_tokens

def replace_questionmarks_positive_prompt(prompt, primary_prompt):
    tokens = prompt.split(", ")
    weighted_tokens = ""
    for token in tokens:
        if primary_prompt in token:
            token_weighting_values = data['positive_prompt']['primary_prompt_weight_values']   
        else:
            token_weighting_values = data['positive_prompt']['token_weighting_values']
        weighted_tokens += token.replace('?', str(get_float_from_value_string(token_weighting_values)))
    return weighted_tokens

def apply_weights_negative_prompt(prompt):
    tokens = prompt.split(", ")
    weighted_tokens = ""
    token_weighting_values = data['negative_prompt']['token_weighting_values']
    for token in tokens:          
        weighted_tokens += "(" + token + ":" + str(get_float_from_value_string(token_weighting_values)) + "), "
    return weighted_tokens

def replace_questionmarks_negative_prompt(prompt):
    token_weighting_values = data['negative_prompt']['token_weighting_values']
    return prompt.replace('?', str(get_float_from_value_string(token_weighting_values)))

def get_random_tokens(prompt_data):
    tokens = prompt_data['random_tokens'].split(', ')
    add_token_chance = prompt_data['random_token_chance']
    token_string = ""
    for token in tokens:
        random_number = random.randint(0, 100)
        if random_number <= add_token_chance:
            token_string += ", " + token
    return token_string

def FeelingLucky(prompt):
    generator = RandomPromptGenerator()
    lucky_generator = FeelingLuckyGenerator(generator)
    prompt = lucky_generator.generate(prompt, 1)
    print(prompt)
    return prompt[0]

def magicprompt(prompt):
    generator = RandomPromptGenerator()
    device_ = data['positive_prompt']['magicprompt']['device']
    mp_model = data['positive_prompt']['magicprompt']['model']
    magic_generator = MagicPromptGenerator(generator, mp_model, device=device_)
    prompt = magic_generator.generate(prompt, 1)
    print(prompt)
    return prompt[0]

def get_positive_prompt():
    mode = data['positive_prompt']['token_weighting_mode']
    primary_prompt = data['positive_prompt']['prompt']
    prompt = primary_prompt
    if data['positive_prompt']['use_feelinglucky'] == True:
        prompt += get_random_tokens(data['positive_prompt']) # will get error from lexica.art if using same search every time
        prompt = FeelingLucky(prompt)
    if data['positive_prompt']['magicprompt']['use'] == True:
        prompt = magicprompt(prompt)
    prompt += get_random_tokens(data['positive_prompt'])
    weight_values = data['positive_prompt']['token_weighting_values']
    if mode == 'all':
        prompt = apply_weights_positive_prompt(prompt, primary_prompt)
    if mode == 'replace_questionmark':
        prompt = replace_questionmarks_positive_prompt(prompt, primary_prompt)
    return prompt + get_embeddings('positive')

def get_negative_prompt():
    mode = data['negative_prompt']['token_weighting_mode']
    prompt = data['negative_prompt']['prompt']
    prompt += get_random_tokens(data['negative_prompt'])
    weight_values = data['negative_prompt']['token_weighting_values']
    if mode == 'all':
        prompt = apply_weights_negative_prompt(prompt)
    if mode == 'replace_questionmark':
        prompt = replace_questionmarks_negative_prompt(prompt)
    return prompt + get_embeddings('negative')
    
def get_embeddings(allingment):
    string = ""
    for embedding in embeddings:
        if allingment == embedding['alignment'] or embedding['alignment'] == 'both':
            random_number = random.randint(0, 100)
            if random_number <= embedding['chance']:
                string += "(embedding:" + embedding['name'] + ":" + str(get_float_from_value_string(embedding['values'])) + "), " 
    return string
    
def get_randomvariate(mu, sigma, min_, max_):
    random_number = random.normalvariate(mu, sigma)
    random_number = round(random_number, 2)
    random_number = min(random_number, max_)
    random_number = max(random_number, min_)
    return random_number

def handle_output():
    if data['output']['add_time_and_date_suffix']  == True:
        folder_name = data['output']['output_folder_name'] + '_{date:%Y-%m-%d_%H-%M-%S}'.format( date=datetime.datetime.now() )
    else:
        folder_name = data['output']['output_folder_name']
    path = os.path.join(folder_paths.output_directory, folder_name)
    os.makedirs(path)
    return path

def get_float_from_value_string(value_string):
    value_list = value_string.split(', ')
    if value_list[0] == 'value':
        return float(value_list[1])
    if value_list[0] == 'range':
        random_number = random.uniform(float(value_list[1]), float(value_list[2]))
        random_number = round(random_number, 2)
        return random_number
    if value_list[0] == 'normal_variate_range':
        return get_randomvariate(value_list[1], value_list[2], value_list[3], value_list[4])

def get_merge_candidates(max):
    merge_candidates = []
    random.shuffle(checkpoints)
    for checkpoint in checkpoints:
        random_number = random.randint(0, 100)
        if random_number >= checkpoint['merge_chance']:
            merge_candidates.append(checkpoint)
        if len(merge_candidates) == max:
            return merge_candidates        
    return merge_candidates

def get_candidate(merge_candidates):
    candidate = random.choice(merge_candidates)
    merge_candidates.remove(candidate)
    return candidate

def get_random_checkpoint():
    random_candidates = []
    for checkpoint in checkpoints:
        if checkpoint['state'] != 'never':
            random_candidates = random_candidates + checkpoint
    return random.choice(random_candidates)['name']

def parse_freeu_string(string_list):
    if string_list[0] == 'standard':
        return string_list[1], string_list[2], string_list[3], string_list[4]
    if string_list[0] == 'range':
        b1 = random.uniform(float(string_list[1]), float(string_list[2]))
        b2 = random.uniform(float(string_list[3]), float(string_list[4]))
        s1 = random.uniform(float(string_list[5]), float(string_list[6]))
        s2 = random.uniform(float(string_list[7]), float(string_list[8]))
        return b1, b2, s1, s2
    if string_list[0] == 'normal_variate_range':
        b1 = get_randomvariate(string_list[1], string_list[2], string_list[3], string_list[4])
        b2 = get_randomvariate(string_list[5], string_list[6], string_list[7], string_list[8])
        s1 = get_randomvariate(string_list[9], string_list[10], string_list[11], string_list[12])
        s2 = get_randomvariate(string_list[13], string_list[14], string_list[15], string_list[16])
        return b1, b2, s1, s2

def get_workflow():
    workflows = data['workflow']['workflows'].split(', ')
    weights = data['workflow']['workflow_weights']
    workflow = random.choices(workflows, weights=weights, k=1)
    if workflow[0].find('_lcm') == -1:
        lcm_workflow = False
    else:
        lcm_workflow = True
    return workflow[0], lcm_workflow

def filter_checkpoints(workflow):
    filtered_checkpoints = []
    for m in data['checkpoints']['checkpoints']:
        type_string_list = m['type'].split(', ')
        if workflow in type_string_list:
            filtered_checkpoints.append(m)
    return filtered_checkpoints

def filter_loras(workflow):
    filtered_loras = []
    for m in data['loras']['loras']:
        type_string_list = m['type'].split(', ')
        if workflow in type_string_list:
            filtered_loras.append(m)
    return filtered_loras

def filter_embeddings(workflow):
    filtered_embeddings = []
    for m in data['embeddings']:
        type_string_list = m['type'].split(', ')
        if workflow in type_string_list:
            filtered_embeddings.append(m)
    return filtered_embeddings

def get_ksampler_settings():
    #seed
    if data['seed']['values'] == 'random':
        seed = random.randint(1, 1125899906842624)
    else:
        seed = data['seed']['values']
    #steps
    steps = int(get_float_from_value_string(data['steps']['values']))
    # cfg
    cfg = get_float_from_value_string(data['cfg']['values'])
    # sampler
    if lcm_workflow == True:
        sampler = data['sampler']['lcm_sampler']
        steps = int(get_float_from_value_string(data['sampler']['lcm_sampler']['steps']))
        cfg = get_float_from_value_string(data['sampler']['lcm_sampler']['cfg'])
        sampler = 'lcm'
    else:
        if data['sampler']['mode'] == 'default':
            sampler = data['sampler']['default_sampler'] 
        else:
            weights = []
            samplers = data['sampler']['samplers']
            for sampler in samplers:
                weights.append(sampler['weight'])
            sampler = random.choices(samplers, weights=weights, k=1)
            sampler = sampler[0]
            if sampler['override_steps_and_cfg'] == True:
                steps = int(get_float_from_value_string(sampler['steps']))
                cfg = get_float_from_value_string(sampler['cfg'])
            sampler = sampler['name']
    # scheduler
    if data['scheduler']['values'] == 'random':
        scheduler = random.choice(data['scheduler']['schedulers'])
    else:
        scheduler = data['scheduler']['values']
    # denoise
    denoise = get_float_from_value_string(data['denoise']['values'])
    return seed, steps, cfg, sampler, scheduler, denoise
    
path = handle_output()
for i in range(data['output']['images']):
    workflow, lcm_workflow = get_workflow()
    # filter models based on workflow
    checkpoints = filter_checkpoints(workflow)
    loras = filter_loras(workflow)
    embeddings = filter_embeddings(workflow)
    
    #with Workflow():
    with torch.inference_mode():
        comfy.model_management.unload_all_models()
        # checkpoint
        mode = data['checkpoints']['mode'].split(', ')
        if mode[0] == 'merge_checkpoints':
            merge_candidates = get_merge_candidates(int(mode[1]))
            print('merge_candidates: ', len(merge_candidates))
            if len(merge_candidates) == 0: # use default checkpoint
                model, clip, vae = CheckpointLoaderSimple(data['checkpoints']['default'])    
            elif len(merge_candidates) == 1: # no merging, use the sole candidate
                model, clip, vae = CheckpointLoaderSimple(merge_candidates[0]['name'])  
            else:
                candidate = get_candidate(merge_candidates)    
                model1, clip, vae = CheckpointLoaderSimple(candidate['name']) 
                #model1 = TomePatchModel(model1, 0.3)
                #unload_all_models_except(model1)
                candidate = get_candidate(merge_candidates)    
                model2, clip, vae = CheckpointLoaderSimple(candidate['name']) 
                #model2 = TomePatchModel(model2, 0.3)    
                model = ModelMergeBlocks(model1, model2, random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                #unload_all_models_except(model)
               # comfy.model_management.unload_model_clones(model1)
               # comfy.model_management.unload_model_clones(model2)
                del model1
                del model2
                comfy.model_management.soft_empty_cache()
                #merge_list = [model]
                while len(merge_candidates) > 0:
                    candidate = get_candidate(merge_candidates)
                    model2, clip, vae = CheckpointLoaderSimple(candidate['name'])  
                    #model2 = TomePatchModel(model2, 0.3)    
                    #merge_list.append(ModelMergeBlocks(merge_list[0], model2, random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
                    model = ModelMergeBlocks(model, model2, random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
                #  unload_all_models_except(model)
                 #   comfy.model_management.unload_model_clones(merge_list.pop(0))
                 #   comfy.model_management.unload_model_clones(model2)
                    del model2
                    comfy.model_management.soft_empty_cache()
                #model = merge_list[0]
        if data['checkpoints']['mode'] == 'random':
            model, clip, vae = CheckpointLoaderSimple(get_random_checkpoint()) 
        if data['checkpoints']['mode'] == 'default':
            model, clip, vae = CheckpointLoaderSimple(data['checkpoints']['default'])  

        # freeu
        freeu_string = data['freeu']['values'].split(', ')
        random_float = random.uniform(0,1)
        if random_float <= float(freeu_string[-1]):
            b1, b2, s1, s2 = parse_freeu_string(freeu_string)
            model = FreeUV2(model, b1, b2, s1, s2)

        # dynamic_thresholding
        #random_float = random.randint(0, 100)
        #if random_float <= data['dynamic_thresholding']['chance']:
        #    mimic_scale = int(get_float_from_value_string(data['dynamic_thresholding']['mimic_scale']))
        #    threshold_percentile = get_float_from_value_string(data['dynamic_thresholding']['threshold_percentile'])
        #    model = DynamicThresholdingSimple(model, mimic_scale, threshold_percentile)
            
        # auto cfg
        random_float = random.randint(0, 100)
        if random_float <= data['automaticcfg']['chance']:
            model = AutomaticCFG(model)

        # CLIP Set Last Layer
        clip = CLIPSetLastLayer(clip, int(get_float_from_value_string(data['clipsetlastlayer']['values'])))
        
        # loras
        for lora in loras:
            random_number = random.randint(0, 100)
            if lora['chance'] >= random_number:    
                strength_model = get_float_from_value_string(lora['strength_model'])
                strength_clip = get_float_from_value_string(lora['strength_clip'])
                model, clip = LoraLoader(model, clip, lora['name'], strength_model, strength_clip)

        # prompt
        pos_cond = CLIPTextEncode(get_positive_prompt(), clip)
        neg_cond = CLIPTextEncode(get_negative_prompt(), clip)

        # encode, decode and ksampler
        if workflow == 'xl' or workflow == 'xl_lcm':
            latent = EmptyLatentImage(data['output']['size_x_xl'], data['output']['size_y_xl'], 1)
        else:
            latent = EmptyLatentImage(data['output']['size_x_sd1_5'], data['output']['size_y_sd1_5'], 1)
 
        seed, steps, cfg, sampler, scheduler, denoise = get_ksampler_settings()
        latent = KSampler(model, seed, steps, cfg, sampler, scheduler, pos_cond, neg_cond, latent, denoise)
        #latent = KSampler(model, 1, 18, 2.26, 'dpmpp_2m', 'karras', pos_cond, neg_cond, latent, 1.0)
        image = VAEDecode(latent, vae)

        del model
        del latent
        del clip
        del vae
        comfy.model_management.soft_empty_cache()
        

        ImageSave( # workflow will not be included in webp file, possible fix pending
        image, # images: Image,
        path, # output_path: str = '[time(%Y-%m-%d)]',
        'ComfyUI', #filename_prefix: str = 'ComfyUI',
        '_', #filename_delimiter: str = '_',
        4, #filename_number_padding: int = 4,
        'false', #filename_number_start: ImageSave.filename_number_start = 'false',
        'png', #extension: ImageSave.extension = 'png',
        100, #quality: int = 100,
        'false', #lossless_webp: ImageSave.lossless_webp = 'false',
        'false', #overwrite_mode: ImageSave.overwrite_mode = 'false',
        'false', #show_history: ImageSave.show_history = 'false',
        'true', #show_history_by_prefix: ImageSave.show_history_by_prefix = 'true',
        'true', #embed_workflow: ImageSave.embed_workflow = 'true',
        'true', #show_previews: ImageSave.show_previews = 'true'
        )
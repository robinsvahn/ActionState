
import os
import numpy as np
from scipy.io import loadmat
import json
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from save_in_proper_json_format import add_caption_and_save_in_proper_format
from calculate_AUROC import calculate_AUROC

def get_pictures(folder_path):
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    return jpg_files


def read_mat_file(file_path):
    # Load the .mat file
    data = loadmat(file_path)
    
    # Return label
    return data["action"][0]


def save_dict(dict, name):
    # Save the dictionary to a JSON file
    with open("data" + "/" + name + ".json", "w") as json_file:
        json.dump(dict, json_file, indent=4)

def fetch_dict(name):
    # Load the dictionary from a JSON file
    with open("data" + "/" + name + ".json", "r") as json_file:
        return json.load(json_file)

def retrieve_and_save_tuples():
        frame_path = r"../penn_action/frames"
        label_path = r"../penn_action/labels"

        action_tuples = {}

        for label_folder, frame_folder in zip(os.listdir(label_path), os.listdir(frame_path)):

            # Get action label and all frames.
            action = read_mat_file(label_path + "/" + label_folder)
            frames = get_pictures(frame_path + "/" + frame_folder)
            
            # Filter to start, middle and end frames
            start, middle, end = frames[0], frames[int(len(frames) / 2)], frames[-1]

            # add relative path to frames so they can easily be retrieved at a later stage. 
            # I.e. we only retrieve a path reference of the frames. 
            start_path = frame_path + "/" + frame_folder + "/" + start
            middle_path = frame_path + "/" + frame_folder + "/" + middle
            end_path = frame_path + "/" + frame_folder + "/" + end

            # Save tuples in list with their respective action label as the key.
            action_tuples.setdefault(action, []).append([start_path, middle_path, end_path])
        
        small_batch = {key: action_tuples[key][:10] for key in action_tuples.keys()}
        save_dict(dict=action_tuples, name="action_tuples_all")
        save_dict(dict=small_batch, name="action_tuples_small_batch")

def plot_tuples(category: list):
    for tuple in category:
        # Create a 3x1 subfigure layout
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Adjust figsize as needed

        for i, img_path in enumerate(tuple):
            # Load and display the image in the corresponding subplot
            img = mpimg.imread(img_path)
            axes[i].imshow(img)
            axes[i].axis('off')  # Turn off axes for better visualization
            #axes[i].set_title(f"Image {i+1}")  # Optional: Add a title for each image

        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.show()

def filter_categories(dict, to_keep):
    filtered_dict = {key: value for key, value in dict.items() if key in to_keep}
    return filtered_dict

def calc_category_action(json_file, model_name=None, unimodal=False, manual=True, small_keys=None):

    baseball_pitch = {"start": [] , "middle": [], "end": []}
    baseball_swing = {"start": [] , "middle": [], "end": []}
    golf_swing = {"start": [] , "middle": [], "end": []}
    tennis_forehand = {"start": [] , "middle": [], "end": []}
    tennis_serve = {"start": [] , "middle": [], "end": []} 
    
    category_patterns = [
        ("baseball pitch", baseball_pitch),
        ("baseball swing", baseball_swing),
        ("golf swing", golf_swing),
        ( "tennis forehand", tennis_forehand),
         ("tennis serve", tennis_serve)
    ]
    if not manual: #Filter llm-results to only be the (150) same instances as in the manual results
        json_file = {k: json_file[k] for k in small_keys if k in json_file}

    last_two_words_pattern = r'(\b\w+\b)[^\w]+(\b\w+\b)\s*$'
    for key, value in json_file.items():
        category = re.search(last_two_words_pattern, value["caption"]).group()
        for pattern, dict in category_patterns:
            if pattern == category:
                stage = value["classes"]

                if manual:
                    acc = value["mturk"]["caption"] / 6 # 6 evaluators
                    dict[stage].append(acc)
                else:
                    if unimodal:
                        print("category: ", category)
                        print("stage: ", stage)
                        print("value: ", value[model_name]["caption"])
                        print("--------------------")
                        dict[stage] = value[model_name]["caption"]
                    else:
                        if value[model_name]["caption"] > value[model_name]["foil"]:
                            dict[stage].append(1)
                        else: 
                            dict[stage].append(0)

    
    final_result = {}
    for name, cat in category_patterns:
        final_result[name] = {}

        for stage, vals in cat.items():
            if unimodal:
               final_result[name][stage] = vals 
            else:
                stage_avg = sum(vals) / len(vals)

                final_result[name][stage] = stage_avg
                
    return final_result
if __name__ == "__main__":
    def main():
        #This is already been run, and needs only to be run again if we want to change which frames are retrieved.
        """retrieve_and_save_tuples() """

        # I suggest to use these actions because they are actions of sequential nature, I.e. they have a clear start / during / end status.
        # But, before actually removing other categories lets look at picture tuples of all categories from small batch.
        """ action_to_keep = ["baseball_pitch", "baseball_swing", "golf_swing", "tennis_forehand", "tennis_serve"] # Add categories/actions that we want to use here
        needs_to_be_vetted = ["tennis_forehand", "baseball_swing"] # Is useable, but looks to have some unclear/bad examples 

        dev_batch = fetch_dict("action_tuples_small_batch")
        full_batch = fetch_dict("action_tuples_all")
        
        dev_batch_filtered = filter_categories(dev_batch, action_to_keep)
        full_batch_filtered = filter_categories(full_batch, action_to_keep)
        """

        # Uncomment this if we want to change how/what is being saved in the properly formatted json-files.
        """dev_batch_properly_formatted = add_caption_and_save_in_proper_format(dev_batch_filtered)
        full_batch_properly_formatted = add_caption_and_save_in_proper_format(full_batch_filtered)
        
        save_dict(dev_batch_properly_formatted, "temporal_stage_small")
        save_dict(full_batch_properly_formatted, "temporal_stage")"""

        # CALCULATE AUROC METRIC (VALSE repository doesn't do this apparently)

        #1. resaving results because the VALSE authors did it horribly
        """results = fetch_dict("plurals-mini")
        save_dict(results, "plurals-mini_properly_formatted")
        """
        #2. Ok now actually calculating it
        """llm_results = fetch_dict("temporal_stage_results_properly_formatted")
        AUROC_metrics = calculate_AUROC(llm_results)
        print("auroc: ", AUROC_metrics)
        """

        # CALCULATE PAIRWISE ACCURACY FOR DISTINCT CATEGORIES AND STAGES

        # on manual categorizations
        """manual_vals = fetch_dict("temporal_stage_small_w_ishaan_toby")
        manual_results = calc_category_action(manual_vals)
        save_dict(manual_results, "manual_results")"""

        #On llm (lxmert/) 
        """llm_results = fetch_dict("temporal_stage_results_properly_formatted")
        manual_vals_keys = fetch_dict("temporal_stage_small_w_ishaan_toby").keys()
        all_keys = fetch_dict("temporal_stage_results_properly_formatted").keys()
        llm_results = calc_category_action(llm_results, "lxmert", manual=False, small_keys=all_keys)
        save_dict(llm_results, "llm_results_all")"""
        

        # CALCULATE PERPLEXITY FOR DISTINCT CATEGORIES AND STAGES

        # On llm (gpt1)
        
        """llm_results = fetch_dict("temporal_stage_gpt1_perplexity")
        #manual_vals_keys = fetch_dict("temporal_stage_small_w_ishaan_toby").keys()
        all_keys = fetch_dict("temporal_stage_results_properly_formatted").keys()
        llm_results = calc_category_action(llm_results, "gpt1", manual=False, unimodal=True, small_keys=all_keys)
        save_dict(llm_results, "llm_gpt1_perplexity_results_all")"""

        # On llm (gpt2)

        """llm_results = fetch_dict("temporal_stage_gpt2_perplexity")
        #manual_vals_keys = fetch_dict("temporal_stage_small_w_ishaan_toby").keys()
        all_keys = fetch_dict("temporal_stage_results_properly_formatted").keys()
        llm_results = calc_category_action(llm_results, "gpt2", manual=False, unimodal=True, small_keys=all_keys)
        save_dict(llm_results, "llm_gpt2_perplexity_results_all")"""




        


        #TODO 
        # Save all pictures in json-format compatible with VALSE repo. (TO BE REVIEWED AND TESTED)
        #   Add caption and other info available, let non-available values (e.g. foil) be None.
        #       Non available info will be added later. 

        # Read up on how to foil, then create script to add foiled captions to all images. (TO BE REVIEWED)

        # Create annotation script for (3) annotaters to decide whether caption or foil (or both(?)) describes the image.



    
    

    

    

        

  

if __name__ == "__main__":
    main()
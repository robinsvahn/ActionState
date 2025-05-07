# TODO 
# 1. Fetch pictures
# 2. Remove useless categories
# 3. Filter to triplets (first on small batch)
# 4. Run on full dataset (seperate categories and make indexing stable (0,1,2))
# 5. Copy small batch to use as sample for development and testing
# 6. save sample and full batch seperately

import os
from scipy.io import loadmat
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from save_in_proper_json_format import add_caption_and_save_in_proper_format

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



if __name__ == "__main__":
    def main():
        #This is already been run, and needs only to be run again if we want to change which frames are retrieved.
        """retrieve_and_save_tuples() """

        # I suggest to use these actions because they are actions of sequential nature, I.e. they have a clear start / during / end status.
        # But, before actually removing other categories lets look at picture tuples of all categories from small batch.
        action_to_keep = ["baseball_pitch", "baseball_swing", "golf_swing", "tennis_forehand", "tennis_serve"] # Add categories/actions that we want to use here
        needs_to_be_vetted = ["tennis_forehand", "baseball_swing"] # Is useable, but looks to have some unclear/bad examples 

        dev_batch = fetch_dict("action_tuples_small_batch")
        full_batch = fetch_dict("action_tuples_all")
        
        dev_batch_filtered = filter_categories(dev_batch, action_to_keep)
        full_batch_filtered = filter_categories(full_batch, action_to_keep)


        # Uncomment this if we want to change how/what is being saved in the properly formatted json-files.
        """dev_batch_properly_formatted = add_caption_and_save_in_proper_format(dev_batch_filtered)
        full_batch_properly_formatted = add_caption_and_save_in_proper_format(full_batch_filtered)
        
        save_dict(dev_batch_properly_formatted, "temporal_stage_small")
        save_dict(full_batch_properly_formatted, "temporal_stage")"""


        #TODO 
        # Save all pictures in json-format compatible with VALSE repo. (TO BE REVIEWED AND TESTED)
        #   Add caption and other info available, let non-available values (e.g. foil) be None.
        #       Non available info will be added later. 

        # Read up on how to foil, then create script to add foiled captions to all images. (TO BE REVIEWED)

        # Create annotation script for (3) annotaters to decide whether caption or foil (or both(?)) describes the image.



    
    

    

    

        

  

if __name__ == "__main__":
    main()
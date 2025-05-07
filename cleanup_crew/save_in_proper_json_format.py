import re

def add_caption_and_save_in_proper_format(batch):
    action_stage_dataset = {}
    stage_nr = ["start", "middle", "end"]
    foils = {"start": ["middle", "end"], "middle": ["start", "end"], "end": ["start", "middle"]}
    for i, category in enumerate(batch.keys()):
        action = re.sub("_", " ", category)
        for m, tuple in enumerate(batch[category]):
            for j, stage in enumerate(tuple):
                key = f"actionstage_{stage_nr[j]}_{category}_{m}"
                bool = m % 2 == 0
                foil = foils[stage_nr[j]][bool]
                value = {
                    "dataset": "Penn_Action",
                    "dataset_idx": stage[-15:-4],
                    "image_file": stage, 
                    "linguistic_phenomena": "Temporal stages",
                    "caption": f"The person is at the {stage_nr[j]} stage of a {action}",
                    "classes": stage_nr[j],
                    "classes_foil": foil, #<-- Add stage used for foil here.
                    "mturk": { #<-- In total 3 votes.
                        "foil": 0, # how many annotators voted that the foil describes the image
                        "caption": 0, # how many annotators voted that the caption only (and not the foil) to describe the image                
                        "other": 0
                    },
                    "foil": f"The person is at the {foil} stage of a {action}" 
                }
                action_stage_dataset[key] = value

    return action_stage_dataset
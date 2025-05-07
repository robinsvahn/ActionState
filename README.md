# ActionStages
Start, middle, end

# Action categories
"baseball_pitch", "baseball_swing", "golf_swing", "tennis_forehand", "tennis_serve"

# Research question
Can a VLM differentiate between different stages of the same action?

    We will try to answer this looking specifically at ball-sport actions.

# image caption
The person is at the <start/middle/end> stage of a <action>"

# Foiling procedure
For all captions describing and certain action stage, the correct stage is switched 50/50 with the two other stages.
I.e. given the image-caption:
    "The person is at the start stage of a baseball pitch"

    foil is 50% of the time:
        "The person is at the middle stage of a baseball pitch"
    
    else:
        "The person is at the end stage of a baseball pitch"

So, the foils are balanced, plausible and syntactically correct. 

# caption-foil validation
The image-caption-foil tuples will be manually annotated as either:
- The foil and only the foil correctly describes the image
- The caption and only the caption correctly describes the image
- Both are plausible descriptions of the image

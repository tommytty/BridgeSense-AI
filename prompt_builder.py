# prompt_builder.py — Construct the Analysis Prompt
# ===================================================
# TODO: Write a function called `build_prompt` that:
#   - Takes the UDP_PRINCIPLES list as input
#   - Returns a string prompt that instructs Claude to:
#       1. Analyze a bridge image for accessibility features
#       2. Score each principle from 1-5
#       3. List detected features
#       4. Provide 3-5 improvement recommendations
#       5. Respond in JSON format
#
# This is the heart of your project — spend time crafting this well!
#
# Hint: Define the exact JSON schema you want Claude to return, e.g.:
# {
#     "overall_score": 3.5,
#     "principles": [
#         {"id": 1, "name": "...", "score": 4, "reasoning": "..."},
#         ...
#     ],
#     "detected_features": ["ramp", "handrail", ...],
#     "recommendations": ["Add tactile paving...", ...]
# }

def build_prompt(principles):
    # TODO: Build and return your prompt string
    pass

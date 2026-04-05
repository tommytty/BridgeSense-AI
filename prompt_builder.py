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
    prompt = "You are an accessibility evaluator specializing in universal design, specifically the 7 Universal Design Principles" \
    " You are extremely knowledgeable on every nook and cranny of a bridge, and you must give me comprehensive review of the bridge based on the following" \
    " Principles that I will list down here"
    
    for p in principles:
        prompt += f"\n{p['id']}. {p['name']}: {p['description']}\n"
        prompt += "Look for:\n"
        for criteria in p['bridge_criteria']:
            prompt += f"- {criteria}\n"
            
    
    prompt += """
                Now that the principles are listed and you know what to look for, 
                analyze and rate them on a scale of 0-5 and also give comprehensive 
                explanations on why you think that score is appropriate.

                Please return the response as JSON only, using this exact format:

                {
                    "overall_score": 3.5,
                    "principles": [
                        {"id": 1, "name": "...", "score": 4, "reasoning": "..."}
                    ],
                    "detected_features": ["ramp", "handrail"],
                    "recommendations": ["Add tactile paving..."]
                }

                Respond with JSON only. Do not include any other text.
                """
    return prompt
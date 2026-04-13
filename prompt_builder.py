# prompt_builder.py — Construct the Analysis Prompt


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

def build_criteria(principles):

    prompt = """
                Before anything, you will check if the picture is a bridge or not. IF the picture is not a bridge, please
                disregard the rest of the prompt and just return in this exact JSON format:
                {"is_bridge" : false, "message" : "The uploaded image does not appear to be a bridge."} 

                If the picture is a bridge, please continue with the prompt! 

                You are an expert at bridge analysis. When you are sent pictures of bridges,
                you analyze the picture and identify what type of bridge it is, what it is used for, 
                the typical users of such bridge, the context of why this bridge was built, why it was built,
                and how it was built, what the goal of the bridge was. the history, the very essence of the reasoning behind
                why this bridge exists. And with as much context and information you have about the bridge as possible,
                you are to create a bridge criteria unique to each picture of the bridges that are sent, so that the person doing the 
                evaluation based on these criterias will do it with as much context as possible to give the most accurate and 
                precise estimations on how that bridge follows the 7 UDP
            """

    for p in principles:
        prompt += f"\n{p['id']}. {p['name']}: {p['description']}\n"
    

    prompt += """ Now that the 7 UDP principle have been given to you, you must return them with the criteria you have come up with in this exact JSON format
    
    {
    "is_bridge": true,
    "principles": [
        {"id": 1, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]},
        {"id": 2, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]},
        {"id": 3, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]},
        {"id": 4, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]},
        {"id": 5, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]},
        {"id": 6, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]},
        {"id": 7, "name": "...", "description": "...", "bridge_criteria": ["...", "..."]}
    ],
    "bridge_type": "...",
    "typical_users": "...",
    "context_summary": "...",
    "reasoning": "...",
}
    
    """
    prompt += """ You may come up with a minimum of three for each one and based on the context of certain bridges, you can 
                  create a maximum of five criterias for each principle
                  
                  Please also tell us what you think the bridge_type is, who the typical users are, and the context summary.
                  In reasoning, please explain why you came to the conclusions to those answers.
                  
                  Based on the bridge TYPE and TYPICAL USERS you identified, 
                  generate criteria that represent what an ideal accessible bridge of this type would have. 
                  These criteria should be aspirational standards — what SHOULD be present for maximum accessibility — 
                  NOT descriptions of what this specific bridge already has. The Evaluator will later check whether the bridge meets these standards, 
                  so the criteria must be able to reveal both strengths AND weaknesses.

                  Please also try and identify the name and location of the bridge in the picture and give a identification confidence level of 0-100%. 

            
                  Respond with JSON only. Do not include any other text
                  """
    
    return prompt
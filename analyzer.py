# analyzer.py — Core Image Analysis
# ====================================
# TODO: Write a function called `analyze_bridge` that:
#   1. Takes an image file path as input
#   2. Reads the image and base64-encodes it (use base64 module + open())
#   3. Detects the image MIME type (jpeg, png, etc.)
#   4. Calls the Anthropic API with the image + your prompt
#   5. Parses the JSON from Claude's response
#   6. Returns the parsed dict
#
# You'll need:
#   import anthropic
#   import base64
#   import json
#
# The API call pattern:
#   client = anthropic.Anthropic(api_key=your_key)
#   message = client.messages.create(
#       model=your_model,
#       max_tokens=4096,
#       messages=[{"role": "user", "content": [...]}]
#   )
#   response_text = message.content[0].text
#
# Don't forget error handling — what if the image doesn't exist?
# What if Claude doesn't return valid JSON?

def analyze_bridge(image_path):
    # TODO: implement
    pass

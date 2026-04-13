# analyzer.py — Core Image Analysis
import anthropic
import base64
import json
import prompt_builder
import mimetypes
from PIL import Image
from config import API_KEY, MODEL
from udp_principles import UDP_PRINCIPLES
from bridge_profiler import bridge_profiler


def analyze_bridge(image_path, principles):
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    base64_string = base64.b64encode(image_data).decode("utf-8")
    with Image.open(image_path) as img:
        mime_type = f"image/{img.format.lower()}"
    prompt = prompt_builder.build_prompt(principles)
    client = anthropic.Anthropic(api_key=API_KEY)
    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": mime_type, "data": base64_string}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    response_text = message.content[0].text
    response_text = response_text.replace("```json", "").replace("```", "").strip() 
    result = json.loads(response_text)
    return result

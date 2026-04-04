# BridgeSense AI — Core Analysis Engine

An AI-powered bridge accessibility evaluator using Claude's vision capabilities
and the 7 Universal Design Principles.

## Project Structure

```
bridgesense-ai/
├── README.md              ← You are here
├── requirements.txt       ← Python dependencies
├── config.py              ← API key + model settings (YOU BUILD)
├── udp_principles.py      ← The 7 UDP definitions + scoring criteria (YOU BUILD)
├── prompt_builder.py      ← Constructs the analysis prompt (YOU BUILD)
├── analyzer.py            ← Sends image to Claude API, parses response (YOU BUILD)
├── report.py              ← Formats the structured report output (YOU BUILD)
├── main.py                ← CLI entry point — ties it all together (YOU BUILD)
└── sample_images/         ← Drop test bridge images here
```

## How to Build (Step by Step)

### Step 1: Setup & Config (`config.py`)
- Store your Anthropic API key (use environment variables, never hardcode!)
- Set the model name: `claude-sonnet-4-20250514`
- Tip: `os.environ.get("ANTHROPIC_API_KEY")` is your friend

### Step 2: Define the Principles (`udp_principles.py`)
- Create a data structure (dict or list of dicts) holding all 7 UDP principles
- Each principle needs: name, description, and what to look for on a bridge
- Example structure:
  ```python
  UDP_PRINCIPLES = [
      {
          "id": 1,
          "name": "Equitable Use",
          "description": "The design is useful and marketable to people with diverse abilities.",
          "bridge_criteria": [
              # What would you look for? Think ramps, alternative routes, etc.
          ]
      },
      # ... 6 more
  ]
  ```

### Step 3: Build the Prompt (`prompt_builder.py`)
- Write a function that takes your UDP principles and returns a system prompt
- The prompt should instruct Claude to:
  - Analyze a bridge image for accessibility features
  - Score each of the 7 principles from 1-5
  - Detect specific features (ramps, surfaces, railings, signage, etc.)
  - Return a structured JSON response
- This is the MOST IMPORTANT file. The quality of your prompt = the quality of your analysis.
- Tip: Ask Claude to respond in JSON format with a specific schema you define

### Step 4: Core Analyzer (`analyzer.py`)
- Write a function that:
  1. Reads an image file and base64-encodes it
  2. Calls the Anthropic API with your prompt + the image
  3. Parses the JSON response
  4. Returns a structured result dict
- Use the `anthropic` Python SDK — it's cleaner than raw HTTP
- Key API pattern:
  ```python
  message = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=4096,
      messages=[{
          "role": "user",
          "content": [
              {"type": "image", "source": {"type": "base64", ...}},
              {"type": "text", "text": your_prompt}
          ]
      }]
  )
  ```

### Step 5: Report Formatter (`report.py`)
- Takes the raw analysis dict and prints a readable report
- Show: overall score, per-principle scores, detected features, recommendations
- Start simple (print to terminal), get fancy later

### Step 6: CLI Entry Point (`main.py`)
- Accept an image path as a command-line argument
- Wire together: load image → build prompt → analyze → format report
- Use `argparse` or `sys.argv`

## Quick Start (once you've built it)

```bash
export ANTHROPIC_API_KEY="your-key-here"
pip install -r requirements.txt
python main.py sample_images/pedestrian_bridge.jpg
```

## The 7 Universal Design Principles (Reference)

1. **Equitable Use** — Useful to people with diverse abilities
2. **Flexibility in Use** — Accommodates a wide range of preferences
3. **Simple and Intuitive Use** — Easy to understand regardless of experience
4. **Perceptible Information** — Communicates info effectively to the user
5. **Tolerance for Error** — Minimizes hazards and adverse consequences
6. **Low Physical Effort** — Can be used efficiently and comfortably
7. **Size and Space for Approach and Use** — Appropriate size and space for use

## Next Steps (after MVP works)

- [ ] Add a web interface (Flask or FastAPI)
- [ ] Support multiple images per bridge
- [ ] Generate PDF reports
- [ ] Add before/after conceptual redesigns
- [ ] Batch analysis mode
"# BridgeSense-AI" 

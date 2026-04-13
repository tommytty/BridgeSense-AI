# BridgeSense AI

**An AI-powered bridge accessibility evaluator using multi-agent LLM chaining and the 7 Universal Design Principles.**

Built by Tommy Tang as a personal project during the Diploma of Computer Systems Technology at BCIT.

---

## What It Does

BridgeSense AI takes a photograph of a bridge and produces a structured accessibility audit against the 7 Universal Design Principles. It identifies the bridge, classifies it by type and typical users, generates context-aware evaluation criteria, scores the bridge against those criteria, and outputs actionable recommendations for improving accessibility.

Unlike traditional accessibility audits, which require expert site visits and manual assessment, BridgeSense AI delivers a preliminary evaluation in under a minute from a single image.

## Architecture

The core technical contribution of this project is a **two-agent AI pipeline** rather than a single-shot prompt.

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────┐
│  React UI    │────▶│  FastAPI Server  │────▶│ Profiler Agent   │────▶│ Evaluator    │
│  (Vite)      │◀────│     (api.py)     │◀────│ (Claude Vision)  │────▶│ Agent        │
└──────────────┘     └──────────────────┘     └──────────────────┘     └──────────────┘
                                                      │                         │
                                                      ▼                         ▼
                                              Classifies bridge,      Scores bridge against
                                              generates tailored      generated criteria,
                                              evaluation criteria     outputs UDP report
```

**Agent 1 — The Profiler:** Classifies the bridge type (pedestrian, highway, railway, etc.), predicts typical users, gathers context, and generates aspirational accessibility criteria tailored to that specific bridge type. A highway bridge and a pedestrian hiking bridge get different yardsticks.

**Agent 2 — The Evaluator:** Takes the image and the Profiler's tailored criteria, then scores the bridge against each of the 7 Universal Design Principles with reasoning and produces targeted improvement recommendations.

### Why Two Agents Instead of One?

The original design used a single API call with hardcoded criteria, but this produced context-blind evaluations — a highway bridge and a pedestrian walkway were judged by the same standards. Splitting the work across two agents with separate responsibilities produced significantly more context-aware and actionable output.

A key design flaw surfaced during development: the Profiler initially generated criteria that *described* what the image already contained (e.g., "has multiple lanes"), effectively rigging the evaluation to pass. Fixing this required explicitly prompting the Profiler to generate **aspirational standards** — what an ideal accessible bridge of this type *should* have — rather than descriptions of what was visible. This is noted in the project as a reminder that multi-agent systems can fail in subtle, systemic ways.

## Tech Stack

**Backend**
- Python 3.13
- FastAPI for the HTTP API
- Anthropic Python SDK (Claude Sonnet 4 for vision + reasoning)
- Pillow for image handling and MIME detection
- Uvicorn as the ASGI server

**Frontend**
- React 18 (Vite)
- Vanilla CSS with design tokens (no UI framework)
- Native Fetch API with FormData for file uploads
- Custom engineering-themed dark UI with monospace data labels, grid background, and subtle animations

## Project Structure

```
BridgeSense AI/
├── backend/
│   ├── api.py                 # FastAPI entry point
│   ├── bridge_profiler.py     # Agent 1 — image analysis & criteria generation
│   ├── analyzer.py            # Agent 2 — UDP scoring
│   ├── prompt_builder.py      # Prompt construction for both agents
│   ├── udp_principles.py      # Base UDP principle templates
│   ├── config.py              # Environment & model config
│   ├── report.py              # Terminal report formatter (CLI mode)
│   ├── main.py                # CLI entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component (all state + views)
│   │   ├── App.css            # Dark engineering-themed styling
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An Anthropic API key

### Backend

```bash
cd backend
python -m pip install -r requirements.txt

# Set your API key (Windows PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."

# Run the API server
python -m uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### CLI Mode

The backend also supports a command-line interface for direct terminal analysis:

```bash
cd backend
python main.py path/to/bridge_image.jpg
```

## API Endpoints

### `POST /analyze`

Analyzes a bridge image. Accepts a multipart form with a `file` field.

**Response (success):**
```json
{
  "profile": {
    "is_bridge": true,
    "bridge_name": "Victoria Falls Bridge",
    "bridge_location": "Zambezi River between Zambia and Zimbabwe",
    "identification_confidence": "95%",
    "bridge_type": "...",
    "typical_users": "...",
    "context_summary": "...",
    "reasoning": "...",
    "principles": [ /* 7 tailored principles with criteria */ ]
  },
  "analysis": {
    "overall_score": 3.4,
    "principles": [ /* 7 scored principles with reasoning */ ],
    "detected_features": [ "..." ],
    "recommendations": [ "..." ]
  }
}
```

**Response (not a bridge):** `400 Bad Request`
```json
{ "detail": "The uploaded image does not appear to be a bridge." }
```

## Key Design Decisions

- **Image MIME detection via Pillow** rather than file extensions, because users upload mislabeled files (e.g., `.jpg` files that are actually WebP).
- **Structured JSON schemas** in every prompt, with explicit "respond with JSON only" instructions and markdown fence stripping on the response side to handle Claude's occasional formatting.
- **Decoupled analyzer** that accepts any `principles` parameter rather than importing a hardcoded list — this enables swapping criteria sources (Profiler output vs. hardcoded) and future experimentation.
- **Graceful non-bridge rejection** through a profiler-level `is_bridge` flag, short-circuiting the pipeline before running the more expensive evaluator.
- **CORS + ephemeral temp files** on the backend so uploaded images are cleaned up even when exceptions occur.

## Known Limitations

- **Bridge identification is best-effort.** Claude's vision can identify major landmarks but may hallucinate names for lesser-known bridges. Confidence scores help communicate this uncertainty.
- **Single-angle analysis.** Each evaluation is based on one image. A real audit would need multiple angles and supplementary data (lighting conditions, surface material specs, etc.).
- **No persistence.** Results are not saved between sessions. Adding a simple database for a history feature is a natural next step.
- **API costs scale with usage.** Each analysis makes two API calls. Budget accordingly for production deployment.

## Future Work

- Progressive loading messages (Profiling → Analyzing) with real backend status, not timers
- EXIF metadata extraction to improve bridge identification accuracy
- PDF report export
- Batch analysis mode
- A judging agent that validates Profiler criteria before handing them to the Evaluator (reflection pattern)
- Support for multiple images per bridge

## License

Personal project — not licensed for commercial use.

## Acknowledgements

Built with Claude (Anthropic) as both the AI backend and a pair-programming collaborator during development.

# BridgeSense AI

> **[→ Try the live demo](https://bridge-sense-ai.vercel.app)** — upload a bridge photo, get an accessibility audit in under a minute.

A multi-agent LLM system that evaluates bridge accessibility against the 7 Universal Design Principles. Built with Claude as both the AI backend and a pair-programming collaborator.

> **Heads up:** The backend runs on a free Render instance that spins down after inactivity. Your first request might take 30–60 seconds while the server wakes up. Subsequent requests are fast.

---

## The Pitch

Most accessibility audits require trained inspectors, site visits, and weeks of turnaround. BridgeSense AI takes a single photograph and produces a structured evaluation — identification, classification, per-principle scoring, and concrete improvement recommendations — in well under a minute.

It's not a replacement for expert review. It's a screening tool that flags issues, prioritizes sites, and surfaces design considerations that might otherwise go unnoticed.

The bridges themselves aren't really the point of the project. The point is the **system design** — a working pattern for multi-agent LLM evaluation that could be pointed at almost any subject (public transit stations, playgrounds, storefronts, anything where Universal Design matters).

## Architecture

Two specialized Claude agents chained together, each with a focused responsibility:

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

**Profiler Agent.** Classifies the bridge type, predicts typical users, gathers context, and generates *aspirational* accessibility criteria tailored to that specific type. A highway bridge and a hiking footbridge get different yardsticks.

**Evaluator Agent.** Receives the image plus the Profiler's tailored criteria. Scores against each of the 7 Universal Design Principles, surfaces detected features, and produces targeted improvement recommendations.

The two agents are **decoupled by design**. The Evaluator accepts any `principles` parameter — it doesn't import a hardcoded list. This means criteria sources can be swapped, profilers can be A/B tested, and the orchestration logic stays clean.

## Why Two Agents Instead of One?

The first version used a single API call with hardcoded criteria. It produced context-blind evaluations — a highway bridge and a pedestrian walkway were judged by the same standards, and the output read like a generic accessibility checklist.

Splitting the work into specialized agents produced significantly more context-aware output. The Profiler can spend its prompt budget thinking about bridge type and user demographics without polluting the scoring step. The Evaluator can focus on rigorous judgment without re-deriving context. Each agent has a smaller, cleaner job.

The **decoupled architecture** also makes evaluation possible. Comparing single-agent vs. multi-agent outputs on the same image is a one-line change in `main.py`. That kind of substitutability matters when you start caring about output quality empirically rather than vibes.

## The Bug That Almost Wasn't a Bug

The most interesting thing I learned building this had nothing to do with multi-agent orchestration. It was a subtle failure mode that *looked* like the system was working perfectly.

The original Profiler was generating criteria like *"has multiple vehicle lanes"* or *"has a cable-stayed structure"* — things it was literally seeing in the image it was looking at. The Evaluator would then score against those criteria, see the same features, and give the bridge full marks.

**Both agents were looking at the same image. The Profiler was inadvertently rigging the exam.**

The bridge always passed because the criteria were descriptions of what was already there. The system produced thorough-looking JSON reports that were quietly useless. From the outside everything looked fine — the issue only surfaced when I started running the same bridges and noticing scores were suspiciously high regardless of obvious accessibility gaps.

The fix was in the Profiler's prompt. I added explicit language requiring **aspirational standards** — what an ideal accessible bridge of this type *should* have — and forbidding descriptions of what the specific bridge contained. Now the criteria can reveal real strengths and weaknesses. The bridge can actually fail.

This is the kind of failure mode you don't see coming with single-agent systems, because there's no boundary between "context gathering" and "evaluation" — they're the same prompt. Multi-agent systems make these dependencies *visible*, but they don't fix them automatically. You still have to design for the right behaviors.

I think about this bug a lot. It's the strongest argument I have that evaluation frameworks aren't optional for production LLM systems — they're how you catch the system being confidently wrong.

## Why Claude?

I built this with Claude Sonnet 4 (Anthropic) rather than GPT-4o or Gemini. A few specific reasons, in priority order:

1. **Structured JSON output is more reliable.** Both agents communicate via JSON schemas, and GPT-4o has a stronger tendency to wrap its output in markdown fences or add prose preambles. Claude follows "respond with JSON only" instructions more consistently. For agent-to-agent communication, parse reliability matters more than raw capability.

2. **Vision quality is comparable, but reasoning quality is noticeably better for this task.** When asked to generate criteria, Claude's outputs are more specific and measurable ("minimum 8 feet pedestrian walkway width") rather than generic ("wide enough for everyone"). That difference compounds across both agents.

3. **The API is straightforward.** Image base64 + text message in a single content block is clean and well-documented. No model-specific quirks around tool calling or function schemas getting in the way of a simple vision request.

4. **Honest reasons:** I have good API access through Anthropic, and Claude has been my main pair-programming tool throughout BCIT. I know its failure modes well enough to design around them.

The whole pipeline is model-agnostic by design. Swapping in a different vision model would be a config change, not a refactor. But if I were building this for production today, I'd stay with Claude for the inter-agent communication layer specifically.

## Tech Stack

**Backend** — Python 3.13, FastAPI, Anthropic Python SDK, Pillow (image handling + real MIME detection from bytes, not file extensions), Uvicorn, deployed on Render.

**Frontend** — React 18 + Vite, vanilla CSS with design tokens, native Fetch API with FormData uploads. No UI framework — wanted full control over the dark engineering aesthetic. Deployed on Vercel.

**Inter-service** — CORS-protected REST API with environment-based URL resolution. The frontend reads `VITE_API_URL` from environment variables, so the same codebase works against local and deployed backends.

The whole thing lives in about 400 lines of Python and 300 lines of JSX.

## Running It Locally

```bash
# Backend
cd backend
python -m pip install -r requirements.txt
$env:ANTHROPIC_API_KEY="sk-ant-..."   # PowerShell
python -m uvicorn api:app --reload

# Frontend (separate terminal)
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

Visit `http://localhost:5173`.

## API Endpoint

### `POST /analyze`

Multipart form with a `file` field containing the bridge image.

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

Non-bridge images return a `400` with a friendly message instead of running the more expensive evaluator.

## Engineering Notes

A few decisions worth calling out:

- **MIME detection from bytes, not extensions.** Pillow opens the image and reports its actual format. Users upload mislabeled files (`.jpg` files that are secretly WebP); trusting extensions caused real production errors during testing.
- **Profiler-level rejection of non-bridge images.** The `is_bridge` flag short-circuits the pipeline before the more expensive evaluator runs. Saves cost and produces a better error UX.
- **Ephemeral temp files with `try/finally` cleanup.** Uploaded images are deleted even when exceptions occur partway through processing. Important for a long-running service.
- **No state between requests.** Each analysis is independent. Made the deployment story trivial — no database, no session management, no migrations.
- **Graceful handling of upstream API errors.** Anthropic's `OverloadedError` (529) and other API failures get translated to user-friendly `503` and `500` responses with messages, not stack traces.

## What I'd Build Next

If I kept working on this:

- **A judge agent.** A third Claude call that validates the Profiler's criteria *before* they reach the Evaluator. If the judge finds criteria that are descriptive rather than aspirational, it sends them back for revision. This is the reflection pattern, and it's the natural extension of the bug story above.
- **A proper eval suite.** Right now I evaluate the pipeline by uploading bridges and reading the output. Production would need a corpus of bridges with known accessibility scores and automated regression testing.
- **EXIF geolocation.** Phone-taken photos include GPS coordinates. Feeding those into the Profiler would dramatically improve bridge identification accuracy for non-landmark bridges.

## Built With Claude

I used Claude as my pair-programming partner throughout this project. The architecture decisions and the code are mine — every line went through my understanding — but Claude was the rubber duck I argued with about design choices, the syntax reference I checked CSS specificity questions against, and the tutor I asked when I needed to learn React's `useState` model from scratch.

My favorite part of working with it is exactly what's in the bug story above. Claude is useful enough that you can ship things you don't fully understand, but it's also a mirror — it gives you back what you give it. The Profiler self-grading bug existed because *my prompt* was sloppy, not because Claude failed. Once I learned to think more carefully about what I was asking for, the system got dramatically better. That feedback loop is how I'd rather work for the rest of my career.

---

**Built by Tommy Tang — Diploma of Computer Systems Technology, BCIT (2026)**
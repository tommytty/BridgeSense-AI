# api.py — FastAPI backend wrapper for BridgeSense AI

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import anthropic

from bridge_profiler import bridge_profiler
from analyzer import analyze_bridge

app = FastAPI()

# CORS — allows your React frontend (running on a different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "BridgeSense AI API is running"}

@app.post("/analyze")
async def analyze_endpoint(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        profile = bridge_profiler(temp_path)
        if not profile.get("is_bridge", True):
            raise HTTPException(status_code=400, detail=profile.get("message", "Not a bridge"))
        result = analyze_bridge(temp_path, profile["principles"])
        return {"profile" : profile, "analysis": result}
    except HTTPException:
        raise  # re-raise HTTPExceptions so FastAPI handles them normally
    except anthropic.APIStatusError as e:
        if e.status_code == 529:
            raise HTTPException(status_code=503, detail="AI service is temporarily overloaded. Please try again.")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
    finally:
        os.remove(temp_path)
from fastapi import FastAPI, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional
import uvicorn
from detector import detect_voice

app = FastAPI()

# Pydantic models
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

class VoiceResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

class ErrorResponse(BaseModel):
    status: str
    message: str

# API Key (Hardcoded for demo, normally env var)
VALID_API_KEY = "AI_DETECT"

@app.post("/api/voice-detection", response_model=VoiceResponse)
async def voice_detection(
    request: VoiceRequest,
    x_api_key: Optional[str] = Header(None)
):
    # Authenticate
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail={"status": "error", "message": "Invalid API key or malformed request"})

    # Validate inputs
    if request.audioFormat.lower() != "mp3":
         raise HTTPException(status_code=400, detail={"status": "error", "message": "Only mp3 format is supported"})

    if not request.audioBase64:
         raise HTTPException(status_code=400, detail={"status": "error", "message": "Missing audio data"})

    # Analyze
    result = detect_voice(request.audioBase64)
    
    # Construct response
    return VoiceResponse(
        status="success",
        language=request.language,
        classification=result["classification"],
        confidenceScore=result["confidenceScore"],
        explanation=result["explanation"]
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    # If detail is a dict, return it directly to match strict error format if needed
    if isinstance(exc.detail, dict):
         return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "message": str(exc.detail)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

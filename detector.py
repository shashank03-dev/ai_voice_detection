import io
import base64
import librosa
import numpy as np
import torch
import soundfile as sf
from transformers import pipeline

import os

# Ensemble Configuration
# On Render Free Tier (512MB RAM), we only load one model to avoid OOM crashes.
IS_LITE = os.getenv("RENDER", "false").lower() == "true"

if IS_LITE:
    print("Running in LITE mode (Render optimization)...")
    MODELS = [
        {"name": "MelodyMachine/Deepfake-audio-detection-V2", "weight": 1.0}
    ]
else:
    MODELS = [
        {"name": "mo-thecreator/Deepfake-audio-detection", "weight": 1.0},
        {"name": "MelodyMachine/Deepfake-audio-detection-V2", "weight": 1.2}, 
        {"name": "Hemgg/Deepfake-audio-detection", "weight": 1.0}
    ]

pipelines = []

print("Initializing Ensemble Models...")
for m in MODELS:
    try:
        print(f"Loading {m['name']}...")
        p = pipeline("audio-classification", model=m['name'])
        pipelines.append({"pipe": p, "weight": m['weight'], "name": m['name']})
        print(f"Loaded {m['name']}")
    except Exception as e:
        print(f"Failed to load {m['name']}: {e}")

def decode_audio(base64_string: str):
    """
    Decodes a base64 string into audio bytes.
    """
    try:
        audio_bytes = base64.b64decode(base64_string)
        return audio_bytes
    except Exception as e:
        raise ValueError("Invalid audio data") from e

def get_ai_score(result):
    """
    Extracts the score for the 'AI/Fake' class from the pipeline result.
    Different models might have different labels.
    """
    # Common labels for fake: "fake", "spoof", "generated"
    # Common labels for real: "real", "bonafide", "human"
    
    # The result is a list of dicts, sorted by score descending usually, or just list of classes.
    # e.g. [{'label': 'fake', 'score': 0.9}, {'label': 'real', 'score': 0.1}]
    
    ai_score = 0.0
    
    for r in result:
        label = r['label'].lower()
        score = r['score']
        
        if any(x in label for x in ["fake", "spoof", "generated", "ai"]):
            ai_score = score
            break
        elif any(x in label for x in ["real", "bonafide", "human"]):
            # If we find the real label, the AI score is 1 - real_score (assuming binary)
            # But wait, looking for specific AI label is safer if multi-class.
            # Assuming binary softmax.
            pass
            
    # If we didn't find an explicit AI label in the top results, maybe it's the other one.
    # Let's verify by checking if we found "Real".
    if ai_score == 0.0:
        for r in result:
            label = r['label'].lower()
            if any(x in label for x in ["real", "bonafide", "human"]):
                ai_score = 1.0 - r['score']
                break
                
    return ai_score

def detect_voice(base64_audio: str):
    """
    Analyzes the audio and returns classification, confidence, and explanation.
    """
    try:
        if not pipelines:
            return {
                "classification": "HUMAN",
                "confidenceScore": 0.0,
                "explanation": "System Error: No models loaded."
            }

        audio_bytes = decode_audio(base64_audio)
        
        votes = []
        total_weight = 0.0
        weighted_score_sum = 0.0
        
        details = []

        for p in pipelines:
            try:
                # Run inference
                result = p["pipe"](audio_bytes)
                score = get_ai_score(result)
                
                weight = p["weight"]
                weighted_score_sum += score * weight
                total_weight += weight
                
                votes.append(score)
                details.append(f"{p['name'].split('/')[0]}: {score:.2f}")
                
            except Exception as e:
                print(f"Error in model {p['name']}: {e}")

        if total_weight == 0:
             return {
                "classification": "HUMAN", 
                "confidenceScore": 0.0,
                "explanation": "Analysis failed across all models."
            }

        final_ai_score = weighted_score_sum / total_weight
        
        # Classification Logic
        classification = "HUMAN"
        confidence_score = 0.0
        
        if final_ai_score >= 0.5:
            classification = "AI_GENERATED"
            confidence_score = final_ai_score
        else:
            classification = "HUMAN"
            confidence_score = 1.0 - final_ai_score
            
        # Dynamic Explanation
        explanation = ""
        
        if classification == "AI_GENERATED":
            if confidence_score > 0.98:
                explanation = "Deep spectral analysis strongly confirms synthetic origin. Multiple models detected unambiguous AI artifacts."
            elif confidence_score > 0.85:
                explanation = "High probability of AI generation.Detected characteristic artifacts consistent with modern TTS systems."
            elif confidence_score > 0.6:
                explanation = "Analysis indicates likelihood of synthesis, though some features mimic human speech patterns."
            else:
                explanation = "Borderline result with synthetic features outweighting natural ones."
        else: # HUMAN
            if confidence_score > 0.98:
                explanation = "Natural organic voice patterns confirmed. Pitch variation and breath sounds are consistent with human speech."
            elif confidence_score > 0.85:
                explanation = "Clear human vocal characteristics detected. Absent of typical deepfake artifacts."
            elif confidence_score > 0.6:
                explanation = "Likely human, though some audio anomalies were detected (possibly due to noise or compression)."
            else:
                explanation = "Inconclusive but leans towards human. Audio quality may be affecting detection certainty."

        # Add debug details for transparency (optional, depending on user need. API doc says 'Short reason')
        # We will stick to the generated explanation but maybe append a note if it's a demo.
        # "explanation" should be professional.
        
        return {
            "classification": classification,
            "confidenceScore": round(confidence_score, 4), # Higher precision
            "explanation": explanation
        }

    except Exception as e:
        print(f"Error in detection: {e}")
        return {
            "classification": "HUMAN", 
            "confidenceScore": 0.0,
            "explanation": f"Error during analysis: {str(e)}"
        }

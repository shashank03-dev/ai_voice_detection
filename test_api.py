import requests
import base64
import os
import glob
import json

API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = "AI_DETECT"

def test_file(filepath):
    print(f"\nTesting {filepath}...")
    try:
        with open(filepath, "rb") as f:
            audio_data = f.read()
            b64_audio = base64.b64encode(audio_data).decode("utf-8")
        
        payload = {
            "language": "English", # Defaulting to English for test, API creates response based on input
            "audioFormat": "mp3",
            "audioBase64": b64_audio
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Find all mp3 files in current directory
    mp3_files = glob.glob("*.mp3")
    if not mp3_files:
        print("No MP3 files found in current directory.")
        return

    print(f"Found {len(mp3_files)} MP3 files. Starting tests...")
    
    for mp3 in mp3_files:
        test_file(mp3)

if __name__ == "__main__":
    main()

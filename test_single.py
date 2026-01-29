import requests
import base64
import sys
import os
import json

API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = "AI_DETECT"

def test_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    print(f"\nTesting {filepath}...")
    try:
        with open(filepath, "rb") as f:
            audio_data = f.read()
            b64_audio = base64.b64encode(audio_data).decode("utf-8")
        
        payload = {
            "language": "English", # Language is just metadata for this API
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_single.py <path_to_mp3_file>")
        print("Example: python3 test_single.py human.mp3")
        sys.exit(1)
        
    filepath = sys.argv[1]
    test_file(filepath)

from transformers import pipeline
import time

def try_load(model_name):
    print(f"Testing load for: {model_name}")
    try:
        start = time.time()
        pipe = pipeline("audio-classification", model=model_name)
        print(f"Success! Loaded in {time.time() - start:.2f}s")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

models = [
    "MelodyMachine/Deepfake-audio-detection-V2",
    "Hemgg/Deepfake-audio-detection",
    "AshishBIS/Speech_Deepfake_Detection_Wav2vec2_Large"
]

for m in models:
    try_load(m)

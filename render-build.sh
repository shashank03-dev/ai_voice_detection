#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Any other build steps (e.g., pre-downloading models if needed)
# python -c "from transformers import pipeline; pipeline('audio-classification', model='MelodyMachine/Deepfake-audio-detection-V2')"

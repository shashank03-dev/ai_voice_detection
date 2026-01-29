# AI Voice Detection API

This project implements a robust REST API for detecting AI-generated voice samples. It uses an **Ensemble of 3 State-of-the-Art Deep Learning Models** to achieve high accuracy and provide detailed explanations.

## Features

- **Ensemble Detection**: Combines predictions from 3 different Hugging Face models.
- **Dynamic Explanations**: Provides context-aware reasons for classification.
- **Format Support**: Accepts Base64 encoded MP3 files.
- **Language Support**: Optimized for Tamil, English, Hindi, Malayalam, Telugu.

## Prerequisites

- Python 3.8+
- `ffmpeg` (Required for audio processing)

## Installation

1. **Install System Dependencies (Linux/Ubuntu)**:

   ```bash
   sudo apt update && sudo apt install ffmpeg -y
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API Server

Start the FastAPI server using `uvicorn`:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`.

## Testing

### Automated Test Script

We have provided a script `test_api.py` that automatically finds all `.mp3` files in the current directory and tests them against the API.

```bash
python3 test_api.py
```

### Manual Testing (cURL)

You can verify the API manually using `curl`:

```bash
curl -X POST http://localhost:8000/api/voice-detection \
-H "Content-Type: application/json" \
-H "x-api-key: AI_DETECT" \
-d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "<YOUR_BASE64_STRING_HERE>"
}'
```

## API Documentation

Once the server is running, you can access the interactive API docs at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

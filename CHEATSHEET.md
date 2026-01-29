# AI Voice Detection API - Cheatsheet

Here are the essential commands you need to run and test this project on your own.

## 1. Setup (First Time Only)

Ensure you are in the project directory:

```bash
cd /home/user/detect
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
python3 -m pip install pyngrok
```

## 2. Running the System

You will typically need **two terminal windows** open.

### Terminal 1: Start the API Server

This must be running for the API to work.

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

_Wait until you see "Application startup complete"._

### Terminal 2: Expose to Internet (For Submission/External Test)

Run this if you need a public URL (like `https://...ngrok-free.app`) to submit to the form.

```bash
python3 expose_api.py
```

_Copy the "Public URL" from the output._

## 3. Testing (Local)

You can run these in Terminal 2 while the server is running in Terminal 1.

**Test with all provided samples:**

```bash
python3 test_api.py
```

**Test a specific file:**

```bash
python3 test_single.py human.mp3
```

## 4. Deployment to Render (24/7 Online)

To host your API 24/7 for free:

1.  **Push to GitHub:** Upload your project folder to a GitHub repository.
2.  **Create Service on Render:**
    - Log in to [Render.com](https://dashboard.render.com).
    - Click **New +** > **Web Service**.
    - Connect your GitHub repository.
3.  **Configure Settings:**
    - **Runtime:** `Python 3`
    - **Build Command:** `./render-build.sh`
    - **Start Command:** `gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app`
4.  **Environment Variables (CRITICAL):**
    - Click **Environment** tab on Render.
    - Add Key: `RENDER`, Value: `true` (This enables "Lite" mode to fit in the 512MB RAM).
    - Add Key: `PYTHON_VERSION`, Value: `3.9.0` (or your preferred version).

## 5. Submission Details

When filling out the evaluation form:

- **Endpoint URL:** `https://your-app-name.onrender.com/api/voice-detection`
- **API Key:** `AI_DETECT`

from pyngrok import ngrok
import time
import sys

# Define the port your FastAPI is running on
PORT = 8000

try:
    # Open a HTTP tunnel on the default port 8000
    # Note: If you have an auth token, you can set it with:
    # ngrok.set_auth_token("YOUR_AUTHTOKEN")
    
    public_url = ngrok.connect(PORT).public_url
    print(f"\n\n========================================================")
    print(f" * Public URL: {public_url}")
    print(f" * API Endpoint: {public_url}/api/voice-detection")
    print(f"========================================================\n\n")
    print("Keep this script running to keep the tunnel open.")
    
    # Keep the script running
    while True:
        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")
    print("\nIf you see an error about missing Authtoken, sign up at ngrok.com")
    print("and run: ngrok config add-authtoken <token>")

from flask import Flask, jsonify, request, Response
import threading
import requests
import uvicorn
from screenshot_service import app as fastapi_app

FASTAPI_PORT = 8000

# Start FastAPI in a separate thread
def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=FASTAPI_PORT)

threading.Thread(target=run_fastapi, daemon=True).start()

app = Flask(__name__)

# Health check endpoint
@app.route('/')
def health():
    return jsonify({"status": "alive"})

# Reverse proxy for /screenshot
@app.route('/screenshot')
def screenshot_proxy():
    url = request.args.get("url")
    full_page = request.args.get("full_page", "false")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    fastapi_url = f"http://127.0.0.1:{FASTAPI_PORT}/screenshot?url={url}&full_page={full_page}"
    try:
        r = requests.get(fastapi_url, stream=True)
        return Response(r.content, content_type=r.headers.get('content-type'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

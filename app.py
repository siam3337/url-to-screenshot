from flask import Flask, jsonify, request, Response
import subprocess
import requests
import os

# Start FastAPI screenshot service in background (port 8000)
subprocess.Popen(["python", "helper.py"])

app = Flask(__name__)
FASTAPI_PORT = 8000

# Health check endpoint
@app.route('/')
def health():
    return jsonify({"status": "alive"})

# Reverse proxy for screenshot
@app.route('/screenshot')
def screenshot_proxy():
    url = request.args.get("url")
    full_page = request.args.get("full_page", "false")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    # Forward request to FastAPI
    fastapi_url = f"http://127.0.0.1:{FASTAPI_PORT}/screenshot?url={url}&full_page={full_page}"
    try:
        r = requests.get(fastapi_url, stream=True)
        return Response(r.content, content_type=r.headers.get('content-type'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, jsonify
import subprocess
import os

# Start the actual screenshot service in background
subprocess.Popen(["python", "helper.py"])

app = Flask(__name__)

@app.route('/')
def index():
    # Respond immediately for health check
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

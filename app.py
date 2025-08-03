from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

LOG_FILE = "claim_log.json"

@app.route("/")
def index():
    try:
        with open(LOG_FILE, "r") as f:
            claim_log = json.load(f)
    except FileNotFoundError:
        claim_log = []
    return render_template("index.html", claim_log=claim_log)

@app.route("/api/logs")
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            claim_log = json.load(f)
    except FileNotFoundError:
        claim_log = []
    return jsonify(claim_log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ✅ THIS FIXES YOUR ERROR

API_URL = "https://api-inference.huggingface.co/models/coqui/XTTS-v2"
HEADERS = {"Authorization": "Bearer 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"}

@app.route("/")
def home():
    return "Voice Cloning Backend Running"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        voice = request.files["voice"]
        text = request.form["text"]

        response = requests.post(
            API_URL,
            headers=HEADERS,
            data={"inputs": text},
            files={"audio": voice}
        )

        if response.status_code != 200:
            return f"API Error: {response.text}"

        with open("output.wav", "wb") as f:
            f.write(response.content)

        return send_file("output.wav", mimetype="audio/wav")

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

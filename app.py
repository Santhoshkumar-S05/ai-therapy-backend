from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import torch

app = Flask(__name__)
CORS(app)

# Load emotion classification model
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

# Route to handle emotion detection
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_input = data.get("text", "")

    if not user_input:
        return jsonify({"error": "No input text provided."}), 400

    result = emotion_classifier(user_input)[0]
    emotion = result['label']
    score = result['score']

    return jsonify({"emotion": emotion, "confidence": round(score, 2)})

if __name__ == '__main__':
    print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")
    app.run(debug=True)

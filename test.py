from flask import Flask, send_file, request, jsonify
from dotenv import load_dotenv
import os
import cohere

# Load environment variables from .env
load_dotenv()

# Get Cohere API key from .env
cohere_api_key = os.getenv("COHERE_API_KEY")

if not cohere_api_key:
    raise ValueError("Cohere API key not found. Did you create and set COHERE_API_KEY in the .env file?")

# Initialize Cohere client
co = cohere.Client(cohere_api_key)

# Setup Flask app
app = Flask(__name__)

from flask import send_file

@app.route("/")
def home():
    return send_file("index.html")


@app.route("/chatbot")
def chatbot():
    return send_file("chatbot.html")

@app.route("/input")
def input():
    return send_file("input.html")

@app.route("/api", methods=["POST"])
def chat():
    message = request.form.get("message")
    if not message:
        return jsonify({"error": "No message received"}), 400

    try:
        response = co.generate(
            model="command-light",
            prompt=message,
            max_tokens=100
        )
        return jsonify({"content": response.generations[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
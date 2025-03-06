from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "OPTIONS"]}})
client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

def verify_claim(claim):
    context = [
        {"role": "system", "content": "You are an expert fact-checker."},
        {"role": "user", "content": f"Fact-check the following claim and provide a credibility score (0-10) with reasoning:\n\n{claim}"},
          ]
    response = client.chat.completions.create(

        model = "gpt-4o-mini-2024-07-18",
        messages = context,
        max_tokens = 500,
        temperature = 0)
    
    response_msg = response.choices[0].message.content
    return response_msg

@app.route('/fact-check', methods=['POST', 'OPTIONS'])
def fact_check():
    # Handle the preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200  # Accept OPTIONS request

    data = request.json
    claim = data.get("claim", "")

    if not claim:
        return jsonify({"error": "No claim provided"}), 400

    result = verify_claim(claim)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)

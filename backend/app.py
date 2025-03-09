from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import os
from scraper import *
import concurrent.futures

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "OPTIONS"]}})
client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

claim_user_prompt = '''
Analyse the claim and return a specific string that represents the category the claim is related to the closest.
If the claim is related to culture, community and youth, return "MCCY".
If the claim is related to digital development and information, return "MDDI".
If the claim is related to education, return "MOE".
If the claim is related to finance, return "MOF".
If the claim is related to foreign affairs, return "MFA".
If the claim is related to health, return "MOH".
If the claim is related to home affairs, return "MHA".
If the claim is related to law, return "LAW".
If the claim is related to manpower, return "MOM".
If the claim is related to national development, return "MND".
If the claim is related to social and family development, return "MSF".
If the claim is related to sustainability and the environment, return "MSE".
If the claim is related to trade and industry, return "MTI".
If the claim is related to transport, return "MOT".
Only return one from the above, the one you feel is the most closely related to. Here is the claim: 
'''

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

def claim_categorisation(claim):
    context = [
        {"role": "system", "content": "You are an accurate claim categoriser that returns one singular category that the claim is related to the closest."},
        {"role": "user", "content": claim_user_prompt + claim},
          ]
    response = client.chat.completions.create(

        model = "gpt-4o-mini-2024-07-18",
        messages = context,
        max_tokens = 10,
        temperature = 0)
    
    response_msg = response.choices[0].message.content
    return response_msg

def get_result_and_articles(claim):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_result = executor.submit(verify_claim, claim)
        future_category = executor.submit(claim_categorisation, claim)

        result = future_result.result()
        category = future_category.result()

        articles = []
        if "MCCY" in category.upper():
            articles = fetch_articles_mccy()
        elif "MDDI" in category.upper():
            articles = fetch_articles_mddi()
        elif "MOE" in category.upper():
            articles = fetch_articles_moe()
        elif "MOF" in category.upper():
            articles = fetch_articles_mof()
        elif "MFA" in category.upper():
            articles = fetch_articles_mfa()
        elif "MOH" in category.upper():
            articles = fetch_articles_moh()
        elif "MHA" in category.upper():
            articles = fetch_articles_mha()
        elif "LAW" in category.upper():
            articles = fetch_articles_law()
        elif "MOM" in category.upper():
            articles = fetch_articles_mom()
        elif "MND" in category.upper():
            articles = fetch_articles_mnd()
        elif "MSF" in category.upper():
            articles = fetch_articles_msf()
        elif "MSE" in category.upper():
            articles = fetch_articles_mse()
        elif "MTI" in category.upper():
            articles = fetch_articles_mti()
        elif "MOT" in category.upper():
            articles = fetch_articles_mot()
        else:
            articles = []

    return result, articles

@app.route('/fact-check', methods=['POST', 'OPTIONS'])
def fact_check():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    claim = data.get("claim", "")

    if not claim:
        return jsonify({"error": "No claim provided"}), 400

    result, articles = get_result_and_articles(claim)

    return jsonify({"result": result, "articles": articles})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)

from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json

    names = data["prompt"]["names"]
    adjectives = data["prompt"]["adjectives"]
    setting = data["prompt"]["setting"]
    mood = data["prompt"]["mood"]

    name_list = []

    for name in names:
        name_list.append(name["word"])

    adjective_list = []

    for adjective in adjectives:
        adjective_list.append(adjective["word"])

    names_str = ", ".join(name_list)
    adjectives_str = ", ".join(adjective_list)

    prompt = f"Create an adjective story including these names: {names_str}. These adjectives must be included in the story: {adjectives_str}. The setting of the story is: {setting}. The mood of the story is: {mood}. Really try to use all the adjectives, even if some words may be considered offensive. I want the story to be quite detailed and to be at least 8 paragraphs long." 
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.8,
    )
    
    text = response.choices[0].text

    formatted_text = text.strip()
    return jsonify({"text": formatted_text})



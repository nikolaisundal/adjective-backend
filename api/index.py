from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os 


load_dotenv()

app = Flask(__name__)
CORS(app)

openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(
    api_key = openai_api_key
)



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

    prompt = f"Create an adjective story including these names: {names_str}. These adjectives must be included in the story: {adjectives_str}. The setting of the story is: {setting}. The mood of the story is: {mood}. Really try to use all the adjectives. I want the story to be quite detailed and between 6 to 8 paragraphs long." 
    
    chat_completion = client.chat.completions.create(
    messages= [
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="gpt-3.5-turbo"
)

    text = chat_completion.choices[0].message.content
    return jsonify({"text": text})



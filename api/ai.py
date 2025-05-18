from flask import Blueprint, jsonify, make_response, request
from openai import OpenAI
import anthropic
import os

open_ai = Blueprint('open_ai', __name__, url_prefix='/api/v1/ai')

OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=OPENAI_KEY)

@open_ai.route("/askOpenAI", methods=['POST'])
def openAI():
    data = request.json
    answer =  client.chat.completions.create(   
        model="gpt-4",
        messages=[
            {"role": "system", "content": data['prompt']},
        ],
    )
    response = make_response(
        jsonify({"answer": answer.choices[0].message.content}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    
    return response


@open_ai.route("/askClaude", methods=['POST'])
def claude():
    CLAUDE_KEY = os.getenv("CLAUDE_KEY")
    print(CLAUDE_KEY)
    data = request.json
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": data['prompt']}
        ]
    )
    return message.content[0].text

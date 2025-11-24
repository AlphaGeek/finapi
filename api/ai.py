from flask import Blueprint, jsonify, make_response, request
from openai import OpenAI
import anthropic
import os

open_ai = Blueprint('open_ai', __name__, url_prefix='/api/v1/ai')


@open_ai.route("/askOpenAI", methods=['POST'])
def openAI():
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=OPENAI_KEY)

    data = request.json
    answer =  client.chat.completions.create(   
        model="gpt-4o",
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
    client = anthropic.Anthropic(
        api_key=CLAUDE_KEY
    )
    
    data = request.json
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": data['prompt']}
        ]
    )
    return message.content[0].text

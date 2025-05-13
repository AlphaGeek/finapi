from flask import Blueprint, jsonify, make_response
from openai import OpenAI
import os

open_ai = Blueprint('open_ai', __name__, url_prefix='/api/v1')

OPENAI_KEY = os.environ.get("OPENAI_KEY", None)
client = OpenAI(api_key=OPENAI_KEY)

@open_ai.route("question", methods=['GET'])
def index():
    answer = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "What is the capital of the United States?"}
        ],
    )

    # answer = client.Completion.create(
    #  model='curie',
    #  messages=[{"role": "user", "content": "Write a story about a lizard that escapes"}]
    # )

    # answer = openai.ChatCompletion.create(
    #  model="gpt-3.5-turbo",
    #  messages=[{"role": "user", "content": "Write a story about a lizard that escapes"}]
    # )
    print(answer)

    response = make_response(
        jsonify({"answer": answer.choices[0].text}),
        200,
    )
    #response = jsonify({"answer": "This will be released soon!"})
    response.headers["Content-Type"] = "application/json"
    return response

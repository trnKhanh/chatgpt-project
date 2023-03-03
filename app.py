from flask import Flask, request, redirect, url_for, render_template
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

history=[]

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/completion", methods=["POST"])
def completion():
    message = request.json["message"]
    # create response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=create_prompt(message),
        max_tokens=100,
        temperature=0.6,
    )
    return json.dumps(response.choices[0].text)

# create prompt function
def create_prompt(p):
    return f'You are the chatbot. User: Hello\nChatbot: Hello. How are you?\nUser: {p}\nChatbot:'
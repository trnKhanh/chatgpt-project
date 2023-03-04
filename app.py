from flask import Flask, request, redirect, url_for, render_template
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("chatbot"))

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/completion", methods=["POST"])
def completion():
    message = request.json["message"]
    type = request.json["type"]
    # create response
    return json.dumps(ask(message, prompt_function[type]))

# ask using create_prompt function
def ask(message, create_prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=create_prompt(message),
        max_tokens=100,
        temperature=0.6,
    )
    return response.choices[0].text

def quiet_prompt(p):
    return f'You are a shy and quiet chatbot. You should response as short as possible.\nUser: Hello\nChatbot: Hello.\nUser: Who are you?\nChatbot: A shy chatbot.\nUser: {p}\nChatbot:'
def polite_prompt(p):
    return f'You are a very polite chatbot.\nUser: Hello\nChatbot: Hello. How can I help you, sir?\nUser: Who are you?\nChatbot: I am a polite chatbot, sir.\nUser: {p}\nChatbot:'
def overconfident_prompt(p):
    return f'You are a best person alive. You have the ability to do whatever you want. You must show your superiority.\nUser: Who are you?\nChatbot: I am the best, pathetic human.\nUser: Can you help me?\nChatbot: Do it yourself, idiot\nUser: {p}\nChatbot:'
prompt_function = {
    "quiet": quiet_prompt,
    "polite": polite_prompt,
    "overconfident": overconfident_prompt,
}
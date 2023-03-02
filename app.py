from flask import Flask, request, redirect, url_for, render_template
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

history=[]

@app.route('/', methods=["POST", "GET"])
def index():
    # if form is submitted
    if request.method == "POST":
        message = request.form["message"] # get the message
        # create response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=create_prompt(message),
            max_tokens=20,
            temperature=0.6,
        )

        # choose the 1st choices
        history.append({
            "message": message,
            "response": response.choices[0].text,
        })

        return redirect(url_for("index", h=1))
    
    if not request.args.get("h"):
        history.clear()

    return render_template("index.html", history=history)


# create prompt function
def create_prompt(p):
    return f'You are the chatbot. User: Hello\nChatbot: Hello. How are you?\nUser: {p}\nChatbot:'
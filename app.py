from flask import Flask, request, redirect, url_for, render_template, session
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        message = request.form["message"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=create_prompt(message),
            max_tokens=20,
            temperature=0.6,
        )

        if "history" not in session:
            session["history"] = []

        session["history"].append({
            "message": message,
            "response": response.choices[0].text,
        })

        return redirect(url_for("index"))
    
    return render_template("index.html", history=session["history"])


# create prompt function
def create_prompt(p):
    return p
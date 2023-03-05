from flask import Flask, request, redirect, url_for, render_template
import openai
import os
import json
import requests
import pycountry

openai.api_key = os.getenv("OPENAI_API_KEY")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

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
    return json.dumps(response_function[type](message))

# ask using create_prompt function
def ask(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.6,
    )
    return response.choices[0].text

def normal_prompt(p):
    return f'You are a chatbot. You should response politely.\nUser: Hello\nChatbot: Hello, sir.\nUser: Who are you?\nChatbot: I am a chatbot\nUser: {p}\nChatbot:'
def extract_name_prompt(p):
    return f'Extract name from the sentence.\nSentence: I want to know the weather in India.\nName: India.\nSentence: What is the weather like in Vietnam.\nName: Vietnam.\nSentence: {p}\nName:'
def weather_prompt(main, min_temp, max_temp, humidity):
    return f'Write a  weather description based on given information.\n\nWeather: rain.\nTemperature: 15 to 20 (Celsius Degree).\nHumidity: 80.\nDescription: The weather is rainy with temperature ranging from 15 to 20 Celsius Degree. The humidity is around 80%. Remember to bring umbrella when going out.\n\nWeather: sunny.\nTemperature: 30 to 40 (Celsius Degree).\nHumidity: 50.\nDescription:  The weather is sunny with temperature ranging from 30 to 40 Celsius Degree. The humidity is around 50%, making it a very hot day day. Remember to use sun cream before going out.\n\nWeather: {main}.\nTemperature: {min_temp} to {max_temp}(Celsius Degree).\nHumidity: {humidity}.\nDescription: '

def normal_response(message):
    return ask(normal_prompt(message))
def weather_resonse(message):
    city_name = ask(extract_name_prompt(message)).strip(".").strip()

    coordinate = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={OPEN_WEATHER_API_KEY}').json()
    lat = coordinate[0]["lat"]
    lon = coordinate[0]["lon"]

    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}&units=metric').json()
    print(lat)
    print(lon)
    main = weather["weather"][0]["main"]
    min_temp = weather["main"]["temp_min"]
    max_temp = weather["main"]["temp_max"]
    humidity = weather["main"]["humidity"]
    return ask(weather_prompt(main, min_temp, max_temp, humidity))

response_function = {
    "normal": normal_response,
    "weather": weather_resonse
}
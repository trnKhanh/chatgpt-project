from flask import Flask, request, redirect, url_for, render_template
import openai
import os
import json
import requests
from pydub import AudioSegment
from langdetect import detect


max_tokens = 100
openai.api_key = os.getenv("OPENAI_API_KEY")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("chatbot"))

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html", botType="normal", messages=normal_chatbot_messages)

@app.route("/weather")
def weather():
    return render_template("chatbot.html", botType="weather")

@app.route("/classification")
def classification():
    return render_template("classification.html")

@app.route("/classify", methods=["POST"])
def classify():
    text = request.json["text"]
    return json.dumps(classify(text));

@app.route("/response", methods=["POST"])
def response():
    message = request.json["message"]
    type = request.json["type"]
    response = response_function[type](message)
    # create response
    return json.dumps({
        "message": response,
        "lang": detect(response),
    })

@app.route("/whisper", methods=["POST"])
def whisper():
    file = request.files["audio_file"]
    file.save("audio_file.webm")
    audio = AudioSegment.from_file("audio_file.webm", format="webm")
    audio.export("audio_file.mp3", format="mp3")

    with open("audio_file.mp3", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    os.remove("audio_file.webm")
    os.remove("audio_file.mp3")
    return json.dumps(transcript["text"])

# classification
def classify(text):
    response = openai.Completion.create(
        model="ada:ft-personal-2023-03-09-03-02-35",
        prompt=f'{text.strip()}.\n#\n',
        max_tokens=1,
        temperature=0.2,
    )
    return response.choices[0].text
    
# ask using completion model
def ask_completion(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.6,
    )
    return response.choices[0].text

# ask using chat model
def ask_chat(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.6,
    )
    return response["choices"][0]["message"]["content"]

# prompt used for completion model
def normal_prompt(p):
    return f"""You are a helpful assistant. You should response politely.
    ###
    User: {p}.
    Assistant: """

def extract_name_prompt(p):
    return f"""You will response with the location name from user message. Response with the name only. If the user does not ask about the weather, response with unidentify.
    ###
    Sentence: {p}.
    Name: """

def weather_description_prompt(main, min_temp, max_temp, humidity, lang):
    return f"""Write a weather description based on given information.
    ###
    Weather: rain. Temperature: 15 to 20 (Celsius Degree). Humidity: 80. Language: en.
    Description: The weather is rainy with temperature ranging from 15 to 20 Celsius Degree. The humidity is around 80%. Remember to bring umbrella when going out.
    Weather: {main}. Temperature: {min_temp} to {max_temp} (Celsius Degree). Humidity: {humidity}. Language: {lang}.
    Description: """

# messages used for chat model
normal_chatbot_messages = [
    {"role": "system", "content": "You are a helpful assistant. You should response politely."},
]
extract_name_messages = [
    {"role": "system", "content": "You will response with the location name from user message. Response with the name only. If the user does not ask about the weather, response with unidentify."},
    {"role": "user", "content":""},
]
# {"role": "user", "content": sentence}

weather_description_messages = [
    {"role": "system", "content": "Write a weather description based on given information."},
    {"role": "user", "content": "Weather: rain. Temperature: 15 to 20 (Celsius Degree). Humidity: 80. Language: en"},
    {"role": "assistant", "content": "The weather is rainy with temperature ranging from 15 to 20 Celsius Degree. The humidity is around 80%. Remember to bring umbrella when going out."},
    {"role": "user", "content":""},
]
# {"role": "user", "content": f'Weather: {main}. Temperature: {temp_min} to {temp_max} (Celsius Degree). Humidity: {humidity}. Language: {lang}'}

# response functions
# normal chatbot
def normal_chatbot_response(message):
    normal_chatbot_messages.append(
        {"role": "user", "content": message}
    )
    result = ask_chat(normal_chatbot_messages)
    normal_chatbot_messages.append(
        {"role": "assistant", "content": result}
    )
    return result

# weather bot
def extract_name(message):
    extract_name_messages[-1]["content"] = message
    name = ask_chat(extract_name_messages)
    return name

def get_weather_description(main, temp_min, temp_max, humidity, lang):
    weather_description_messages[-1]["content"] = f'Weather: {main}. Temperature: {temp_min} to {temp_max} (Celsius Degree). Humidity: {humidity}. Language: {lang}'
    weather_description = ask_chat(weather_description_messages)
    return weather_description

def weather_resonse(message):
    location_name = extract_name(message)
    try:
        coordinate = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=1&appid={OPEN_WEATHER_API_KEY}').json()
        lat = coordinate[0]["lat"]
        lon = coordinate[0]["lon"]

        weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}&units=metric').json()
        main = weather["weather"][0]["main"]
        temp_min = weather["main"]["temp_min"]
        temp_max = weather["main"]["temp_max"]
        humidity = weather["main"]["humidity"]
        lang = detect(message)
    except:
        return "I do not understand what you've said."

    return get_weather_description(main, temp_min, temp_max, humidity, lang)

# dictionary for response type
response_function = {
    "normal": normal_chatbot_response,
    "weather": weather_resonse
}
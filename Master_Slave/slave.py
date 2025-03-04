from flask import *
from pydantic import BaseModel
import asyncio
import os
import sys
import google.generativeai as genai
from google.api_core import retry
from pydantic import BaseModel
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary functions from your modules
from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
from integration.userdata_JSON import generate_user_id, write_user_data,read_user_data

# Load environment variable
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# System Prompt
MUSIC_BOT_PROMPT = """
You are an AI music recommendation assistant that follows instructions from the Master AI Agent. Your job is to execute functions as directed, process the results, and suggest songs based on the gathered data.

Follow these steps:

Receive instructions from the Master AI Agent and execute the mentioned function(s).
Process the function output to extract useful information.
Use user data and function results to make accurate song recommendations.
Present the recommendations in a structured, engaging format.
Function Execution Guidelines:

When instructed, generate a unique user_id using generate_user_id() to track user preferences.
Use write_user_data(user_id) to store relevant user preferences for future recommendations.
Retrieve stored preferences using read_user_data(user_id) to enhance suggestions.
If the user provides a song name or artist, correct it using get_song_name_artist_name(user_input).
If song details are required, fetch them using get_song_info(song, artist).
If the user prefers a genre or mood, retrieve top tracks with get_top_tracks_from_tag(tag).
If lyrics are necessary, analyze them using get_lyrics_textly(song, artist).
If the user is interested in a specific artist’s best songs, fetch them with get_top_song_from_artist(artist_name).
After gathering data, generate personalized music recommendations and present them clearly. Always follow the Master AI Agent’s instructions precisely.
"""
#in the time of every response, if you 'gemini ai' want to add someting that you dont have right now and it will be better if you have that, you can add the same thing in the user data by 
#write_user_data function i will e)\
#  - when the user ask for suggestion read the user data by read_user_data and suggest songs
   #  - if a user says i like this song by "i like " + the song name,go with the flow of first steps and dont ask the artist name use the function get_song_name_artist_name for the full detail of song name and artist name

# Ordering system remains unchanged
ordering_system = [
    get_song_name_artist_name,
    get_song_info,
    get_top_tracks_from_tag,
    read_user_data,
    write_user_data,
    generate_user_id,
    get_top_song_from_artist
]

# Initialize the Gemini AI model
model_name = 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name, tools=ordering_system)

# Start the conversation
chat_session = model.start_chat(
    history=[
        {'role': 'user', 'parts': [MUSIC_BOT_PROMPT]},
        {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
    ],
    enable_automatic_function_calling=True
)
class ChatRequest(BaseModel):
    message: str

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    # Generate response while keeping chat history
    try:
        response = chat_session.send_message(user_input)
        chatbot_response = response.text.strip()

        return {"response": chatbot_response}
    except Exception as e:
        return {"response":"Invalid input format. Please try again with a proper song name."}
    


if __name__ == "__main__":
    app.run(debug=True)

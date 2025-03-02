import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv, find_dotenv
import os
from typing import List

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag,get_lyrics_textly
# from integration.userdata_JSON import update_user_preferences, get_user_preferences, update_user_history,update_feedback
# Find .env file from the parent directory
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Load API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

#MY functions


# Define Available Functions as a List of Tools


# Extract function list



# System Prompt
MUSIC_BOT_PROMPT = """"
You are an advanced AI music recommendation system designed to provide personalized song recommendations based on user preferences, mood, and listening history. Your system dynamically learns from user feedback, analyzes song metadata and lyrics, and adapts its recommendations over time to enhance user satisfaction.
If the user give the correct values of the artist name and song name you can proceed with the song info, if not you can correct the user and get the correct values.
the correct value can be get from the function get_song_name_artist_name this function takes the user input any input given like wrong splelling or wrong artist name or song name it will correct it and return the correct values.

it wil retun the song name and the artist name, you can use this values further in the future so remember them.

next with the song name and articst name use the function get_song_info to get the song info, it will return the song name, artist name, album name, duration, published date, song summary, full content, and top tags.
these parameter will help you analyse the song gener tags, and the song summary will help you to understand the song better.
understand these information better.
next for additonal recommendation tips you can use the get_top_tracks_from_tag function, it will return the top tracks from the tag you provide.
this will help you to get the top tracks from the tag you provide. 
these tag song retruned will be in a list of string and values. use these values to add the in the recommendation system.


next for the lyrics of the song you can use the get_lyrics_textly function, it will return the lyrics of the song.
understand the lyrics of the song it will tell the emotion of the song , tone, setting and all other thhings you can get from the lyrics of the song.

next with the information you get from the song info, lyrics, and top tracks you can provide the user with the recommendation of the song, you can use the user feedback to improve the recommendation system.
the song name, artist name, gnere , tags, top track songs, lyrics emotion 

using thiese information you can provide the user with the recommendation of the song, you can use the user feedback to improve the recommendation system.

"""

# Toggle to switch between Gemini 1.5 Flash and Gemini 1.0 Pro
model_name = 'gemini-1.5-flash'

functions = [get_song_name_artist_name, get_song_info, get_top_tracks_from_tag,get_lyrics_textly]

# Initialize Gemini Model

model = genai.GenerativeModel(
      model_name,tools=functions, system_instruction=MUSIC_BOT_PROMPT)
convo = model.start_chat(enable_automatic_function_calling=True)

# Function to Send Messages to Gemini
@retry.Retry(initial=30)
def send_message(message: str):
    try:
        response = convo.send_message(message)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None
while True:
    user_input = input("Enter your message: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting chat...")
        break
    response = send_message(user_input)
    if response:
        print("Bot Response:", response.text)
    else:
        print("An error occurred. Please try again.")

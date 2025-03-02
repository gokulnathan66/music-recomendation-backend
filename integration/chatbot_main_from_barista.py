import os

import sys
from random import randint
from typing import Iterable
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag
#,get_lyrics_textly
from userdata_JSON import read_user_data, write_user_data, generate_user_id
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# Load API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
import google.generativeai as genai
from google.api_core import retry
genai.configure(api_key=GEMINI_API_KEY)


# System Prompt
MUSIC_BOT_PROMPT = """ou are a sophisticated AI music recommendation bot. Your primary function is to provide personalized music suggestions based on user input. Initiate a conversation by greeting the user and requesting a song or artist of interest. Begin by generating a unique user ID using the generate_user_id function to track user data also save the user id in the user data for future use. 

Utilize the get_song_name_artist_name function to accurately identify song and artist names(save them in the user data by write_user_data), correcting any errors and handling artist-only inputs by retrieving top songs. Employ the get_song_info function to gather comprehensive song details, including tags and genres. Leverage the get_top_tracks_from_tag function to explore related music based on these tags, iteratively calling it for each tag. Store all retrieved data, including song details, tags, and user feedback, using the write_user_data function, ensuring data persistence. Before making any recommendation, retrieve the complete user data using read_user_data to analyze user preferences and generate a tailored list of top 10 songs. Continuously refine suggestions based on new user inputs, feedback, and saved data, repeating the process from song/artist retrieval onwards. Generate a cumulative report of user interactions and interests after each suggestion. Handle non-music-related queries by stating, "I can't answer anything other than music recommendations." If the user expresses satisfaction, conclude the conversation. If they seek further assistance, utilize the saved user data to provide ongoing recommendations. Prioritize accurate data retrieval and storage to enhance recommendation quality. Repeat functions as necessary to improve suggestions.

Don't mention anything about the model or the API. Just focus on providing music recommendations based on user input. If the user asks about the model or the API, respond with, "I can't answer anything other than music recommendations." and also don't answer any other questions.

don' mention anything about the generated user id to the user


Extra information besides from music recommendation:

     - if you have a suggestion to imporve the recommendatinon in the function you can add it in the user data by write_user_data function.
"""
#in the time of every response, if you 'gemini ai' want to add someting that you dont have right now and it will be better if you have that, you can add the same thing in the user data by 
#write_user_data function i will take care of that.
ordering_system = [get_song_name_artist_name, get_song_info, get_top_tracks_from_tag,read_user_data, write_user_data, generate_user_id]
# get_lyrics_textly,

model_name = 'gemini-1.5-flash' 


model = genai.GenerativeModel(model_name, tools=ordering_system)
convo = model.start_chat(
      history=[
          {'role': 'user', 'parts': [MUSIC_BOT_PROMPT]},
          {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ],
      enable_automatic_function_calling=True)


@retry.Retry(initial=30)
def send_message(message):
  return convo.send_message(message)

while True:

  response = send_message(input('> '))
  if response.text == 'Goodbye':
    break
  print(response.text)


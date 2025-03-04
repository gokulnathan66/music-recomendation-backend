from flask import *
from pydantic import BaseModel
import asyncio
import os
import sys
import google.generativeai as genai
from google.api_core import retry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary functions from your modules
from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
from mongodb import ChatHistoryManager
# Load environment variable
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# System Prompt
SLAVE_BOT_PROMPT = """
You are an AI music recommendation assistant that follows instructions from the Master AI Agent. Your job is to execute functions as directed, process the results, and suggest songs based on the gathered data.

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
    get_top_song_from_artist
]

# Initialize the Gemini AI model
model_name = 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name, tools=ordering_system)

chat = ChatHistoryManager(collection_name="SLAVE-HISTORY")
@retry.Retry(initial=30)
def send_message_slave(user_id, message: str):                                                                                                                                                                                                                                                                                                                                   
    try:
        # Retrieve recent chat history
        recent_history = chat.get_recent_chat_history(user_id)

        # Start chat with existing history
        chat_session = model.start_chat(
        history=[
          {'role': 'user', 'parts': [SLAVE_BOT_PROMPT]},
          {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ]+ recent_history,
        enable_automatic_function_calling=True

        )
        
        # Get response
        response = chat_session.send_message(message)

        # Save messages to database
        chat.save_chat_history(user_id, "user", message)
        chat.save_chat_history(user_id, "model", response.text)

        return response.text

    except Exception as e:
        print(f"Error: {e}")
        return None
    
# while True:
#     response= send_message_slave(123,"get song detail for artic monkeys 505")
#     print(response)
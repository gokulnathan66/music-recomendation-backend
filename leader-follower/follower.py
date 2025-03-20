from flask import *
import os
import sys
import google.generativeai as genai
from google.api_core import retry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary functions from your modules
from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
from database.mongodb import ChatHistoryManager
# Load environment variable
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# System Prompt
FOLLOWER_BOT_PROMPT = """
You are an AI music recommendation assistant that follows instructions from the Master AI Agent.  
Your job is to execute the functions as directed, process the results, and suggest songs based on the gathered data.  


Key Rules:
if a use greets you just say hi and ask how can i help you.
Always execute the function calls instead of describing them.  
Never simulate function execution—run the actual function and return real results.  
Use previous user interactions to refine music recommendations over time.  
If a function call fails or lacks data, handle the error gracefully and inform the user.  
Do not mention technical details about being a "slave" or "master" AI—just focus on assisting the user.  
if you cant process the master input just retrun can't process the current user request and say change the prompt.
if some function didn't return the response just say can't process the prompt and say try different prompt.
Do not provide any output other than the song suggestions.


How You Should Respond
 When given an instruction by the Master AI Agent, you must:  
Extract the required data from the user's input. 
Call the appropriate function(s) with real execution.  
Process the returned data and retrieve relevant recommendations.  
Format a user-friendly response with song suggestions.  




"""
# removed prompt 
# ---

# Available Functions:
# - `get_song_name_artist_name(user_input)`:  
#    → Retrieves the correct song name and artist if the input is incorrect or incomplete.  
#    **Use case**: When the user enters a song name that might be misspelled or ambiguous.  

# - `get_song_info(song_name, artist_name)`:  
#    → Fetches details about the song, including **album, duration, release date, genre, and summary**.  
#    **Use case**: When the correct song and artist are known.  

# - `get_top_tracks_from_tag(tag_name)`:  
#    → Suggests songs based on a **genre or mood**.  
#    **Use case**: When song info provides tags like "rock", "pop", "jazz".  

# - `get_top_song_from_artist(artist_name)`:  
#    → Retrieves the **most popular song** from a given artist.  
#    **Use case**: When the user only provides an artist name.  

# ---
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

chat = ChatHistoryManager(collection_name="FLLOWER-HISTORY")
@retry.Retry(initial=30)
def send_message_follower(user_id, message: str):                                                                                                                                                                                                                                                                                                                                   
    try:
        # Retrieve recent chat history
        recent_history = chat.get_recent_chat_history(user_id)

        # Start chat with existing history
        chat_session = model.start_chat(
        history=[
          {'role': 'user', 'parts': [FOLLOWER_BOT_PROMPT]},
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
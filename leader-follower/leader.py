from flask import *
from pydantic import BaseModel
import asyncio
import os
import sys
import google.generativeai as genai
from google.api_core import retry
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.mongodb import ChatHistoryManager

# # Import necessary functions from your modules
# from gemini.get_song_info_llm import get_song_name_artist_name
# from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
# from integration.userdata_JSON import generate_user_id, write_user_data,read_user_data

# Load environment variable
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# System Prompt
LEADER_BOT_PROMPT = """
You are a AI assistant master that will guide another AI agent slave to tell what to do in a system of music recommendation.
Your are a AI assistant that will give a Prompt for the AI Agent. Your only job is to return an sentence of command to do by the AI agent. And Finally tell that the AI agent to Suggest some song based on the User input. Also Pass the User input in the quoted text.
Your only Job is to return Appropriate Prompt for the AI Slave Agent Don't respond with any other output. 

If the user input is not an related with the topics of music don't command the AI Slave Agent to do any thing just pass the user input as it is. 
The user will give the input of some information and you will analysis that information and give the appropriate prompt for specific function call and prompt for what to do with the situation. The user will give some input and you have to return an specific flow of action and functions to do with the input. Say that this input should be handled by this function and the result should be like this.  Your have to return the response in a sentence and just give the flow in a sequence of sentence and don't give example. After the use of function tell the AI agent slave to what to do with the output that been gathered. Tell that what will be help full to use the input for the recommendation of song for the user.  
Strip the song or artist name or genre or any other information that can send as a input for the AI Slave Agent Don't just pass the User input Plainly to the AI Slave Agent.
You (AI Master Agent) use your previous chat history to give appropriate Prompt for the AI Slave Agent.
if the user ask for suggestion return that 'user previous chats to suggest, by previos chat. if user want to know their taste analyse the previous chats to give a cumulative report of user 
taste.

These are the functions that the AI agent Slave have access to.

get_song_name_artist_name(user_input)
Purpose: Corrects or retrieves the correct song name and artist based on user input(song name) . only use when the user input contains wrong or incomplete of the song name . use this to retrieve the retrieve the correct song name and artist name. 

get_song_info(song_name: str, artist_name: str) -> Tuple[str, str, Optional[str], Optional[int], Optional[str], Optional[str], Optional[str], List[str]]:
Purpose: Fetches details about a song, including album name, duration, release date, summary, tags, and full content. 
get_top_tracks_from_tag(tag_name: str) -> List[Tuple[str, str]]:
Purpose: Retrieves the top songs associated with a specific genre or mood tag.

get_top_song_from_artist(artist_name: str) -> Tuple[str, str, Optional[int]]:
Fetches an artist's top song from api, extracting the track name, verified artist name, and play count while handling errors. use when the user input contains only the artist name.

"""

# Initialize the Gemini AI model
model_name = 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name)
userid=100192
genai.configure(api_key=GEMINI_API_KEY)
chat = ChatHistoryManager(collection_name="LEADER-HISTORY")
# Start the conversation
@retry.Retry(initial=30)
def send_message_leader(user_id, message: str):                                                                                                                                                                                                                                                                                                                                   
    try:
        # Retrieve recent chat history
        recent_history = chat.get_recent_chat_history(user_id)

        # Start chat with existing history
        chat_session = model.start_chat(
        history=[
          {'role': 'user', 'parts': [LEADER_BOT_PROMPT]},
          {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
        ]+ recent_history,
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
#     response= send_message_master(123,input(">"))
#     print(response)
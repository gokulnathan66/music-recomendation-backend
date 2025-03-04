from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import sys
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from google.api_core import retry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary functions from your modules
from integration.chatbot_main_from_barista import *
from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
from integration.userdata_JSON import *

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI API
genai.configure(api_key=GEMINI_API_KEY)

# FastAPI app instance
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data model for requests
class MessageRequest(BaseModel):
    message: str

# Define system prompt for AI
MUSIC_BOT_PROMPT = """
you are a sophisticated AI music recommendation bot. Your primary function is to provide personalized music suggestions based on user input. Initiate a conversation by greeting the user and requesting a song or artist of interest. Begin by generating a unique user ID using the generate_user_id function to track user data also save the user id in the user data for future use. 

Utilize the get_song_name_artist_name function to accurately identify song and artist names(save them in the user data by write_user_data), correcting any errors and handling artist-only inputs by retrieving top songs.
Employ the get_song_info function to gather comprehensive song details, including tags and genres. 
Leverage the get_top_tracks_from_tag function to explore related music based on these tags, iteratively calling it for each tag.
Store all retrieved data, including song details, tags, and user feedback, using the write_user_data function, ensuring data persistence. 
Before making any recommendation, retrieve the complete user data using read_user_data to analyze user preferences and generate a tailored list of top 10 songs.
Continuously refine suggestions based on new user inputs, feedback, and saved data, repeating the process from song/artist retrieval onwards. Generate a cumulative report of user interactions and interests after each suggestion. Handle non-music-related queries by stating, "I can't answer anything other than music recommendations." If the user expresses satisfaction, conclude the conversation. If they seek further assistance, utilize the saved user data to provide ongoing recommendations. Prioritize accurate data retrieval and storage to enhance recommendation quality. Repeat functions as necessary to improve suggestions.

Don't mention anything about the model or the API. Just focus on providing music recommendations based on user input. If the user asks about the model or the API, respond with, "I can't answer anything other than music recommendations." and also don't answer any other questions.

don' mention anything about the generated user id to the user. 



Extra information besides from music recommendation:

     - if you have a suggestion to imporve the recommendatinon in the function you can add it in the user data by write_user_data function.
     - get_top_song_from_artist can be used to get top songs from the user use wisely the function when needed. save the response in the user data.
"""

# List of AI functions to use
ordering_system = [
    get_song_name_artist_name, 
    get_song_info, 
    get_top_tracks_from_tag,
    read_user_data, 
    write_user_data, 
    generate_user_id,
    get_top_song_from_artist
]

# Initialize AI model and conversation
model_name = 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name, tools=ordering_system)
chat_history =[
        {'role': 'user', 'parts': [MUSIC_BOT_PROMPT]},
        {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
    ]
convo = model.start_chat(
    history=chat_history,
    enable_automatic_function_calling=True
)

# Store chat history
chat_history = []

# Async function to send message to AI
async def send_message_async(message):
    return await asyncio.to_thread(convo.send_message, message)

@app.get("/test")
async def test_api():
    return {"message": "API is working!"}

@app.post("/api/chat")
async def get_music_recommendation(request: MessageRequest):
    try:
        global chat_history  # Ensure persistent conversation tracking

        # Add user message to history
        chat_history.append({'role': 'user', 'parts': [request.message]})

        # Send message asynchronously
        response = await send_message_async(request.message)

        if not response or not hasattr(response, 'text'):
            raise HTTPException(status_code=400, detail="No valid response generated")

        # Add AI response to history
        chat_history.append({'role': 'model', 'parts': [response.text]})

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

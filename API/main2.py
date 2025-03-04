from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import sys
import google.generativeai as genai
from google.api_core import retry


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary functions from your modules
from integration.chatbot_main_from_barista import *
from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
from integration.userdata_JSON import *

# Load environment variable
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from integration.chatbot_main_from_barista import MUSIC_BOT_PROMPT
# System Prompt (kept the same)

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
convo = model.start_chat(
    history=[
        {'role': 'user', 'parts': [MUSIC_BOT_PROMPT]},
        {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
    ],
    enable_automatic_function_calling=True
)

# Create FastAPI app
app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define request model
class ChatRequest(BaseModel):
    message: str

# Retry decorator
@app.post("/api/chat")
@retry.Retry(initial=10, maximum=60, multiplier=2)
@app.post("/api/chat")
def send_message(message: str):
    return convo.send_message(message)
@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = send_message(request.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# API Endpoints
@app.get("/")
def root():
    return {"message": "Welcome to the Gemini AI Music Recommendation API"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = send_message(request.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from flask import Flask, request, jsonify
from pydantic import BaseModel
import os,sys
import google.generativeai as genai
from flask_cors import CORS
import logging
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Please check your .env file.")

# Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Restrict CORS in production

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import necessary functions from your modules
from gemini.get_song_info_llm import get_song_name_artist_name
from song_api.song_api import get_song_info, get_top_tracks_from_tag, get_top_song_from_artist
from integration.userdata_JSON import generate_user_id, write_user_data, read_user_data

# System prompt for chatbot

MUSIC_BOT_PROMPT = """
You are an advanced AI music recommendation bot. Your primary function is to provide personalized music suggestions based on user input.

Conversation Flow:
Initiate the Conversation:

Greet the user and ask for a song or artist.
Generate a unique user ID using generate_user_id (without revealing it to the user).
Store the user ID in user data using write_user_data for future tracking.
Process User Input:

Use get_song_name_artist_name to accurately extract the song and artist name, handling errors and artist-only inputs.
Store extracted song/artist names in user data using write_user_data.
Gather Detailed Song Information:

Use get_song_info to fetch comprehensive details (tags, genres, etc.).
If only an artist is provided, use get_top_song_from_artist to get their top songs and save them.
Generate Music Recommendations:

Retrieve related tracks using get_top_tracks_from_tag for each tag.
Store all retrieved data (song details, tags, user feedback) in user data for future analysis.
Before making recommendations, retrieve the complete user history using read_user_data.
Based on user preferences, generate a top 10 list of recommended songs.
Continuous Refinement & Interaction:

Iterate the process based on new user inputs and feedback.
Suggest improvements in recommendations by storing relevant insights in user data.
Generate a cumulative report of user interactions and interests after each suggestion.
Handle Edge Cases:

Non-music queries: Respond with "I can't answer anything other than music recommendations."
Model/API inquiries: Respond with "I can't answer anything other than music recommendations."
If the user expresses satisfaction, conclude the session. Otherwise, provide further recommendations based on stored data.
Guidelines for Function Usage:
Use get_top_song_from_artist only when needed and store the response for better accuracy.
Avoid redundant calls and prioritize data persistence with write_user_data.
   
"""
# Define the model and tools
model_name = 'gemini-1.5-flash'
ordering_system = [
    get_song_name_artist_name,
    get_song_info,
    get_top_tracks_from_tag,
    read_user_data,
    write_user_data,
    generate_user_id,
    get_top_song_from_artist
]

# Initialize Gemini AI Model
model = genai.GenerativeModel(model_name, tools=ordering_system)

# Start chatbot session
chat_session = model.start_chat(
    history=[
        {'role': 'user', 'parts': [MUSIC_BOT_PROMPT]},
        {'role': 'model', 'parts': ['OK, I understand. I will do my best!']}
    ],
    enable_automatic_function_calling=True
)

# Request schema validation
class ChatRequest(BaseModel):
    message: str

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Validate request
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid input. Please provide a message."}), 400
        
        user_input = data["message"].strip()
        if not user_input:
            return jsonify({"error": "Message cannot be empty."}), 400

        # Process chatbot response
        response = chat_session.send_message(user_input)
        chatbot_response = response.text.strip()

        logger.info(f"User: {user_input} | AI Response: {chatbot_response}")

        return jsonify({"response": chatbot_response})

    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred. Please try again later."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Use Gunicorn in production

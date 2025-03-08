#org_api.py
from flask import Flask, request, jsonify
from leader import send_message_leader
from follower import send_message_follower
from flask_cors import CORS
import os
import logging
from waitress import serve

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "Welcome to the home page"

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        session_id = data.get("session_id")
        user_message = data.get("message")

        if not session_id or not user_message:
            return jsonify({"error": "Missing session_id or message"}), 400
        
        leader_response = send_message_leader(session_id, user_message)
        follower_response = send_message_follower(session_id, leader_response)
        
        return jsonify({"response": follower_response})

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")  # Change default to 0.0.0.0
    PORT = int(os.environ.get("FLASK_PORT", 5000))
    serve(app, host=HOST, port=PORT)

#this is the organization api for the using of and organising of master and slave api
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory storage for chat sessions
chats = {}

@app.route('/create_chat', methods=['POST'])
def create_chat():
    """Generate a new chat ID."""
    chat_id = str(uuid.uuid4())  # Unique chat ID
    chats[chat_id] = []  # Initialize chat session
    return jsonify({"chat_id": chat_id})

@app.route('/send_message', methods=['POST'])
def send_message():
    """Store messages in a chat session."""
    data = request.json
    chat_id = data.get("chat_id")
    message = data.get("message")

    if not chat_id or chat_id not in chats:
        return jsonify({"error": "Invalid chat ID"}), 400

    chats[chat_id].append({"user": message})
    return jsonify({"message": "Message sent successfully"})

@app.route('/get_chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Retrieve chat history by chat ID."""
    if chat_id not in chats:
        return jsonify({"error": "Chat ID not found"}), 404
    
    return jsonify({"chat_id": chat_id, "messages": chats[chat_id]})

if __name__ == '__main__':
    app.run(debug=True)

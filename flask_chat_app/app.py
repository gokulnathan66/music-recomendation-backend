from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

# In-memory storage (Replace with a database in production)
chats = {}

@app.route('/')
def home():
    """Home page showing previous chats."""
    return render_template('index.html', chat_ids=list(chats.keys()))

@app.route('/create_chat', methods=['POST'])
def create_chat():
    """Generate a new chat session and redirect to it."""
    chat_id = str(uuid.uuid4())  # Shorten ID for readability
    chats[chat_id] = []  # Store chat history
    return redirect(url_for('chat_page', chat_id=chat_id))

@app.route('/chat/<chat_id>')
def chat_page(chat_id):
    """Render the chat interface with a sidebar showing past chats."""
    if chat_id not in chats:
        return "Chat ID not found!", 404
    return render_template('chat.html', chat_id=chat_id, chat_ids=list(chats.keys()))

@socketio.on('join')
def handle_join(data):
    """A user joins a chat room (WebSocket room)."""
    chat_id = data['chat_id']
    join_room(chat_id)
    emit('load_messages', chats[chat_id], room=request.sid)

@socketio.on('send_message')
def handle_message(data):
    """Store user messages and broadcast them to the chat room."""
    chat_id = data.get("chat_id")
    message = data.get("message")

    if not chat_id or chat_id not in chats:
        return

    chats[chat_id].append({"user": message})
    emit('receive_message', {"user": message}, room=chat_id)  # Broadcast to chat room

if __name__ == '__main__':
    socketio.run(app, debug=True)

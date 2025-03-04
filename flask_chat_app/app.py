from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid

app = Flask(__name__)

# In-memory chat storage
chats = {}

@app.route('/')
def home():
    """Home page to start a new chat."""
    return render_template('index.html')

@app.route('/create_chat', methods=['POST'])
def create_chat():
    """Generate a new chat session and redirect to it."""
    chat_id = str(uuid.uuid4())
    chats[chat_id] = []  # Initialize chat session
    return redirect(url_for('chat_page', chat_id=chat_id))

@app.route('/chat/<chat_id>')
def chat_page(chat_id):
    """Render the chat interface for a specific chat ID."""
    if chat_id not in chats:
        return "Chat ID not found!", 404
    return render_template('chat.html', chat_id=chat_id)

@app.route('/send_message', methods=['POST'])
def send_message():
    """Receive and store user messages."""
    data = request.json
    chat_id = data.get("chat_id")
    message = data.get("message")

    if not chat_id or chat_id not in chats:
        return jsonify({"error": "Invalid chat ID"}), 400

    chats[chat_id].append({"user": message})
    return jsonify({"status": "Message received"})

@app.route('/get_chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Return chat history."""
    if chat_id not in chats:
        return jsonify({"error": "Chat ID not found"}), 404
    return jsonify({"chat_id": chat_id, "messages": chats[chat_id]})

if __name__ == '__main__':
    app.run(debug=True)

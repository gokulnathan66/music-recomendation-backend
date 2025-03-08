# this api manages the communication between the user and model
from flask import Flask, request, jsonify
from leader import send_message_master
from follower import send_message_slave
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


@app.route("/")
def home():
    test = "Welcome to the home page"
    return test
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # Get JSON input

    session_id = data.get("session_id")
    user_message = data.get("message")

    response = send_message_master(session_id,user_message)
    slave_response=send_message_slave(session_id,user_message)
    return jsonify({"response": slave_response})


if __name__ == '__main__':
    app.run(debug=True)

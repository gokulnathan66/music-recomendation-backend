from flask import Flask, request, jsonify
from master import send_message_master
from slave import send_message_slave

app = Flask(__name__)
userid="12hi87oL"

@app.route("/")
def home():
    test = "Welcome to the home page"
    return test
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # Get JSON input
    message = data.get('message', 'i like sun flower')  # Default to 'Guest' if no name is provided
    
    response = send_message_master(userid,message)
    slave_response=send_message_slave(userid,response)
    return jsonify({
        "User message": message,
        "slave response": slave_response,
        "master_replay":response,
    })

if __name__ == '__main__':
    app.run(debug=True)

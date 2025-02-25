import json
import os
from datetime import datetime

USER_DATA_FILE = "user_data.json"

def load_user_data():
    """Loads user data from the JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}  # Return empty dictionary if file doesn't exist

def save_user_data(data):
    """Saves user data to the JSON file."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
        
def update_user_preferences(user_id, liked_song=None, disliked_song=None, preferred_genre=None, feedback=None):
    """
    Updates user preferences:
    - Adds liked/disliked songs
    - Updates preferred genres
    - Stores feedback
    """
    data = load_user_data()

    if user_id not in data:
        data[user_id] = {
            "liked_songs": [],
            "disliked_songs": [],
            "preferred_genres": [],
            "history": [],
            "feedback": {"positive": [], "negative": []}
        }

    if liked_song:
        data[user_id]["liked_songs"].append(liked_song)

    if disliked_song:
        data[user_id]["disliked_songs"].append(disliked_song)

    if preferred_genre and preferred_genre not in data[user_id]["preferred_genres"]:
        data[user_id]["preferred_genres"].append(preferred_genre)

    if feedback:
        feedback_type = "positive" if feedback["type"] == "positive" else "negative"
        data[user_id]["feedback"][feedback_type].append(feedback["message"])

    save_user_data(data)

def get_user_preferences(user_id):
    """Retrieves stored user preferences."""
    data = load_user_data()
    return data.get(user_id, {"message": "User not found"})

def update_user_history(user_id, song_name, artist):
    """
    Logs song listening history for the user.
    """
    data = load_user_data()

    if user_id not in data:
        data[user_id] = {
            "liked_songs": [],
            "disliked_songs": [],
            "preferred_genres": [],
            "history": [],
            "feedback": {"positive": [], "negative": []}
        }

    song_entry = {
        "song_name": song_name,
        "artist": artist,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data[user_id]["history"].append(song_entry)
    save_user_data(data)
def update_feedback(user_id, song_name, artist, feedback_type):
    """
    Updates feedback on a song.
    - feedback_type: "like" or "dislike"
    """
    data = load_user_data()

    if user_id not in data:
        data[user_id] = {
            "liked_songs": [],
            "disliked_songs": [],
            "preferred_genres": [],
            "history": [],
            "feedback": {"positive": [], "negative": []}
        }

    song_entry = {"song_name": song_name, "artist": artist}

    if feedback_type == "like":
        data[user_id]["liked_songs"].append(song_entry)
    elif feedback_type == "dislike":
        data[user_id]["disliked_songs"].append(song_entry)

    save_user_data(data)

#testing the function 
# Example user ID
# user_id = "123456"

# # Add liked song
# update_user_preferences(user_id, liked_song={"song_name": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop"})

# # Add disliked song
# update_user_preferences(user_id, disliked_song={"song_name": "Song XYZ", "artist": "Artist ABC", "genre": "Rock"})

# # Add preferred genre
# update_user_preferences(user_id, preferred_genre="Hip-Hop")

# # Update user history
# update_user_history(user_id, song_name="Shape of You", artist="Ed Sheeran")

# # Update feedback
# update_feedback(user_id, song_name="Old Town Road", artist="Lil Nas X", feedback_type="dislike")

# # Retrieve and print user preferences
# user_data = get_user_preferences(user_id)
# print(json.dumps(user_data, indent=4))



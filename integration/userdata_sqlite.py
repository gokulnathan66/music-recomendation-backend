import sqlite3
from datetime import datetime

DB_FILE = "user_data.db"

def create_tables():
    """Creates necessary tables if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liked_songs (
                user_id TEXT,
                song_name TEXT,
                artist TEXT,
                genre TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disliked_songs (
                user_id TEXT,
                song_name TEXT,
                artist TEXT,
                genre TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferred_genres (
                user_id TEXT,
                genre TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                user_id TEXT,
                song_name TEXT,
                artist TEXT,
                date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                user_id TEXT,
                type TEXT CHECK(type IN ('positive', 'negative')),
                message TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        conn.commit()

def update_user_preferences(user_id, liked_song=None, disliked_song=None, preferred_genre=None, feedback=None):
    """Updates user preferences including liked/disliked songs, preferred genres, and feedback."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

        if liked_song:
            cursor.execute("INSERT INTO liked_songs (user_id, song_name, artist, genre) VALUES (?, ?, ?, ?)",
                           (user_id, liked_song["song_name"], liked_song["artist"], liked_song["genre"]))
        
        if disliked_song:
            cursor.execute("INSERT INTO disliked_songs (user_id, song_name, artist, genre) VALUES (?, ?, ?, ?)",
                           (user_id, disliked_song["song_name"], disliked_song["artist"], disliked_song["genre"]))
        
        if preferred_genre:
            cursor.execute("INSERT OR IGNORE INTO preferred_genres (user_id, genre) VALUES (?, ?)", (user_id, preferred_genre))
        
        if feedback:
            cursor.execute("INSERT INTO feedback (user_id, type, message) VALUES (?, ?, ?)",
                           (user_id, feedback["type"], feedback["message"]))
        
        conn.commit()

def get_user_preferences(user_id):
    """Retrieves stored user preferences."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT song_name, artist, genre FROM liked_songs WHERE user_id = ?", (user_id,))
        liked_songs = cursor.fetchall()
        
        cursor.execute("SELECT song_name, artist, genre FROM disliked_songs WHERE user_id = ?", (user_id,))
        disliked_songs = cursor.fetchall()
        
        cursor.execute("SELECT genre FROM preferred_genres WHERE user_id = ?", (user_id,))
        preferred_genres = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT song_name, artist, date FROM history WHERE user_id = ?", (user_id,))
        history = cursor.fetchall()
        
        cursor.execute("SELECT type, message FROM feedback WHERE user_id = ?", (user_id,))
        feedback = cursor.fetchall()
        
        return {
            "liked_songs": liked_songs,
            "disliked_songs": disliked_songs,
            "preferred_genres": preferred_genres,
            "history": history,
            "feedback": feedback
        }

def update_user_history(user_id, song_name, artist):
    """Logs song listening history for the user."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (user_id, song_name, artist, date) VALUES (?, ?, ?, ?)",
                       (user_id, song_name, artist, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

def update_feedback(user_id, song_name, artist, feedback_type):
    """Updates feedback on a song."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        table = "liked_songs" if feedback_type == "like" else "disliked_songs"
        cursor.execute(f"INSERT INTO {table} (user_id, song_name, artist, genre) VALUES (?, ?, ?, '')",
                       (user_id, song_name, artist))
        
        conn.commit()

# Initialize database
create_tables()
# Test script for SQLite-based user preferences

user_id = "test_user"

# Test adding liked song
update_user_preferences(user_id, liked_song={"song_name": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop"})
print("Liked song added.")

# Test adding disliked song
update_user_preferences(user_id, disliked_song={"song_name": "Song XYZ", "artist": "Artist ABC", "genre": "Rock"})
print("Disliked song added.")

# Test adding preferred genre
update_user_preferences(user_id, preferred_genre="Hip-Hop")
print("Preferred genre added.")

# Test updating user history
update_user_history(user_id, song_name="Shape of You", artist="Ed Sheeran")
print("User history updated.")

# Test updating feedback
update_feedback(user_id, song_name="Old Town Road", artist="Lil Nas X", feedback_type="dislike")
print("Feedback updated.")

# Retrieve and print user preferences
user_data = get_user_preferences(user_id)
print("Retrieved user preferences:")
print(user_data)

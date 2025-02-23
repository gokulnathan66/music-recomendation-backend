import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gemini import gemini_communication, get_song_info_llm
from song_api.song_api import *

# User input
user_input = "hi i like to listen to i waanbe beyours by aricmonkeys"

# Extract song details
song_name, artist_name = get_song_info_llm.get_song_name_artist_name(user_input)
track_name, artist_name, album_name, duration, published_date, summary, content, top_tags = get_song_info(song_name, artist_name)

all_song_with_respective_tags = []

# Ensure top_tags is a valid list
if top_tags:
    for tag in top_tags:
        result = get_top_tracks_from_tag(tag)
        for track in result:
            artist = track[1]  # Assuming track[1] is the artist name
            song = track[0]    # Assuming track[0] is the song name
            all_song_with_respective_tags.append({"artist": artist, "song": song, "tag": tag})

# Structured prompt for song recommendations
predefine_prompt = f"""
Here's a structured prompt that guides the model to suggest songs based on user inputs:  

---

**Guiding Prompt for Song Recommendation Model:**  

Analyze the user's song preferences based on the following inputs:  

1. **User's Provided Song Details:**  
   - **Song Name:**   
   - **Artist Name:**  
   - **Album Name:**  
   - **Duration:** 
   - **Published Date:**   
   - **Summary:** 
   - **Content Description:** 

2. **Tag-Based Categorization:**  
   - The song is tagged under 
   - Retrieve **top songs for each tag** and compare their relevance to the provided song.  

3. **Recommendation Criteria for Similar Songs:**  
   - Suggest **10 songs** that align with the user's taste, considering:  
     - **Similar lyrics/emotion** (e.g., heartbreak, joy, empowerment).  
     - **Musical elements** (e.g., tempo, key, instrumentation).  
     - **Genre and artist similarity** (e.g., indie, rock, pop, classical).  
     - **Mood-based relevance** (e.g., study-friendly, workout, late-night listening).  

4. **Output Format:**  
   - Provide the **top 10 recommended songs**, including:  
     - **Song Name**  
     - **Artist Name**  
     - **Album Name**  
     - **Why it was recommended (emotion, theme, genre, musical similarity, etc.)**  

### **Objective:**  
When the user asks for song recommendations, use this structured approach to **suggest songs that best match their preferences**, creating a personalized music discovery experience.
"""

# Constructing user prompt as a dictionary for structured input
userprompt = {
    "song_name": song_name,
    "artist_name": artist_name,
    "album_name": album_name,
    "duration": duration,
    "published_date": published_date,
    "summary": summary,
    "content": content,
    "top_tags": top_tags,
    "top_songs_from_each_tag": all_song_with_respective_tags
}

# Ensure the response function handles dictionary input
response = gemini_communication.gemani_response(predefine_prompt, str(userprompt))

print(response)

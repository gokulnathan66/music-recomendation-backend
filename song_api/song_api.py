

import requests
import json
from dotenv import load_dotenv, find_dotenv
import os
from typing import Tuple, List, Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Find .env file from the parent directory
dotenv_path = find_dotenv()

# Load environment variables from .env
load_dotenv(dotenv_path)

# Example: Accessing an environment variable
MUSIC_API_KEY = os.getenv("MUSCI_API_KEY")

api_key=MUSIC_API_KEY

# Define the base URL
url = "https://ws.audioscrobbler.com/2.0/"


def get_song_info(song_name: str, artist_name: str) -> Tuple[str, str, Optional[str], Optional[int], Optional[str], Optional[str], Optional[str], List[str]]:
    """
    Fetches detailed information about a song using the Last.fm API.

    This function sends a GET request to the Last.fm API with the given song name and artist name. 
    It retrieves and extracts details such as the track name, artist name, album name, duration, 
    published date, song summary, full content, and top tags.

    Args:
        song_name (str): The name of the song to search for.
        artist_name (str): The name of the artist who performed the song.

    Returns:
        Tuple[str, str, Optional[str], Optional[int], Optional[str], Optional[str], Optional[str], List[str]]:
            - track_name (str): The name of the track.
            - artist_name (str): The name of the artist.
            - album_name (Optional[str]): The album title (if available).
            - duration (Optional[int]): Duration of the song in milliseconds (if available).
            - published_date (Optional[str]): The published date of the song (if available).
            - summary (Optional[str]): A short summary of the song (if available).
            - content (Optional[str]): Detailed content or description of the song (if available).
            - top_tags (List[str]): A list of top tags associated with the song.

    Example:
        >>> get_song_info("Shape of You", "Ed Sheeran")
        ('Shape of You', 'Ed Sheeran', 'Divide', 233712, '12 Jan 2017, 15:00', 'Shape of You is a song...',
         'Full content of Shape of You...', ['pop', 'dance', 'acoustic'])

    Notes:
        - If the API request fails, an error message is printed, and `None` is returned for missing fields.
        - The function assumes `api_key` and `url` are predefined and accessible.
        - `requests` library is used for API calls, ensure it is installed.
    """

    # Define parameters
    params = {
        "method": "track.getinfo",
        "track": song_name,
        "artist": artist_name,
        "api_key": api_key,  # Ensure api_key is defined
        "format": "json"
    }

    # Send GET request with parameters
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return song_name, artist_name, None, None, None, None, None, []

    data = response.json()  # Parse JSON response

    try:
        track_name = data['track']['name']
        artist_name = data['track']['artist']['name']
        album_name = data['track'].get('album', {}).get('title')
        duration = int(data['track'].get('duration', 0)) if data['track'].get('duration') else None
        published_date = data['track'].get('wiki', {}).get('published')
        summary = data['track'].get('wiki', {}).get('summary')
        content = data['track'].get('wiki', {}).get('content')
        top_tags = [tag['name'] for tag in data['track'].get('toptags', {}).get('tag', [])]

    except KeyError as e:
        print(f"Missing key in response: {e}")
        return song_name, artist_name, None, None, None, None, None, []

    print("get song info called")
    return track_name, artist_name, album_name, duration, published_date, summary, content, top_tags
#testing the function
# get_song_info("Shape of You", "Ed Sheeran")



def get_top_tracks_from_tag(tag_name: str) -> List[Tuple[str, str]]:
    """
    Fetches the top tracks associated with a given music tag using the Last.fm API.

    This function sends a GET request to the Last.fm API with a specified tag name 
    (e.g., "rock", "pop", "jazz") and retrieves the top tracks for that tag. 
    It extracts and returns a list of tuples containing the song title and artist name.

    Args:
        tag_name (str): The genre or category tag to search for (e.g., "rock", "pop", "jazz").

    Returns:
        List[Tuple[str, str]]: A list of tuples where each tuple contains:
            - track_name (str): The name of the track.
            - artist_name (str): The name of the artist.

    Example:
        >>> get_top_tracks_from_tag("pop")
        [('Blinding Lights', 'The Weeknd'), ('Watermelon Sugar', 'Harry Styles'), ...]

    Notes:
        - If the API request fails, an empty list is returned.
        - Ensure `api_key` and `url` are correctly set up before calling this function.
        - The function assumes that the "track" list exists in the response.
    """

    # Define parameters
    params = {
        "method": "tag.gettoptracks",
        "tag": tag_name,
        "api_key": api_key,  # Ensure api_key is defined
        "format": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return []

    json_response = response.json()  # Parse JSON response

    # Extract track names and artist names safely
    tracks = json_response.get("tracks", {}).get("track", [])
    
    # Ensure tracks is a list before processing
    if not isinstance(tracks, list):
        return []

    result = [(track.get("name", "Unknown Track"), track.get("artist", {}).get("name", "Unknown Artist")) for track in tracks]
    print("get top tracks from tag called")
    return result
#testing get top tag trackes

#this api function takes too much time to retrive
def get_lyrics(song_name, artist_name):
    # Define parameters
    url_lyrics = f"https://api.lyrics.ovh/v1/{artist_name}/{song_name}"


    # Send GET request with parameters
    response = requests.get(url_lyrics)

    # Check if request was successful
    if response.status_code == 200:
        json_response = response.json()  # Parse JSON response
        print(json_response)
        # print(json_response['track']['toptags'])
    else:
        print(f"Request failed with status code: {response.status_code}")

#testing the function
# get_lyrics("Shape of You", "Ed Sheeran")
import requests
from typing import Optional

def get_lyrics_textly(song_name: str) -> Optional[str]:
    """
    Fetches song lyrics from the Textyl API based on the provided song name.

    This function sends a GET request to the Textyl API with the given song title 
    and retrieves the lyrics if available. If the request is successful and lyrics 
    are found, the function returns the lyrics as a string. Otherwise, it prints 
    an error message and returns None.

    Args:
        song_name (str): The title of the song for which lyrics are requested.

    Returns:
        Optional[str]: The lyrics of the song as a string if found, otherwise None.

    Example:
        >>> lyrics = get_lyrics_textly("Shape of You")
        >>> print(lyrics)
        "The club isn't the best place to find a lover..."

    Notes:
        - The API request is made with `verify=False` to bypass SSL verification.
        - If the API response structure changes, additional error handling may be required.
        - Ensure that the API is reachable and functioning before calling this function.
    """

    url = "https://api.textyl.co/api/lyrics"
    params = {"q": song_name}
    print("get lyrics textly called")

    try:
        response = requests.get(url, params=params, verify=False)
        if response.status_code == 200:
            json_response = response.json()  # Parse JSON response
            
            # Debugging: Print full response (remove in production)
            # print(json_response)
            
            # Extract lyrics if available
            return json_response
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return None

#testing the Function 


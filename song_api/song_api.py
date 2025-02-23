

import requests
import json
from dotenv import load_dotenv, find_dotenv
import os

# Find .env file from the parent directory
dotenv_path = find_dotenv()

# Load environment variables from .env
load_dotenv(dotenv_path)

# Example: Accessing an environment variable
MUSIC_API_KEY = os.getenv("MUSIC_API_KEY")

api_key=MUSIC_API_KEY

# Define the base URL
url = "https://ws.audioscrobbler.com/2.0/"

def get_song_info(song_name, artist_name):
    # Define parameters
    params = {
        "method": "track.getinfo",
        "track": song_name,
        "artist": artist_name,
        "api_key": api_key,
        "format": "json"
    }

    # Send GET request with parameters
    response = requests.get(url, params=params)
    

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()    # Parse JSON response
        # print(json_response['track']['toptags'])
    else:
        print(f"Request failed with status code: {response.status_code}")
    # Extract the required fields

    track_name = data['track']['name']
    artist_name = data['track']['artist']['name']
    album_name = data['track']['album']['title']
    duration = data['track']['duration']
    published_date = data['track']['wiki']['published']
    summary = data['track']['wiki']['summary']
    content = data['track']['wiki']['content']
    top_tags = [tag['name'] for tag in data['track']['toptags']['tag']]  # Extract tag names

    # # Print extracted details
    # print("Track Name:", track_name)
    # print("Artist Name:", artist_name)
    # print("Album Name:", album_name)
    # print("Duration:", duration, "milliseconds")
    # print("Published Date:", published_date)
    # print("Summary:", summary)
    # print("Content:", content)
    # print("Top Tags:", ", ".join(top_tags))

    return track_name, artist_name, album_name, duration, published_date, summary, content, top_tags
#testing the function
# get_song_info("Shape of You", "Ed Sheeran")



def get_top_tracks_from_tag(tag_name):    
    # Define parameters
    params = {
        "method": "tag.gettoptracks",
        "tag": tag_name,
        "api_key": api_key,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        json_response = response.json()  # Parse JSON response
        
        # Extract track names and artist names
        tracks = json_response.get("tracks", {}).get("track", [])
        result = [(track["name"], track["artist"]["name"]) for track in tracks]
        
        return result
    else:
        print(f"Request failed with status code: {response.status_code}")
        return []

#testing get top tag trackes
# print(get_top_tracks_from_tag("pop"))


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

def get_lyrics_textly(song_name):
    url = "https://api.textyl.co/api/lyrics"
    params = {
        "q": song_name
    }
    response = requests.get(url, params=params,verify=False)
    if response.status_code == 200:
        json_response = response.json()  # Parse JSON response
        print(json_response)
        # print(json_response['track']['toptags'])
    else:
        print(f"Request failed with status code: {response.status_code}")
#testing the Function 

# get_lyrics_textly("Shape of You")


#get_song_info_llm.py
# Now import song_api
from .gemini_communication import gemani_response
from typing import Tuple, Optional

def get_song_name_artist_name(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts the correct song title and artist name from user input using the Gemini API.

    This function sends a predefined prompt along with the user input to the Gemini API, 
    ensuring it returns only the corrected song title and artist name in a structured format.

    Args:
        user_input (str): The user's input containing the song name and/or artist.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing:
            - song_name (Optional[str]): The corrected song title.
            - artist_name (Optional[str]): The corrected artist name.
            If parsing fails, returns (None, None).

    Example:
        >>> get_song_name_artist_name("Shpe of U by Ed Sheran")
        ('Shape of You', 'Ed Sheeran')
    """
    
    predefined_prompt = (
        "You are an AI model that extracts the correct song title and artist name from user input. "
        "Your response should only contain the corrected song title and artist name in the format: "
        "'<Song Name> by <Artist Name>'. Do not provide any additional text or explanations. "
        "If the user input contains errors in the song title or artist name, correct them."
    )

    response_gem = gemani_response(predefined_prompt, user_input)
    
    if "by" in response_gem:
        response_parts = response_gem.rsplit("by", 1)  # Splitting from the last occurrence of "by"
        song_name = response_parts[0].strip()
        artist_name = response_parts[1].strip()
        return song_name, artist_name
    else:
        print("Error: Unexpected response format from Gemini API:", response_gem)
        return None, None  # Return None if parsing fails


#testing the function
#get song infoo test
# response=song_api.get_song_info(song_name,artist_name)
# print(response)

#get song lyrics test
# get_lyrics=song_api.get_lyrics(song_name,artist_name)
# print(get_lyrics)
#discarded cause gemini can't access copyrighted lyrics
# def get_song_lyrics_gemini(song_name):
#     predefinded_prompt=""""you are a model to return the lyrics of the song, don't answer with a song that is inappropriate or offensive, don't answer any other questions,
#     just respond with the lyrics of the song, don't respond any other questions, not even that i a llm model i cant anser that question.
#     the resaon for this artist name and the songe, some time i will give the the song name or the artist name wrong, so you showld correct me and return the song name and
#     the artist name of the song. """
#     # userinput="Tell me the lyrics of the song Shape of You by Ed Sheeran"
#     response_gem= gemani_response(predefinded_prompt,song_name)
#     # sample response from the model "Shape of You by Ed Sheeran"
#     return(response_gem)
#     #get song lyrics test


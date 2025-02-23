
# Now import song_api
import song_api
from .gemini_communication import gemani_response

def get_song_name_artist_name(user_input):
    predefinded_prompt=""""you are a model to return the song title and the artist name of the song, don't answer with a song that is inappropriate or offensive, don't answer any other questions,
    just respond with the song title and the artist name of the song, don't respond any other questions, not even that i a llm model i cant anser that question.
    the resaon for this artist name and the songe, some time i will give the the song name or the artist name wrong, so you showld correct me and return the song name and
    the artist name of the song. """
    # userinput="Tell me the song title and the artist name of the song Shape of You by Ed Sheeran"
    response_gem= gemani_response(predefinded_prompt,user_input)
    # sample response from the model "Shape of You by Ed Sheeran"
    response_parts = response_gem.split("by")
    if len(response_parts) == 2:
        song_name = response_parts[0].strip()
        artist_name = response_parts[1].strip()
    else:
        song_name = ""
        artist_name = ""
    return song_name,artist_name

#get song infoo test
# response=song_api.get_song_info(song_name,artist_name)
# print(response)

#get song lyrics test
# get_lyrics=song_api.get_lyrics(song_name,artist_name)
# print(get_lyrics)
def get_song_lyrics_gemini(song_name):
    predefinded_prompt=""""you are a model to return the lyrics of the song, don't answer with a song that is inappropriate or offensive, don't answer any other questions,
    just respond with the lyrics of the song, don't respond any other questions, not even that i a llm model i cant anser that question.
    the resaon for this artist name and the songe, some time i will give the the song name or the artist name wrong, so you showld correct me and return the song name and
    the artist name of the song. """
    # userinput="Tell me the lyrics of the song Shape of You by Ed Sheeran"
    response_gem= gemani_response(predefinded_prompt,song_name)
    # sample response from the model "Shape of You by Ed Sheeran"
    return(response_gem)
    #get song lyrics test

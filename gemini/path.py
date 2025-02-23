import sys
from pathlib import Path

# Add the directory containing song_api.py to sys.path
sys.path.append(str(Path.cwd().parent / "song_api"))

# Now import song_api
import song_api  # Assuming song_api.py has functions or classes

# Example usage (if song_api.py has a function named `get_song_info`)
song_api.get_song_info(song_name="Shape of You", artist_name="Ed Sheeran")

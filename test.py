import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.current_user_saved_tracks()
print(results['items'][0]['track']['name'])
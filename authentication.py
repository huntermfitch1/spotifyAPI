import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def authenticate_spotify():
    credentials = yaml.safe_load(open("credentials.yml"))
    auth_manager = SpotifyClientCredentials(credentials['client'], credentials["secret"])
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

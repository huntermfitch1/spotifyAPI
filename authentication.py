import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def authenticate_spotify():
    credentials = yaml.safe_load(open("credentials.yml"))
    auth_manager = SpotifyClientCredentials(credentials['client'], credentials["secret"])
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# dataset: https://components.one/datasets/pitchfork-reviews-dataset

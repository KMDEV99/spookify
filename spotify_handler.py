import os
import requests
from io import BytesIO
from PIL import Image
from spotipy.oauth2 import SpotifyOAuth
import spotipy

class SpotifyHandler:
    def __init__(self, client_id, client_secret, redirect_uri, cache_dir):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-read-currently-playing",
            cache_path=".cache"
        ))
        self.cache_dir = cache_dir

    def get_current_track(self):
        """Fetches currently playing track info from Spotify."""
        try:
            return self.sp.currently_playing()
        except:
            return None

    def get_album_art(self, track_id, url):
        """Downloads and caches album art, resized for RPi performance."""
        path = os.path.join(self.cache_dir, f"{track_id}.png")
        if not os.path.exists(path):
            res = requests.get(url)
            img = Image.open(BytesIO(res.content)).convert("RGBA")
            img = img.resize((320, 320), Image.NEAREST)
            img.save(path)
        return Image.open(path)

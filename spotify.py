from auth import ClientAuth
import requests

# TODO: test in and out of Google App Engine
class Spotify:
    def __init__(self, key=None, secret=None):
        import os
        self.key = key if key is not None else os.getenv('SPOTIFY_CLIENT_ID')
        self.secret = secret if secret is not None else os.getenv('SPOTIFY_CLIENT_SECRET')
        self.root_url = "https://api.spotify.com/v1"
        self.session = None
    
    def _get(self, *args, **kwargs):
        if self.session is None:
            self.session = requests.Session()
            self.session.auth = ClientAuth(self.key, self.secret)
        return self.session.get(*args, **kwargs)
    
    def _get_rel(self, rel_url, *args, **kwargs):
        url = self.root_url + rel_url
        return self._get(url, *args, **kwargs)
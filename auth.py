# import requests_toolbelt.adapters.appengine
import requests
import datetime
# requests_toolbelt.adapters.appengine.monkeypatch()

class ClientAuth(requests.auth.AuthBase):
    
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.token = None
        self.token_type = None
        self.expires_at = None
        self.retry_count = 0
        self.retry_max = 3
    
    def renew_if_needed(self):
        """Check if the access token has expired"""
        if self.token is None:
            self.renew()
        if self.expires_at and datetime.datetime.utcnow() >= self.expires_at:
            self.renew()
    
    def renew(self):
        """Get a new access token"""
        response = requests.post(self.token_url, auth=(self.key, self.secret), data={'grant_type':'client_credentials'})
        if response is not None:
            body = response.json()
            self.token = body['access_token']
            self.token_type = body['token_type']
            self.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=body['expires_in'])
    
    def build_headers(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
    
    def retry_request(self, r, **kwargs):
        """Reuse the request to make a new one"""
        """Code essentially copied from handle_401 method shown here https://github.com/requests/requests/blob/master/requests/auth.py"""
        r.content
        r.close()
        prep = r.request.copy()
        self.build_headers(prep)
        _r = r.connection.send(prep, **kwargs)
        _r.history.append(r)
        _r.request = prep
        
        return _r
    
    def handle_response(self, r, **kwargs):
        """Handle unauthorized requests by trying to get a new access token"""
        if not 400 <= r.status_code < 500:
            self.retry_count = 0
            return r
        
        if r.status_code == 401 and self.retry_count < self.retry_max:
            self.renew()
            self.retry_count += 1
            return self.retry_request(r)
        
        # Too many additional attempts on 401 or another 4XX error. Just return the response.
        self.retry_count = 0
        return r
    
    def __call__(self, r):
        
        self.renew_if_needed()
        
        self.build_headers(r)
        r.register_hook('response', self.handle_response)
        return r
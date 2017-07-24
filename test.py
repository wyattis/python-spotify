import unittest
from spotify import Spotify

class SpotifyAuthTests(unittest.TestCase):
    def setUp(self):
        self.spotify = Spotify()
    def test_authfails(self):
        res = self.spotify._get_rel('/tracks/2TpxZ7JUBn3uw46aR7qd6V')
        self.assertTrue(res is not None, "Something went wrong with intial request for authfails")
        self.spotify.session.auth.token = "asdfasdxfasf"
        res = self.spotify._get_rel('/tracks/2TpxZ7JUBn3uw46aR7qd6V')
        self.assertTrue('error' not in res.json(), "The ClientAuth didn't renew")

class SpotifyRequestTest(unittest.TestCase):
    def setUp(self):
        self.spotify = Spotify()
    def test_rawgettrack(self):
        res = self.spotify._get_rel('/tracks/2TpxZ7JUBn3uw46aR7qd6V')
        self.assertTrue(res is not None, "Authentication didn't work for some reason")



if __name__ == '__main__':
    unittest.main()
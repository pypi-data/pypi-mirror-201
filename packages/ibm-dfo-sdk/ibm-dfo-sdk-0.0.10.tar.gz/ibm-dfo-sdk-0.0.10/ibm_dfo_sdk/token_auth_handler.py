
from pyarrow import flight

""" Helper class to handle authentication tokens for flight
"""
class TokenClientAuthHandler(flight.ClientAuthHandler):
    def __init__(self, tok: str):
        # Call off to the base ClientAuthHandler
        super().__init__()

        # Set up the Bearer token
        self.token = bytes('Bearer ' + tok, 'utf-8')

    def authenticate(self, outs, ins):
        outs.write(self.token)
        self.token = ins.read()

    def get_token(self):
        return self.token

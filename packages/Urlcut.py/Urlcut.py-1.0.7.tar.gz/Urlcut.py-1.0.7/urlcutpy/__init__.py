import requests
import json

class UrlcutError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[Urlcut.py] {self.message}'

Token = ""

def Authenticate(_Authorization_Token):
    global Token 
    if _Authorization_Token:
        token_length = len(_Authorization_Token)
        if token_length < 27:
            raise UrlcutError("API key is too short to be valid.")
        else:
            Token = _Authorization_Token
    else:
        raise UrlcutError("No API key provided.")
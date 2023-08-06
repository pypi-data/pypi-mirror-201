import requests
import json

class UrlcutError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[Urlcut.py] {self.message}'

Token = ""

def Authenticate(_Authorization_Token:str):
    global Token 
    if _Authorization_Token:
        token_length = len(_Authorization_Token)
        if token_length < 27:
            raise UrlcutError("API key is too short to be valid.")
        else:
            Token = _Authorization_Token
    else:
        raise UrlcutError("No API key provided.")

def Create(_Link:str):
    global Token
    if Token:
        token_length = len(Token)
        if token_length < 27:
            raise UrlcutError("Test")
        else:
            API_URL = "https://v3.urlcut.app/developer/api/create"
            API_Headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {Token}'
            }
            API_Data = {
                "refLink": _Link
            }

            API_Response = requests.post(API_URL, headers=API_Headers, data=json.dumps(API_Data))
            API_Final = API_Response.json()
            return API_Final
    else:
        raise UrlcutError("No Api key provided.")


def Delete(_Identifier:str):
    global Token
    if Token:
        token_length = len(Token)
        if token_length < 27:
            raise UrlcutError("Test")
        else:
            API_URL = "https://v3.urlcut.app/developer/api/delete"
            API_Headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {Token}'
            }
            API_Data = {
                "shortened": _Identifier
            }

            API_Response = requests.delete(API_URL, headers=API_Headers, data=json.dumps(API_Data))
            API_Final = API_Response.json()
            return API_Final
    else:
        raise UrlcutError("No Api key provided.")
from app.credentials import *
from app.errors import *
import requests
import os

DIRNAME = '\\'.join(os.path.dirname(__file__).split("/"))

def pathing(dir, file):
    return os.path.join(f"{DIRNAME}/{dir}", file)


def validate(TOKEN, boolean=False):
    headers = {'Authorization': f"Bearer {TOKEN}",
           'Client-Id': CLIENT_ID
           }

    validation = requests.get(
        'https://id.twitch.tv/oauth2/validate', headers=headers)
    if validation.status_code == 200:
        if boolean:
            return True
        return validation.json()
    else:
        if boolean:
            return False
        raise ValidationError('Invalid or expired token')
        
def revoke(TOKEN):
    data = {'token': f"{TOKEN}",
               'client_id': CLIENT_ID}
    revokation = requests.post('https://id.twitch.tv/oauth2/revoke', data=data).status_code
    return revokation

def refresh(refresh_token):
    data = {'client_id': CLIENT_ID,
               'client_secret': CLIENT_SECRET,
               'grant_type': 'refresh_token',
               'refresh_token': f'{refresh_token}'
               }
    refreshment = requests.post('https://id.twitch.tv/oauth2/token', data=data).json()
    return refreshment

if __name__ == '__main__':
    token = refresh('r6lw421dm5m9t7f154gwttdd01lkzzxhlukxmzy9xnvmnwbnsm')['access_token']
    print(validate(token))

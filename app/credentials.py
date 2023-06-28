from dotenv import load_dotenv, find_dotenv
import os
# Load environment variables
load_dotenv(find_dotenv())

APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

# Twitch Env Variables
TWITCH_AUTHORIZATION_URL = os.getenv('TWITCH_AUTHORIZATION_URL')
TWITCH_TOKEN_URL = os.getenv('TWITCH_TOKEN_URL')
LOGIN_SCOPES = os.getenv('LOGIN_SCOPES')

_endpoints = ['users', ]
TWITCH_API_BASE_URL = os.getenv('TWITCH_API_BASE_URL')
TWITCH_API = {endpoint: f'{TWITCH_API_BASE_URL}/{endpoint}' for endpoint in _endpoints}

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Streamlabs Env Variables
STREAMLABS_SOCKET_BASE_URL = os.getenv('STREAMLABS_SOCKET_BASE_URL')
STREAMLABS_AUTHORIZATION_URL = os.getenv('STREAMLABS_AUTHORIZATION_URL')
STREAMLABS_TOKEN_URL = os.getenv('STREAMLABS_TOKEN_URL')
STREAMLABS_SOKET_TOKEN_URL = os.getenv('STREAMLABS_SOKET_TOKEN_URL')

STREAMLABS_CLIENT_ID = os.getenv('STREAMLABS_CLIENT_ID')
STREAMLABS_CLIENT_SECRET = os.getenv('STREAMLABS_CLIENT_SECRET')
STREAMLABS_REDIRECT_URI = os.getenv('STREAMLABS_REDIRECT_URI')

# MongoDB Env Variables
# MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
MONGODB_URL = os.getenv('MONGODB_URL')
DB_NAME = os.getenv('DB_NAME')
TWITCH_TOKENS_COLLECTION = os.getenv('TWITCH_TOKENS_COLLECTION')
STREAMLABS_SOCKET_TOKENS_COLLECTION = os.getenv('STREAMLABS_SOCKET_TOKENS_COLLECTION')
SUBATHON_COLLECTION = os.getenv('SUBATHON_COLLECTION')

DEFAULT_DEADLINE = int(os.getenv('DEFAULT_DEADLINE'))

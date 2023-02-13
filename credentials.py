from dotenv import load_dotenv, find_dotenv
import os
# Load environment variables
load_dotenv(find_dotenv())

MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

STREAMLABS_CLIENT_ID = os.getenv('STREAMLABS_CLIENT_ID')
STREAMLABS_CLIENT_SECRET = os.getenv('STREAMLABS_CLIENT_SECRET')
STREAMLABS_REDIRECT_URI = os.getenv('STREAMLABS_REDIRECT_URI')
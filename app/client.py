from pymongo import MongoClient
from app import MONGODB_URL

# Connect to the MongoDB server
db_client = MongoClient(MONGODB_URL)

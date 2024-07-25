from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("apiKey")
AUTH_DOMAIN = os.getenv("authDomain")
PROJECT_ID = os.getenv("projectId")
STORAGE_BUCKET = os.getenv("storageBucket")
MESSAGING_SENDER_ID = os.getenv("messagingSenderId")
APP_ID = os.getenv("appId")
DATABASE_URL = os.getenv("databaseURL")

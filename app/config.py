from dotenv import load_dotenv
import os

import json 
load_dotenv()

API_KEY = os.getenv("API_KEY")
AUTH_DOMAIN = os.getenv("AUTH_DOMAIN")
PROJECT_ID = os.getenv("PROJECT_ID")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET")
MESSAGING_SENDER_ID = os.getenv("MESSAGING_SENDER_ID")
APP_ID = os.getenv("APP_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
ALLOWED_ORIGINS = json.loads(os.getenv("ALLOWED_ORIGINS"))
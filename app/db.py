from functools import lru_cache

from app import config

import pyrebase

# Todo: Create .env file and read later!
firebase_config = {
  "apiKey": config.API_KEY,
  "authDomain": config.AUTH_DOMAIN,
  "projectId": config.PROJECT_ID,
  "storageBucket": config.STORAGE_BUCKET,
  "messagingSenderId": config.MESSAGING_SENDER_ID,
  "appId": config.APP_ID,
  "databaseURL": config.DATABASE_URL,
};


firebase = pyrebase.initialize_app(firebase_config)  
auth = firebase.auth()

db = firebase.database()
auth = firebase.auth()

def get_all_object(object_name):
    objects = db.child(object_name).get()
    data = []
    for obj in objects.each():
        data.append(obj.val())
    
    return data
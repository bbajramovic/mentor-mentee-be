# Read data from mentee.json and call api

import json

import requests

from app.models import Mentor, Mentee

def read_mentee_data():
    with open('mentee.json') as f:
        data = json.load(f)
    return data

def call_api():
    data = read_mentee_data()
    for mentee in data:
        response = requests.post('http://127.0.0.1:8000/mentees/add', json=mentee)
        
        print(response.json())
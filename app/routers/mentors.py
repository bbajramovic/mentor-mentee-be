from fastapi import APIRouter
from app.models import Mentor
from app.db import db

router = APIRouter()

@router.get("/{id}", tags=["mentors"])
async def get_mentor_info(id: int):
    # TODO: Get data from firebase
    return {"mentor": ""}


@router.get("/list/", tags=["mentors"])
async def get_mentors():
    # TODO: Get data from firebase
    mentors = db.child("mentors").get()
    print(mentors)
    # return []
    # print(mentees.val())
    data = []
    
    for mentor in mentors.each():
        data.append(mentor.val())
    
    return {"mentors": data}

@router.post("/add", tags=["mentors"])
async def add_mentor(mentor: Mentor):
    data = mentor
    # Convert data to dictionary
    data = data.dict()
    print(data)
    db.child("mentors").push(data)
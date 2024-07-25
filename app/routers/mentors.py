from fastapi import APIRouter
from app.models import Mentor
from app.db import db

router = APIRouter()

@router.get("/{id}", tags=["mentors"])
async def get_mentor_info(id: int):
    # TODO: Get data from firebase
    return {"mentor": ""}


@router.get("/list", tags=["mentors"])
async def get_mentors():
    # TODO: Get data from firebase
    return {
        "list": [
            {
                # mentor abc from database!
            }
        ]
    }

@router.post("/add", tags=["mentors"])
async def add_mentor(mentor: Mentor):
    data = mentor
    # Convert data to dictionary
    data = data.dict()
    print(data)
    db.child("mentors").push(data)
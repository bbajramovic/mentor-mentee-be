from fastapi import APIRouter
from app.models import Mentee
from app.db import db

router = APIRouter()

@router.get("/{id}", tags=["mentees"])
async def get_mentee_info(id: int):
    # TODO: Get data from firebase
    return {"mentee": ""}


@router.get("/list", tags=["mentees"])
async def get_mentees():
    # TODO: Get data from firebase
    # mentees = db.child("mentees").get()
    # print(mentees)
    return {
        "list": [
            {
                # mentee abc from database!
            }
        ]
    }
    # print(mentees.val())
    # data = []
    # 
    # for mentee in mentees.each():
        # data.append(mentee.val())
    
    # return {"mentees": data}

@router.post("/add", tags=["mentees"])
async def add_mentee(mentee: Mentee):
    data = mentee
    # Convert data to dictionary
    data = data.dict()
    print(data)
    db.child("mentees").push(data)
    
    # Set code success
    
    # return {"code": 200, "message": "Success add mentee!"}
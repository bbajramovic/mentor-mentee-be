from fastapi import APIRouter
from app.models import Mentee
from app.db import db, get_all_object
from pydantic import BaseModel

router = APIRouter()

@router.get("/{id}", tags=["mentees"])
async def get_mentee_info(id: str):
    # Get data from firebase
    data = db.child("mentees").order_by_child("id").equal_to(id).get()
    return data.val()


@router.get("/get", tags=["mentees"])
async def read_items() :
    data = get_all_object("mentees")
    return {"mentees": data}


@router.post("/add", tags=["mentees"])
async def add_mentee(mentee: Mentee):
    data = mentee
    # Convert data to dictionary
    data = data.dict()
    print(data)
    db.child("mentees").push(data)
    
    # Set code success
    
    # return {"code": 200, "message": "Success add mentee!"}
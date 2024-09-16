from fastapi import APIRouter
from app.models import Mentor
from app.db import db
from app.db import get_all_object

router = APIRouter()

@router.get("/{id}", tags=["mentors"])
async def get_mentor_info(id: str):
    # Get data from firebase
    data = db.child("mentors").order_by_child("id").equal_to(id).get()
    return data.val()

# Get all mentors
@router.get("/", tags=["mentors"])
async def get_mentors():
    data = get_all_object("mentors")
    return {"data":2}



@router.post("/add", tags=["mentors"])
async def add_mentor(mentor: Mentor):
    data = mentor
    # Convert data to dictionary
    data = data.dict()
    db.child("mentors").push(data)
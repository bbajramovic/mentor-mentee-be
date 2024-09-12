from fastapi import APIRouter
from app.db import get_all_object, db
from app.utils.matching import generateGroup
from pydantic import BaseModel

router = APIRouter()

class NewMatchBody(BaseModel):
    matchName: str
    
@router.delete("/delete/{uid}", tags=["match"])
async def delete_match(uid: str):
    # Query the match by uid
    # Delete the match
    db.child("matches").order_by_child("uid").equal_to(uid).remove()
    return {"message": "Match deleted!"}
    
@router.get("/list", tags=["match"])
async def get_all_matches():
    matches = get_all_object("matches")
    return matches

@router.post("/new", tags=["match"])
async def create_new_match(request:NewMatchBody):
    # TODO: 
    matchName = request.matchName
    # Get all mentors, all mentees
    # Iteratate through each
    
    mentees = get_all_object("mentees")
    mentors = get_all_object("mentors")
    
    # Get match name from request
    # matchName = request.json().get("matchName")
    
    # TODO: 
    # Filter all mentees who have been matched
    # Filter all mentor who have been matche with maximum mentee they need
  
    result = generateGroup(mentees, mentors, matchName)
    
    db.child("matches").push(result)    
    # Call function
    return result

    

# TODO:
# Delete, Update, Create, Get all, Get one, Get by id, Get by uuid
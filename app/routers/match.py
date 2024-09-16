from fastapi import APIRouter
from app.db import get_all_object, db
from app.utils.matching import generateGroup
from pydantic import BaseModel
import pandas as pd

router = APIRouter()

class NewMatchBody(BaseModel):
    matchName: str
    
class UpdateMatchNameBody(BaseModel):
    newName: str
    uid: str
    
@router.get("/get/{uid}", tags=["match"])
async def get_match(uid: str):
    # Query the match by uid
    match = db.child("matches").order_by_child("uid").equal_to(uid).get()
    val = match.val()
    if not val:
        return {}
    key = list(val.keys())[0]
    return val[key]


@router.put("/update/match_name", tags=["match"])
async def update_match_name(request: UpdateMatchNameBody):
    # Query the match by uid
    uid = request.uid
    newName = request.newName
    # db.child("matches").order_by_child("uid").equal_to(uid).update({"matchName": newName})
    matches = db.child("matches").get()
    for match in matches.each():
        if match.val().get("uid") == uid:
            key = match.key()
            db.child("matches").child(key).update({"matchName": newName})
            return {"message": "Match name updated!", "status": "success"}
    return {"message": "Match not found!", "status": "error"}
@router.delete("/delete/{uid}", tags=["match"])
async def delete_match(uid: str):
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
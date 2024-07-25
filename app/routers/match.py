from fastapi import APIRouter
from app.utils.matching import calculateMatching
router = APIRouter()

class mockDB():
    def get_all_mentors():
        return []
    def get_all_mentees():
        return []
    
db = mockDB()

# Get match by mentor




@router.get("/list", tags=["match"])
async def get_all_match():
    # TODO: 
    # Get all mentors, all mentees
    # Iteratate through each
    
    mentees = db.get_all_mentees()
    mentors = db.get_all_mentors()
    
    # TODO: 
    # Filter all mentees who have been matched
    # Filter all mentor who have been matche with maximum mentee they need
  
    result = calculateMatching(mentees, mentors)
     
    # Call function
    return {"matching_result": result}


@router.post("/confirm", tags=["match"])
async def confirm_match():
    # TODO: Update database for both mentor & mentee
    return {
        "list": [
            {
                # mentor abc from database!
            }
        ]
    }

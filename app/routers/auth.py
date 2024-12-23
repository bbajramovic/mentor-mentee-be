from fastapi import APIRouter
from app.models import Login
from app.db import db
from app.db import get_all_object
from app.db import auth
from fastapi import HTTPException

router = APIRouter()


@router.post("/login", tags=["auth"])
async def login(login: Login):
    try:
        # Print the login object
        print("Login: ", login)
        user = auth.sign_in_with_email_and_password(login.email, login.password)
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@router.post("/logout", tags=["auth"])
async def logout():
    auth.current_user = None
    return {"message": "Logged out successfully!"}
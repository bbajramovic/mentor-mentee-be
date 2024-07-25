from fastapi import Depends, FastAPI

from .routers import mentors, mentees, match

from app.db import db

app = FastAPI()


app.include_router(mentees.router, prefix='/mentees')
app.include_router(mentors.router, prefix='/mentors')
app.include_router(match.router, prefix='/match')


@app.get("/")
async def root():
    return {"message": "Hello Big Buddy!"}

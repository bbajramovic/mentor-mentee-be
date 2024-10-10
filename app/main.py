from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import mentees, mentors, match
from app.config import ALLOWED_ORIGINS


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(mentees.router, prefix='/mentees')
app.include_router(mentors.router, prefix='/mentors')
app.include_router(match.router, prefix='/match')

@app.get("/")
async def root():
    return {"message": "Hello Big Buddy!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
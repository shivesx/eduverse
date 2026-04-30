from fastapi import FastAPI
from app.db.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router
from app.routers import user_router
from app.routers import college_router
from app.routers import subject_router
from app.routers import assignment_router



Base.metadata.create_all(bind=engine)

app=FastAPI(title="Eduverse",version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message":"BACKEND START"}


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(college_router.router)
app.include_router(subject_router.router)
app.include_router(assignment_router.router)
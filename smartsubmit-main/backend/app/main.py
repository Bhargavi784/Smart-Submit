from fastapi import FastAPI
from app.core.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, submissions, assignments,classrooms
from app.models import Base, User, Assignment, Submission
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="smart Submit API")

Base.metadata.create_all(bind=engine)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(submissions.router)
app.include_router(assignments.router)
app.include_router(classrooms.router)

@app.get("/api")
def home():
    return {"message": "Smart Submit Backend is live!"}




app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

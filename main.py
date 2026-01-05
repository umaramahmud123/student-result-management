from fastapi import FastAPI
from database import Base, engine
from routers import students, courses, results
from routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Result Management API")

app.include_router(auth_router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(results.router)

@app.get("/")
def root():
    return {"message": "API is running"}

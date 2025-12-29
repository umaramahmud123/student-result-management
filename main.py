from fastapi import FastAPI
from database import Base, engine
from routers import students, courses, results

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Routers
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(results.router)

#@app.get("/")
#def root():
 #   return {"message": "Student Result Management API Running"}

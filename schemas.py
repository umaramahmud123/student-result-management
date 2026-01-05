from pydantic import BaseModel, Field



class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=72)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- STUDENT ----------

class StudentBase(BaseModel):
    name: str
    department: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    model_config = {
        "from_attributes": True
    }


# ---------- COURSE ----------

class CourseBase(BaseModel):
    course_name: str
    credit_unit: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    model_config = {
        "from_attributes": True
    }


# ---------- RESULT ----------

class ResultBase(BaseModel):
    student_id: int
    course_id: int
    score: float

class ResultCreate(ResultBase):
    pass

class ResultUpdate(BaseModel):
    score: float   # usually we only update the score

class Result(ResultBase):
    id: int
    model_config = {
        "from_attributes": True
    }


class StudentSummary(BaseModel):
    student_id: int
    name: str
    department: str
    total_score: float
    average_score: float
    grade: str


class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/", response_model=list[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@router.get("/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    return student


@router.put("/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, updated: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    for key, value in updated.dict().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    db.delete(student)
    db.commit()
    return {"detail": "Student deleted successfully"}


def calculate_grade(average: float) -> str:
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 45:
        return "D"
    else:
        return "F"


@router.get("/{student_id}/summary", response_model=schemas.StudentSummary)
def student_summary(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")

    results = db.query(models.Result).filter(models.Result.student_id == student_id).all()
    if not results:
        raise HTTPException(404, "No results for this student")

    total = sum(r.score for r in results)
    avg = total / len(results)
    grade = calculate_grade(avg)

    return schemas.StudentSummary(
        student_id=student.id,
        name=student.name,
        department=student.department,
        total_score=total,
        average_score=avg,
        grade=grade
    )

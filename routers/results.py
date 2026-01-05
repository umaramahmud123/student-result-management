from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_current_user
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/results",
    tags=["Results"]
)

@router.post("/", response_model=schemas.Result)
def create_result(
    result: schemas.ResultCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # ✅ protected
):
    new_result = models.Result(**result.dict())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

@router.get("/", response_model=list[schemas.Result])
def get_results(db: Session = Depends(get_db)):
    return db.query(models.Result).all()

@router.get("/{result_id}", response_model=schemas.Result)
def get_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not result:
        raise HTTPException(404, "Result not found")
    return result

@router.put("/{result_id}", response_model=schemas.Result)
def update_result(
    result_id: int,
    updated: schemas.ResultUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # ✅ protected
):
    result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not result:
        raise HTTPException(404, "Result not found")

    result.score = updated.score
    db.commit()
    db.refresh(result)
    return result

@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # ✅ protected
):
    result = db.query(models.Result).filter(models.Result.id == result_id).first()
    if not result:
        raise HTTPException(404, "Result not found")

    db.delete(result)
    db.commit()
    return {"detail": "Result deleted"}

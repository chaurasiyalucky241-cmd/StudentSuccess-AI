from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
import models.student as models
import schemas.student as schemas

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("/", response_model=List[schemas.StudentResponse])
def list_students(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=2000), db: Session = Depends(get_db)):
    return db.query(models.Student).offset(skip).limit(limit).all()

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(
        (models.Student.student_id == student.student_id) | 
        (models.Student.email == student.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student ID or Email already exists")
    
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

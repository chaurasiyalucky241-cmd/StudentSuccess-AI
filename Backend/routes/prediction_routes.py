from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
import models.student as models
import schemas.student as schemas
from services.ml_service import analyze_and_predict

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])

@router.get("/{student_id}", response_model=schemas.PredictionResponse)
def get_student_prediction(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student record not found")
    
    pred_gpa, risk, factors, recs = analyze_and_predict(
        attendance=student.attendance,
        internal_marks=student.internal_marks,
        assignment_score=student.assignment_score,
        lab_performance=student.lab_performance,
        previous_gpa=student.previous_gpa,
        backlogs=student.backlogs,
        study_hours=student.study_hours,
        participation=student.participation_score
    )

    return schemas.PredictionResponse(
        student_id=student.student_id,
        name=student.name,
        predicted_gpa=pred_gpa,
        risk_level=risk,
        main_factors=factors,
        recommendations=recs
    )

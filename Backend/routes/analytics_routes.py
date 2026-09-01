from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
import models.student as models
import schemas.student as schemas
from services.ml_service import analyze_and_predict, predict_many, risk_for

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard", response_model=schemas.DashboardMetrics)
def get_dashboard_summary(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    count = len(students)
    
    if count == 0:
        return schemas.DashboardMetrics(
            total_students=0,
            average_gpa=0.0,
            at_risk_students=0,
            at_risk_percentage=0.0,
            average_attendance=0.0,
            performance_trend={"Previous GPA": 0.0, "Attendance": 0.0, "Internal Marks": 0.0},
            risk_distribution={"Low Risk": 0, "Medium Risk": 0, "High Risk": 0},
            subject_performance={"Attendance": 0.0, "Internal Marks": 0.0, "Assignments": 0.0, "Lab Performance": 0.0, "Participation": 0.0}
        )

    avg_gpa = round(sum(s.previous_gpa for s in students) / count, 2)
    avg_att = round(sum(s.attendance for s in students) / count, 1)
    
    distribution = {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}
    batch_predictions = predict_many(students)
    for index, s in enumerate(students):
        prediction = batch_predictions[index]
        if prediction is None:
            prediction, _, _, _ = analyze_and_predict(
                s.attendance, s.internal_marks, s.assignment_score,
                s.lab_performance, s.previous_gpa, s.backlogs,
                s.study_hours, s.participation_score
            )
        risk = risk_for(prediction, s.attendance, s.backlogs)
        distribution[risk] += 1

    at_risk_count = distribution["Medium Risk"] + distribution["High Risk"]
    at_risk_pct = round((at_risk_count / count) * 100, 1)
    average_metrics = {
        "Attendance": round(sum(s.attendance for s in students) / count, 1),
        "Internal Marks": round(sum(s.internal_marks for s in students) / count, 1),
        "Assignments": round(sum(s.assignment_score for s in students) / count, 1),
        "Lab Performance": round(sum(s.lab_performance for s in students) / count, 1),
        "Participation": round(sum(s.participation_score for s in students) / count, 1),
    }

    return schemas.DashboardMetrics(
        total_students=count,
        average_gpa=avg_gpa,
        at_risk_students=at_risk_count,
        at_risk_percentage=at_risk_pct,
        average_attendance=avg_att,
        performance_trend={"Previous GPA": avg_gpa, "Attendance": avg_att, "Internal Marks": average_metrics["Internal Marks"]},
        risk_distribution=distribution,
        subject_performance=average_metrics
    )

import numpy as np
import os
from pathlib import Path
import joblib
import pandas as pd
from typing import Tuple, List

MODEL_PATH = Path(__file__).resolve().parents[1] / "student_cgpa_model.pkl"
_model = None
_model_load_attempted = False


def load_model():
    global _model, _model_load_attempted
    if _model_load_attempted:
        return _model
    _model_load_attempted = True
    if os.getenv("USE_ML_MODEL", "false").lower() != "true":
        return None
    if MODEL_PATH.exists():
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception:
            _model = None
    return _model


def predict_many(students):
    model = load_model()
    if model is None:
        return [None] * len(students)
    features = pd.DataFrame([
        {
            "Attendance": student.attendance,
            "Internal Marks": student.internal_marks,
            "Assignment Score": student.assignment_score,
            "Lab Performance": student.lab_performance,
            "Previous CGPA": student.previous_gpa,
            "Study Hours": student.study_hours,
            "Participation": student.participation_score,
            "Backlogs": student.backlogs,
        }
        for student in students
    ])
    return np.clip(model.predict(features), 0.0, 10.0).round(2).tolist()

def risk_for(predicted_gpa: float, attendance: float, backlogs: int) -> str:
    if predicted_gpa < 6.0 or backlogs >= 2 or attendance < 65.0:
        return "High Risk"
    if predicted_gpa < 7.5 or backlogs == 1 or attendance < 75.0:
        return "Medium Risk"
    return "Low Risk"

def analyze_and_predict(
    attendance: float,
    internal_marks: float,
    assignment_score: float,
    lab_performance: float,
    previous_gpa: float,
    backlogs: int,
    study_hours: float,
    participation: float
) -> Tuple[float, str, List[str], List[str]]:
    model = load_model()
    if model is not None:
        features = pd.DataFrame({
            "Attendance": [attendance],
            "Internal Marks": [internal_marks],
            "Assignment Score": [assignment_score],
            "Lab Performance": [lab_performance],
            "Previous CGPA": [previous_gpa],
            "Study Hours": [study_hours],
            "Participation": [participation],
            "Backlogs": [backlogs],
        })
        predicted_gpa = round(float(np.clip(model.predict(features)[0], 0.0, 10.0)), 2)
    else:
        raw_gpa = (
        (attendance * 0.15) +
        (internal_marks * 0.25) +
        (assignment_score * 0.15) +
        (lab_performance * 0.10) +
        ((previous_gpa * 10.0) * 0.20) +
        (min(study_hours * 15.0, 100.0) * 0.10) +
        (participation * 0.05) -
        (backlogs * 5.0)
        ) / 10.0
        predicted_gpa = round(float(np.clip(raw_gpa, 0.0, 10.0)), 2)

    risk_level = risk_for(predicted_gpa, attendance, backlogs)

    factors = []
    if attendance < 75.0:
        factors.append(f"Low Attendance ({attendance}%)")
    if internal_marks < 55.0:
        factors.append(f"Low Internal Marks ({internal_marks}/100)")
    if study_hours < 2.0:
        factors.append(f"Low Study Hours ({study_hours} hrs/day)")
    if backlogs > 0:
        factors.append(f"Active Backlogs ({backlogs})")
    if not factors:
        factors.append("Consistent performance across metrics")

    recommendations = []
    if attendance < 75.0:
        recommendations.append("Improve attendance above minimum 75% threshold")
    if internal_marks < 60.0:
        recommendations.append("Attend specialized faculty doubt-clearing sessions")
    if study_hours < 3.0:
        recommendations.append("Increase daily self-study duration to at least 3 hours/day")
    if backlogs > 0:
        recommendations.append("Enroll in remedial courses to clear active backlogs")
    if assignment_score < 70.0:
        recommendations.append("Submit periodic assignments and revision sheets on time")
    if not recommendations:
        recommendations.append("Maintain existing academic routine; explore advanced electives")

    return predicted_gpa, risk_level, factors, recommendations

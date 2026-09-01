from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    semester: int = Field(1, ge=1, le=8)
    subject: str = Field("Python Programming")
    attendance: float = Field(0.0, ge=0.0, le=100.0)
    internal_marks: float = Field(0.0, ge=0.0, le=100.0)
    assignment_score: float = Field(0.0, ge=0.0, le=100.0)
    lab_performance: float = Field(0.0, ge=0.0, le=100.0)
    previous_gpa: float = Field(0.0, ge=0.0, le=10.0)
    backlogs: int = Field(0, ge=0)
    study_hours: float = Field(0.0, ge=0.0)
    participation_score: float = Field(0.0, ge=0.0, le=100.0)

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    class Config:
        from_attributes = True

class DashboardMetrics(BaseModel):
    total_students: int
    average_gpa: float
    at_risk_students: int
    at_risk_percentage: float
    average_attendance: float
    performance_trend: Dict[str, float]
    risk_distribution: Dict[str, int]
    subject_performance: Dict[str, float]

class PredictionResponse(BaseModel):
    student_id: str
    name: str
    predicted_gpa: float
    risk_level: str
    main_factors: List[str]
    recommendations: List[str]

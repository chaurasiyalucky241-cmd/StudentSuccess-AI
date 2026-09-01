from sqlalchemy import Column, Integer, String, Float
from database.connection import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column("student_name", String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    semester = Column(Integer, nullable=False, default=1)
    subject = Column(String(120), nullable=False, default="Python Programming")
    attendance = Column(Float, default=0.0)
    internal_marks = Column(Float, default=0.0)
    assignment_score = Column(Float, default=0.0)
    lab_performance = Column(Float, default=0.0)
    previous_gpa = Column("previous_cgpa", Float, default=0.0)
    backlogs = Column(Integer, default=0)
    study_hours = Column(Float, default=0.0)
    participation_score = Column("participation", Float, default=0.0)

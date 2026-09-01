import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine, SessionLocal
from models.student import Student
from routes import student_router, analytics_router, predictions_router

Base.metadata.create_all(bind=engine)

def seed_initial_data():
    db = SessionLocal()
    try:
        target_students = 1000
        existing_count = db.query(Student).count()
        if existing_count >= target_students:
            return

        first_names = [
            "Aarav", "Ananya", "Vihaan", "Diya", "Arjun", "Ishita", "Kabir", "Meera",
            "Rohan", "Saanvi", "Aditya", "Prisha", "Yuvraj", "Aisha", "Kunal", "Naina",
            "Tanmay", "Khushi", "Dev", "Pooja", "Rahul", "Riya", "Aman", "Sneha", "Harsh",
            "Mira", "Vivaan", "Aditi", "Nikhil", "Tanya", "Manav", "Sara", "Aryan", "Jiya",
            "Rudra", "Pranav", "Anvi", "Hritik", "Zenya", "Om", "Aarohi", "Ira", "Vansh",
            "Shreya", "Parth", "Nidhi", "Krishna", "Lakshmi", "Rajat", "Samaira", "Varun"
        ]
        last_names = [
            "Sharma", "Verma", "Patel", "Reddy", "Nair", "Singh", "Kumar", "Iyer",
            "Gupta", "Chawla", "Joshi", "Malhotra", "Kapoor", "Saini", "Mehta", "Bose",
            "Saxena", "Khanna", "Das", "Yadav", "Khan", "Goyal", "Pandey", "Roy", "Tripathi",
            "Sen", "Mishra", "Shah", "Rao", "Menon", "Kulkarni", "Rastogi", "Agarwal", "Jain",
            "Krishna", "Dutta", "Bhatia", "Sethi", "Thakur", "Sondhi", "Chopra", "Pathak", "Nandan",
            "Bharadwaj", "Tiwari", "Kaur", "Suri", "Ghosh", "Venkatesh", "Raghavan", "Naidu"
        ]
        semester_subjects = {
            2: ["Mathematics", "English", "EVS", "Hindi", "Computer Science"],
            3: ["Mathematics", "Science", "Social Science", "English", "Computer Science"],
            4: ["Mathematics", "Science", "Social Science", "English", "Computer Science"],
            5: ["Physics", "Chemistry", "Biology", "English", "Mathematics"],
            6: ["Physics", "Chemistry", "Biology", "Computer Science", "Mathematics"]
        }

        students_to_add = []
        for index in range(existing_count + 1, target_students + 1):
            semester = ((index - 1) % 5) + 2
            subject = semester_subjects[semester][(index - 1) % len(semester_subjects[semester])]
            first_name = first_names[(index * 7) % len(first_names)]
            last_name = last_names[(index * 11 + 3) % len(last_names)]
            name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}{index}@university.edu"
            student_id = f"STU{index:04d}"

            students_to_add.append(
                Student(
                    student_id=student_id,
                    name=name,
                    email=email,
                    semester=semester,
                    subject=subject,
                    attendance=float((index * 13) % 101),
                    internal_marks=float((index * 17) % 101),
                    assignment_score=float((index * 19) % 101),
                    lab_performance=float((index * 23) % 101),
                    previous_gpa=round(4.0 + ((index * 7) % 51) / 10.0, 1),
                    backlogs=(index % 3),
                    study_hours=float(1.0 + ((index * 5) % 7)),
                    participation_score=float((index * 29) % 101),
                )
            )

        if students_to_add:
            db.add_all(students_to_add)
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

seed_initial_data()

app = FastAPI(
    title="StudentSuccess AI Backend",
    description="REST API for Student Performance Prediction & Risk Intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router)
app.include_router(analytics_router)
app.include_router(predictions_router)

@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "StudentSuccess AI Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

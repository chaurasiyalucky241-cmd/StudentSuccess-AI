import sqlite3
from pathlib import Path


def ensure_schema(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            semester INTEGER NOT NULL DEFAULT 1,
            subject TEXT NOT NULL DEFAULT 'Python Programming',
            attendance REAL DEFAULT 0.0,
            internal_marks REAL DEFAULT 0.0,
            assignment_score REAL DEFAULT 0.0,
            lab_performance REAL DEFAULT 0.0,
            previous_cgpa REAL DEFAULT 0.0,
            backlogs INTEGER DEFAULT 0,
            study_hours REAL DEFAULT 0.0,
            participation REAL DEFAULT 0.0
        )
        """
    )
    conn.commit()


def seed_students(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM students")

    first_names = [
        "Aarav", "Ananya", "Vihaan", "Diya", "Arjun", "Ishita", "Kabir", "Meera",
        "Rohan", "Saanvi", "Aditya", "Prisha", "Yuvraj", "Aisha", "Kunal", "Naina",
        "Tanmay", "Khushi", "Dev", "Pooja", "Rahul", "Riya", "Aman", "Sneha", "Harsh",
        "Mira", "Vivaan", "Aditi", "Nikhil", "Tanya", "Manav", "Sara", "Aryan", "Jiya",
        "Rudra", "Pranav", "Anvi", "Hritik", "Zenya", "Om", "Aarohi", "Ira", "Vansh",
        "Shreya", "Parth", "Nidhi", "Krishna", "Lakshmi", "Rajat", "Samaira", "Varun",
        "Kartik", "Yash", "Manya", "Ojas", "Harini", "Amanpreet", "Ayesha", "Veda",
        "Eshan", "Dhruv", "Gauri", "Ivaan", "Priya", "Neel", "Suhani", "Yamini", "Arnav",
        "Bhavya", "Chetan", "Disha", "Esha", "Farhan", "Gautam", "Himanshi", "Ishaan",
        "Jasmine", "Kavya", "Luv", "Mihir", "Nupur", "Palak", "Qasim", "Ritika", "Sai",
        "Tara", "Uday", "Vaani", "Waseem", "Xena", "Yug", "Zoya"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Reddy", "Nair", "Singh", "Kumar", "Iyer",
        "Gupta", "Chawla", "Joshi", "Malhotra", "Kapoor", "Saini", "Mehta", "Bose",
        "Saxena", "Khanna", "Das", "Yadav", "Khan", "Goyal", "Pandey", "Roy", "Tripathi",
        "Sen", "Mishra", "Shah", "Rao", "Menon", "Kulkarni", "Rastogi", "Agarwal", "Jain",
        "Krishna", "Dutta", "Bhatia", "Sethi", "Thakur", "Sondhi", "Chopra", "Pathak", "Nandan",
        "Bharadwaj", "Tiwari", "Kaur", "Suri", "Ghosh", "Venkatesh", "Raghavan", "Naidu",
        "Arora", "Banerjee", "Chauhan", "Dhingra", "Emandi", "Furtado", "George", "Haldar",
        "Jalota", "Kale", "Lamba", "Mathew", "Narang", "Oberoi", "Pillai", "Quazi", "Raval",
        "Seth", "Tandon", "Umrania", "Vora", "Walia", "Xavier", "Yezdani", "Zutshi"
    ]
    semester_subjects = {
        2: ["Mathematics", "English", "EVS", "Hindi", "Computer Science"],
        3: ["Mathematics", "Science", "Social Science", "English", "Computer Science"],
        4: ["Mathematics", "Science", "Social Science", "English", "Computer Science"],
        5: ["Physics", "Chemistry", "Biology", "English", "Mathematics"],
        6: ["Physics", "Chemistry", "Biology", "Computer Science", "Mathematics"],
    }

    row_values = []
    for i in range(1, 1001):
        semester = ((i - 1) % 5) + 2
        subject = semester_subjects[semester][(i - 1) % len(semester_subjects[semester])]
        first = first_names[(i * 11) % len(first_names)]
        last = last_names[(i * 7 + 3) % len(last_names)]
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}{i}@university.edu"
        student_id = f"STU{i:04d}"
        attendance = float((i * 13) % 101)
        internal_marks = float((i * 17) % 101)
        assignment_score = float((i * 19) % 101)
        lab_performance = float((i * 23) % 101)
        previous_gpa = round(4.0 + ((i * 7) % 51) / 10.0, 1)
        backlogs = i % 3
        study_hours = float(1.0 + ((i * 5) % 7))
        participation_score = float((i * 29) % 101)

        row_values.append(
            (
                student_id,
                name,
                email,
                semester,
                subject,
                attendance,
                internal_marks,
                assignment_score,
                lab_performance,
                previous_gpa,
                backlogs,
                study_hours,
                participation_score,
            )
        )

    cur.executemany(
        """
        INSERT INTO students (
            student_id,
            student_name,
            email,
            semester,
            subject,
            attendance,
            internal_marks,
            assignment_score,
            lab_performance,
            previous_cgpa,
            backlogs,
            study_hours,
            participation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        row_values,
    )
    conn.commit()


def main():
    db_path = Path(__file__).resolve().parent / "studentsuccess.db"
    conn = sqlite3.connect(db_path)
    ensure_schema(conn)
    seed_students(conn)

    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    counts = conn.execute(
        "SELECT semester, COUNT(*) FROM students GROUP BY semester ORDER BY semester"
    ).fetchall()
    sample = conn.execute(
        "SELECT student_id, student_name, semester, subject FROM students ORDER BY id LIMIT 5"
    ).fetchall()
    print(f"total_students={total}")
    print(f"semester_counts={counts}")
    print(f"sample={sample}")
    conn.close()


if __name__ == "__main__":
    main()

import sqlite3,random,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # web/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                       # CTF-TUCaN/
DB_PATH = os.path.join(BASE_DIR, "database", "app.db")

GRADES = ["1.0","1.3","1.7","2.0","2.3","2.7","3.0","3.3","3.7","4.0","5.0"]
GRADE_WEIGHTS = [2,3,6,8,8,12,12,10,10,9,10]

def generate_grades():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE role = 'student'")
    students = cursor.fetchall()

    cursor.execute("SELECT id FROM courses")
    courses = [row[0] for row in cursor.fetchall()]

    inserted = 0

    for (student_id,) in students:
        selected_courses = random.sample(courses, random.randint(2, 12))

        for course_id in selected_courses:
            grade = random.choices(GRADES, weights=GRADE_WEIGHTS, k=1)[0]

            cursor.execute(
                """
                INSERT INTO grades (student_id, course_id, grade)
                VALUES (?, ?, ?)
                """,
                (student_id, course_id, grade)
            )
            inserted += 1

    conn.commit()
    conn.close()

    print(f"[+] {inserted} grades generated.")

if __name__ == "__main__":
    generate_grades()

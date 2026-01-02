from db import get_db


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            grade TEXT
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS admin_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    """)

    db.commit()

def seed_db():
    db = get_db()

    users = [
        ("student1", "student1", "student"),
        ("student2", "student2", "student"),
        ("admin", "admin", "admin")
    ]

    for user in users:
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            user
        )

    grades = [
        (1, "Math", "12"),
        (1, "Security", "9"),
        (2, "Math", "14"),
        (2, "Security", "8")
    ]

    for grade in grades:
        db.execute(
            "INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
            grade
        )

    db.execute(
        "INSERT INTO admin_notes (content) VALUES (?)",
        ("Internal admin notes",)
    )

    db.commit()


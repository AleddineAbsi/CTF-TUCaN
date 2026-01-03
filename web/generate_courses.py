import sqlite3,os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # web/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                       # CTF-TUCaN/
DB_PATH = os.path.join(BASE_DIR, "database", "app.db")

COURSES = [
    ("04-10-0118/de", "Mathematik I für Informatik", 5.0, "WS2025"),
    ("04-10-0120/de", "Automaten, formale Sprachen und Entscheidbarkeit", 5.0, "WS2025"),
    ("20-00-0004", "Funktionale und objektorientierte Programmierkonzepte", 10.0, "WS2025"),
    ("20-00-0900", "Digitaltechnik", 5.0, "SS2024"),
    ("04-10-0119/de", "Mathematik II für Informatik", 9.0, "SS2024"),
    ("04-10-0121/de", "Aussagenlogik und Prädikatenlogik", 5.0, "WS2025"),
    ("20-00-0005", "Algorithmen und Datenstrukturen", 10.0, "WS2025"),
    ("20-00-0902", "Rechnerorganisation", 5.0, "WS2025"),
    ("20-00-0013", "Modellierung, Spezifikation und Semantik", 5.0, "WS2025"),
    ("20-00-0014", "Visual Computing", 5.0, "WS2025"),
    ("20-00-0017", "Software Engineering", 5.0, "WS2025"),
    ("20-00-0018", "Computersystemsicherheit", 5.0, "WS2025"),
    ("20-00-0903", "Betriebssysteme", 5.0, "WS2025"),
    ("20-00-1150", "Probabilistische Methoden der Informatik", 5.0, "WS2025"),
]

def generate_courses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for course in COURSES:
        cursor.execute(
            """
            INSERT INTO courses (course_code, course_name, ects, semester)
            VALUES (?, ?, ?, ?)
            """,
            course
        )

    conn.commit()
    conn.close()
    print("[+] Courses generated.")

if __name__ == "__main__":
    generate_courses()

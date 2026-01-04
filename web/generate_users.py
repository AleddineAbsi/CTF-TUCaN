import os
import sqlite3
import random
import uuid
import hashlib

# Paths and configuration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # web/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                       # CTF-TUCaN/
DB_PATH = os.path.join(BASE_DIR, "database", "app.db")

NAMES_PATH = os.path.join(PROJECT_ROOT, "wordlists", "names.txt")
FAMILY_NAME_PATH = os.path.join(PROJECT_ROOT, "wordlists", "familynames.txt")
PASSWORDS_PATH = os.path.join(PROJECT_ROOT, "wordlists", "passwords.txt")

EMAIL_DOMAIN = "tu.local"
DEFAULT_ROLE = "student"


# Wordlist loading
def load_wordlist(path):
    """
    Loads a wordlist file into memory.
    Empty lines are ignored and values are normalized.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip().lower() for line in f if line.strip()]


names = load_wordlist(NAMES_PATH)
familynames = load_wordlist(FAMILY_NAME_PATH)
passwords = load_wordlist(PASSWORDS_PATH)

if not names or not passwords:
    raise RuntimeError("Required wordlists are empty or missing.")


# Identifier generation
def generate_username():
    """
    Generates a realistic username using a name-based pattern.
    """
    first = random.choice(names)
    last = random.choice(familynames)
    number = random.randint(1, 999)
    return f"{first}.{last}{number}"


def generate_login():
    """
    Generates a unique internal login identifier.
    """
    return "tu" + uuid.uuid4().hex[:8] + "Da"


# User generation
def generate_users(count):
    """
    Inserts a given number of student users into the database.
    Collisions are skipped.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    inserted = 0

    for _ in range(count):
        login_name = generate_login()
        username = generate_username()
        password_plain = random.choice(passwords)

        # Password hashing is intentionally weak for testing purposes
        password_hash = hashlib.md5(password_plain.encode()).hexdigest()
        email = f"{username}@{EMAIL_DOMAIN}"

        print(
            f"Generating user: {username} "
            f"(login: {login_name}, password: {password_plain})"
        )

        try:
            cursor.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                (login_name, password_hash, DEFAULT_ROLE)
            )

            user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO user_identity (user_id, email)
                VALUES (?, ?)
                """,
                (user_id, email)
            )

            inserted += 1
            print(f"user {username} with password {password_plain} generated successfully.")

        except sqlite3.IntegrityError:
            # In case of identifier collisions, the entry is skipped
            continue

    conn.commit()
    conn.close()

    print(f"{inserted} users generated successfully.")


# Dedicated Markus account 

def generate_markus_user():
    """
    Creates a dedicated test user with known credentials.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    login_name = generate_login()
    username = "markus.brown103"
    password_plain = ""
    password_hash = hashlib.md5(password_plain.encode()).hexdigest()
    email = f"{username}@{EMAIL_DOMAIN}"

    print(
        f"Generating dedicated test user: {username} "
        f"(login: {login_name}, password: {password_plain})"
    )

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            """,
            (login_name, password_hash, DEFAULT_ROLE)
        )

        user_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO user_identity (user_id, email)
            VALUES (?, ?)
            """,
            (user_id, email)
        )

    except sqlite3.IntegrityError:
        # User already exists, no action required
        pass

    conn.commit()
    conn.close()


def generate_admin(password_plain):
    """
    Creates a legacy admin account for testing purposes.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    login_name = generate_login()
    password_md5 = hashlib.md5(password_plain.encode()).hexdigest()

    cursor.execute(
        """
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """,
        (login_name, password_md5, "legacy")
    )

    conn.commit()
    conn.close()

    print("Legacy admin inserted.")


# Script execution
generate_users(734)
generate_admin("fwspsdf1d1fdasw")
generate_admin("legacy123")
generate_users(423)
generate_markus_user()
generate_admin("fwspsdf1d1fdasw")
generate_users(100)
generate_users(429)

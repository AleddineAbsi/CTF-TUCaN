import os, sqlite3, random ,uuid, hashlib
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # web/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                       # CTF-TUCaN/
DB_PATH = os.path.join(BASE_DIR, "database", "app.db")
NAMES_PATH = os.path.join(PROJECT_ROOT, "wordlists", "names.txt")
FAMILY_NAME_PATH = os.path.join(PROJECT_ROOT, "wordlists", "familynames.txt")
PASSWORDS_PATH = os.path.join(PROJECT_ROOT, "wordlists", "passwords.txt")

NUMBER_OF_USERS = 429
EMAIL_DOMAIN = "tu.local"
DEFAULT_ROLE = "student"

# load wordlists
def load_wordlist(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip().lower() for line in f if line.strip()]

names = load_wordlist(NAMES_PATH)
familynames = load_wordlist(FAMILY_NAME_PATH)
passwords = load_wordlist(PASSWORDS_PATH)

if not names or not passwords:
    raise RuntimeError("Wordlists are empty or missing.")

# username generation

def generate_username():
    first = random.choice(names)
    last = random.choice(familynames)
    number = random.randint(1, 999)
    return f"{first}.{last}{number}"


def generate_login():
    return "tu" + uuid.uuid4().hex[:8] +"Da"


# Database user insertion

def generate_users(i):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    inserted = 0
    for _ in range(i):
        login_name = generate_login()
        username = generate_username()
        password_plain = random.choice(passwords)
        password_hash = hashlib.md5(password_plain.encode()).hexdigest()  
        email = f"{username}@{EMAIL_DOMAIN}"
        print(f"Generating user: {username} with credentials: {login_name} with password: {password_plain}")
        try:
            cursor.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                (login_name, password_hash, DEFAULT_ROLE)
            )
            user_id =cursor.lastrowid
            cursor.execute(
             "INSERT INTO user_identity (user_id, email) VALUES (?, ?)",
             (user_id, email)
            )
            inserted += 1
        except sqlite3.IntegrityError:
            # for collisions, simply skip
            continue
    conn.commit()
    conn.close()
    print(f"[+] {inserted} users generated successfully.")


def generate_admin(password_plain):
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    login_name = generate_login()
    password_md5 = hashlib.md5(password_plain.encode()).hexdigest()
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (login_name, password_md5, "legacy")
    )
    db.commit()
    db.close()

    print("Legacy admin inserted.")

generate_users(53)
generate_admin("ofwienfo32fsfw2340adf")
generate_users(142)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
login_name = generate_login()
username = "markus.brown103"
password_plain = ""
password_hash = hashlib.md5(password_plain.encode()).hexdigest() 
email = f"{username}@{EMAIL_DOMAIN}"
print(f"Generating user: {username} with credentials: {login_name} with password: {password_plain}")
try:
    cursor.execute(
        """
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """,
        (login_name, password_hash, DEFAULT_ROLE)
    )
    user_id =cursor.lastrowid
    cursor.execute(
        "INSERT INTO user_identity (user_id, email) VALUES (?, ?)",
        (user_id, email)
    )
except sqlite3.IntegrityError:
    # for collisions, simply skip
    pass
conn.commit()
conn.close()

generate_users(234)
generate_admin("legacy123")
generate_admin("wfewfg2398fsa92k")
generate_users(100)
generate_users(429)







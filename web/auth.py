from flask import request, session, redirect, url_for, render_template
from db import get_db
import hashlib, re

def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = hashlib.md5(password.encode()).hexdigest()

        db = get_db()

        # sql injection (can't use username = OR email = then it breaks the wanted sqlinjection)
        #login via tu-id
        query1 = f"""
        SELECT users.*,user_identity.email
        FROM users
        LEFT JOIN user_identity
        ON users.id = user_identity.user_id
        WHERE username = '{username}'
        AND password = '{password_hash}'
        """
        user = db.execute(query1).fetchone()
        if not user:
            #extra login with email 
            query = f"""
            SELECT users.*, user_identity.email
            FROM users
            LEFT JOIN user_identity
            ON users.id = user_identity.user_id
            WHERE
            user_identity.email = '{username}'
            AND users.password = '{password_hash}'
            """
            user = db.execute(query).fetchone()

            if user:
                # legacy account disabled
                if user["role"] != "student":
                    error = "Account disabled"
                else:
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["role"] = user["role"]
                    email= user["email"]
                    session["display_name"] = get_user_fullname(email)
                    return redirect("/aktuelles")
            else:
                error = "Invalid credentials"
        else:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            email= user["email"]
            session["display_name"] = get_user_fullname(email)
            return redirect("/aktuelles")
    
    return render_template("login.html", error=error)

def logout():
    session.clear()
    return redirect("/login")

def get_user_fullname(email):
    local_part = email.split("@")[0]
    local_part = re.sub(r"\d+$", "", local_part)
    parts = local_part.split(".")
    first_name = parts[0].capitalize()
    last_name = parts[1].capitalize() if len(parts) > 1 else ""
    display_name = f"{first_name} {last_name}".strip()
    return display_name
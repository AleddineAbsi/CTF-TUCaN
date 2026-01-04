from flask import request, session, redirect, url_for, render_template
from db import get_db
import hashlib, re

def login():
    error = None
    try :
        role = session.get("role")
        if session.get("role") == "student":
            return redirect("/aktuelles")
    except Exception:
        pass   

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
        WHERE role = 'student' 
        AND username = '{username}'
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
        if not user:
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
    if session["role"]=="admin":
        session.clear()
        return redirect("/admin")
    else:
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

def admin_login():
    error = None
    try :
        role = session.get("role")
        if session.get("role") == "admin":
            return redirect("/admin/systemstatus")
    except Exception:
        pass   
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = hashlib.md5(password.encode()).hexdigest()

        blacklist = ["--","OR",";"]

        for bad in blacklist:
            if bad in username:
                username = username.replace(bad, "")
        print(f"Sanitized username: {username}")

        db = get_db()
        query = f"""
        SELECT *
        FROM users
        WHERE role IN ('admin', 'legacy')
        AND username = '{username}'
        AND password = '{password_hash}'
        """
        try:
            user = db.execute(query).fetchone()
        except Exception:
            error = f'User {username} with the given password does not match our records.'
            return render_template("admin.html", error=error)
        
        if not user:
            error = f'User {username} with the given password does not match our records.'
        else:
            # legacy account disabled
            if user["role"] == "admin":
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                return redirect("/admin/systemstatus")
            elif user["role"] == "legacy":
                error = "Legacy admin account disabled"
            else:
                error = "Account disabled"
    
    return render_template("admin.html", error=error)
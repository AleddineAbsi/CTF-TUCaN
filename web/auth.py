from flask import request, session, redirect, render_template
from db import get_db
import hashlib
import re


def login():
    """
    Handles student authentication.
    Supports login via username or email address.
    """
    error = None

    # Redirect already authenticated students
    if session.get("role") == "student":
        return redirect("/aktuelles")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Password hashing (intentionally weak for demonstration purposes)
        password_hash = hashlib.md5(password.encode()).hexdigest()

        db = get_db()

        # Primary authentication using username
        # Note: Query is intentionally constructed this way for security testing scenarios
        query_username = f"""
        SELECT users.*, user_identity.email
        FROM users
        LEFT JOIN user_identity
            ON users.id = user_identity.user_id
        WHERE users.role = 'student'
          AND users.username = '{username}'
          AND users.password = '{password_hash}'
        """
        user = db.execute(query_username).fetchone()

        # Fallback authentication using email address
        if not user:
            query_email = f"""
            SELECT users.*, user_identity.email
            FROM users
            LEFT JOIN user_identity
                ON users.id = user_identity.user_id
            WHERE user_identity.email = '{username}'
              AND users.password = '{password_hash}'
            """
            user = db.execute(query_email).fetchone()

        if not user:
            error = "Invalid credentials"
        else:
            # Initialize user session
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            # Display name is derived from the email address
            session["display_name"] = get_user_fullname(user["email"])

            return redirect("/aktuelles")

    return render_template("login.html", error=error)


def logout():
    """
    Clears the current session and redirects the user
    based on their role.
    """
    role = session.get("role")
    session.clear()

    if role == "admin":
        return redirect("/admin_tucan_portal")

    return redirect("/login")


def get_user_fullname(email):
    """
    Derives a readable display name from an email address.
    E-mail is in the format: {first_name}.{last_name}{number}@tu.local
    """
    local_part = email.split("@")[0]

    local_part = re.sub(r"\d+$", "", local_part)

    parts = local_part.split(".")
    first_name = parts[0].capitalize()
    last_name = parts[1].capitalize() if len(parts) > 1 else ""

    return f"{first_name} {last_name}".strip()


def admin_login():
    """
    Handles authentication for administrative users.
    Includes basic input filtering for demonstration purposes.
    """
    error = None

    # Redirect already authenticated admins
    if session.get("role") == "admin":
        return redirect("/admin_tucan_portal/systemstatus")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = hashlib.md5(password.encode()).hexdigest()

        # Minimal blacklist-based input filtering
        # This is intentionally limited and not meant as a secure solution
        blacklist = ["--", "OR", ";"]
        for token in blacklist:
            username = username.replace(token, "")

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
            error = f"User {username} with the given password does not match our records."
            return render_template("admin.html", error=error)

        if not user:
            error = f"User {username} with the given password does not match our records."
        else:
            # Legacy accounts are intentionally blocked
            if user["role"] == "admin":
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                return redirect("/admin_tucan_portal/systemstatus")

            if user["role"] == "legacy":
                error = "Legacy admin account disabled"
            else:
                error = "Account disabled"

    return render_template("admin.html", error=error)

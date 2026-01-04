from functools import wraps
from flask import session, redirect

# Restrict access to authenticated student sessions
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Debug output for session inspection during development
        print("SESSION =", dict(session))

        # Enforce student-only access
        if "user_id" not in session or session.get("role") != "student":
            return redirect("/login")

        return f(*args, **kwargs)

    return wrapper

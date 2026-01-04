from flask import session, redirect, render_template
from db import get_db
import socket, platform


# Render a raw database backup view for administrators
def get_backup_db():
    # Enforce admin-only access
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/admin_tucan_portal")

    db = get_db()

    # Fetch all user credentials for backup purposes
    users = db.execute("""
        SELECT id, username, password, role
        FROM users
    """).fetchall()

    return render_template("backupdb.html", users=users)


# Display basic system and runtime information
def get_system_info():
    # Enforce admin-only access
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/admin_tucan_portal")

    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)

    # Collect system metadata for monitoring/debugging
    system_data = {
        "hostname": hostname,
        "ip": internal_ip,
        "os": platform.system() + " " + platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "working_dir": "/app"
    }

    return render_template("systemstatus.html", system=system_data)

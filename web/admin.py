from flask import session, redirect, render_template
from db import get_db
import os, socket, platform, time


def get_backup_db():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/admin_tucan_portal")

    db = get_db()
    users = db.execute("""
        SELECT id, username, password, role
        FROM users
    """).fetchall()

    return render_template("backupdb.html",users=users)

def get_system_info():
    if not session.get("user_id") or session.get("role") != "admin":
        return redirect("/admin_tucan_portal")
    sysinfo = {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "cwd": os.getcwd()
    }
    return render_template("systemstatus.html", sysinfo=sysinfo)



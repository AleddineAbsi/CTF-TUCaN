from flask import Flask, render_template, abort, session
from datetime import datetime

from db import close_db
from auth import login, logout, admin_login
from utils import login_required
from grades import grades_by_id
from admin import get_backup_db, get_system_info


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "dev-secret-key"


# Global template variables
@app.context_processor
def inject_now():
    """
    Makes the current datetime available in all templates.
    Useful for timestamps.
    """
    return {"now": datetime.now()}


# Authentication routes
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login_route():
    return login()


@app.route("/logout")
def logout_route():
    return logout()



# General user pages
@app.route("/aktuelles")
@login_required
def aktuelles():
    return render_template("aktuelles.html")


@app.route("/about")
@login_required
def about():
    return "About TU-Portal"


@app.route("/service")
@login_required
def service():
    return render_template("service.html")


@app.route("/hilfe")
@login_required
def hilfe():
    return render_template("hilfe.html")


@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

# Grades pages
@app.route("/prufungen")
@app.route("/prufungen/<string:section>")
@app.route("/prufungen/<string:section>/<string:subsection>")
@login_required
def prufungen(section=None, subsection=None):
    """
    Handles all examination-related views.
    Uses URL parameters to avoid unnecessary route duplication.
    """
    if section is None:
        return render_template("prufungen.html")

    if section == "prufungsplan" and subsection is None:
        return render_template("prufungsplan.html")

    if section == "semesterergebnisse" and subsection is None:
        return render_template("semesterergebnisse.html")

    if section == "semesterergebnisse" and subsection == "modulergebnisse":
        return render_template("modulergebnisse.html")

    abort(404)

# Explicit route for grades by id for IDOR exploit
app.add_url_rule("/prufungen/semesterergebnisse/modulergebnisse",view_func=grades_by_id)

# Admin pages
@app.route("/admin_tucan_portal", methods=["GET", "POST"])
def admin_login_route():
    return admin_login()


@app.route("/admin_tucan_portal/systemstatus")
def admin_system_status():
    return get_system_info()


@app.route("/admin_tucan_portal/backupdb")
def admin_backup_db():
    return get_backup_db()



# Debug tools
@app.route("/debug-session")
def debug_session():
    """
    Development-only route to inspect the current session content.
    """
    return str(dict(session))


# Application lifecycle
@app.teardown_appcontext
def teardown_db(exception):
    """
    Ensures the database connection is properly closed
    after each request.
    """
    close_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

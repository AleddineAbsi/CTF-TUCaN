from flask import Flask, render_template, abort, session
from datetime import datetime
from db import close_db
from auth import login,logout,admin_login
from utils import login_required
from grades import grades_by_id
from admin import get_backup_db,get_system_info

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
now=datetime.now()
app.secret_key="dev-secret-key"
app.add_url_rule("/", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/prufungen/semesterergebnisse/modulergebnisse",view_func=grades_by_id)
app.add_url_rule("/admin",view_func=admin_login,methods=["GET", "POST"])
app.add_url_rule("/admin/backupdb",view_func=get_backup_db)
app.add_url_rule("/admin/systemstatus",view_func=get_system_info)


@app.context_processor
def inject_now():
    return {
        "now": datetime.now()
    }

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/aktuelles")
@login_required
def aktuelles():
    return render_template("aktuelles.html")
app.add_url_rule("/aktuelles", view_func=aktuelles)


@app.route("/about")
@login_required
def about():
    return "About TU-Portal"

@app.route("/prufungen")
@app.route("/prufungen/<string:section>")
@app.route("/prufungen/<string:section>/<string:subsection>")
@login_required
def prufungen(section=None, subsection=None):
    if section is None:
        return render_template("prufungen.html")
    if section == "prufungsplan" and subsection is None:
        return render_template("prufungsplan.html")
    if section == "semesterergebnisse" and subsection is None:
        return render_template("semesterergebnisse.html")
    if section == "semesterergebnisse" and subsection == "modulergebnisse":
        return render_template("modulergebnisse.html")
    abort(404)

@app.route("/service")
@login_required
def service():
    return render_template("service.html")

@app.route("/hilfe")
@login_required
def hilfe():
    return render_template("hilfe.html")

@app.route("/admin")
@app.route("/admin/<string:section>")
def admin(section=None):
    if section is None:
        return render_template("admin.html")
    if section == "systemstatus":
        return render_template("systemstatus.html")
    abort(404)




@app.route("/debug-session")
def debug_session():
    #session not defined yet
    return str(dict(session))

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")


@app.teardown_appcontext
def teardown_db(exception):
    close_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

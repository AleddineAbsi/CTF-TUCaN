from flask import Flask, render_template, abort
from datetime import datetime


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
now=datetime.now()


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/aktuelles")
def aktuelles():
    return render_template("aktuelles.html",now=now)

@app.route("/about")
def about():
    return "About TU-Portal"

@app.route("/prufungen")
@app.route("/prufungen/<string:section>")
@app.route("/prufungen/<string:section>/<string:subsection>")
def prufungen(section=None, subsection=None):
    if section is None:
        return render_template("prufungen.html", now=now)
    if section == "prufungsplan" and subsection is None:
        return render_template("prufungsplan.html", now=now)
    if section == "semesterergebnisse" and subsection is None:
        return render_template("semesterergebnisse.html", now=now)
    if section == "semesterergebnisse" and subsection == "modulergebnisse":
        return render_template("modulergebnisse.html", now=now)
    abort(404)

@app.route("/service")
def service():
    return render_template("service.html",now=now)

@app.route("/hilfe")
def hilfe():
    return render_template("hilfe.html",now=now)

@app.route("/admin")
@app.route("/admin/<string:section>")
def admin(section=None):
    if section is None:
        return render_template("admin.html",now=now)
    if section == "systemstatus":
        return render_template("systemstatus.html",now=now)
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

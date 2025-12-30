from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login")
def login():
    now=datetime.now()
    return render_template("aktuelles.php",now=now)

@app.route("/about")
def about():
    return "About TU-Portal"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

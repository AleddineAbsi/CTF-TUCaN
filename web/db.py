import sqlite3
from flask import g

DATABASE = "database/app.db"


def get_db():
    """
    Returns a SQLite database connection bound to the current request context.
    Ensures a single connection is reused per request.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        # Enables dictionary-like access to rows
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closes the database connection at the end of the request lifecycle.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()

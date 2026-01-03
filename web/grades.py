from flask import request, session, redirect, render_template, url_for, send_file
from db import get_db
from utils import login_required
import os

def grades_by_id():
    if not session.get("user_id"):
        return redirect("/login")

    student_id = request.args.get("id")

    # automatically redirect to own id
    if not student_id:
        return redirect(
            url_for(
                "grades_by_id",
                id=session.get("user_id")
            )
        )

    db = get_db()
    rows = db.execute(
        """
        SELECT
            courses.course_code,
            courses.course_name,
            courses.ects,
            courses.semester,
            grades.grade
        FROM grades
        JOIN courses ON grades.course_id = courses.id
        WHERE grades.student_id = ?
        """,
        (student_id,)
    ).fetchall()
    if not rows:
        path = os.path.join(
            os.path.dirname(__file__),
            "internal",
            "dev_todo.txt"
        )
        return send_file(
            path,
            mimetype="text/plain"
        )
    return render_template(
        "modulergebnisse.html",
        grades=rows,
        student_id=student_id
    )

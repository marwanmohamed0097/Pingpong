from flask import Blueprint, render_template, request, redirect, url_for
import os
import sqlite3

nurses_bp = Blueprint("nurses", __name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hospital.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@nurses_bp.before_request
def prepare_nurse_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS nurses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                shift TEXT NOT NULL
            )
        """)


@nurses_bp.route("/nurses", methods=["GET", "POST"])
def nurse_list():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()
        shift = request.form.get("shift", "").strip()

        if not all([name, department, shift]):
            error = "Please complete all fields."
        else:
            with get_connection() as connection:
                connection.execute(
                    "INSERT INTO nurses (name, department, shift) VALUES (?, ?, ?)",
                    (name, department, shift)
                )
            return redirect(url_for("nurses.nurse_list"))

    with get_connection() as connection:
        nurses = connection.execute(
            "SELECT * FROM nurses ORDER BY name"
        ).fetchall()

    return render_template("nurses.html", nurses=nurses, error=error)


@nurses_bp.route("/nurses/<int:nurse_id>/delete", methods=["POST"])
def delete_nurse(nurse_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM nurses WHERE id = ?", (nurse_id,))

    return redirect(url_for("nurses.nurse_list"))

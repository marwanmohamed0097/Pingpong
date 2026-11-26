from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, "hospital.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)


init_db()


@app.route("/")
def dashboard():
    with get_connection() as connection:
        patient_count = connection.execute(
            "SELECT COUNT(*) FROM patients"
        ).fetchone()[0]

    return render_template("index.html", patient_count=patient_count)


@app.route("/patients", methods=["GET", "POST"])
def patients():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not all([name, age_text, gender, phone, address]):
            error = "Please complete all fields."
        else:
            try:
                age = int(age_text)
                if age < 0:
                    error = "Age cannot be negative."
            except ValueError:
                error = "Age must be a whole number."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO patients (name, age, gender, phone, address)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (name, age, gender, phone, address)
                )
            return redirect(url_for("patients"))

    with get_connection() as connection:
        patient_list = connection.execute(
            "SELECT * FROM patients ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "patients.html",
        patients=patient_list,
        error=error
    )


@app.route("/patients/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM patients WHERE id = ?",
            (patient_id,)
        )

    return redirect(url_for("patients"))


if __name__ == "__main__":
    app.run(debug=True)

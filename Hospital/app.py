from flask import Flask, render_template, request, redirect, url_for
from medicine_routes import medicines_bp
from lab_test_routes import lab_tests_bp
from nurse_routes import nurses_bp
import os
import sqlite3

app = Flask(__name__)
from export_routes import exports_bp
app.register_blueprint(exports_bp)
app.register_blueprint(medicines_bp)
app.register_blueprint(lab_tests_bp)
app.register_blueprint(nurses_bp)
DATABASE = os.path.join(app.root_path, "hospital.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
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
        connection.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                phone TEXT NOT NULL,
                availability TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        """)


init_db()


@app.route("/")
def dashboard():
    with get_connection() as connection:
        patient_count = connection.execute(
            "SELECT COUNT(*) FROM patients"
        ).fetchone()[0]
        doctor_count = connection.execute(
            "SELECT COUNT(*) FROM doctors"
        ).fetchone()[0]
        appointment_count = connection.execute(
            "SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled'"
        ).fetchone()[0]

    return render_template(
        "index.html",
        patient_count=patient_count,
        doctor_count=doctor_count,
        appointment_count=appointment_count
    )


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

    return render_template("patients.html", patients=patient_list, error=error)



@app.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id):
    with get_connection() as connection:
        patient = connection.execute(
            "SELECT * FROM patients WHERE id = ?",
            (patient_id,)
        ).fetchone()

    if patient is None:
        return redirect(url_for("patients"))

    form_data = {
        "name": patient["name"],
        "age": patient["age"],
        "gender": patient["gender"],
        "phone": patient["phone"],
        "address": patient["address"]
    }
    error = None

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "address": request.form.get("address", "").strip()
        }

        if not all(form_data.values()):
            error = "Please complete all fields."
        else:
            try:
                age = int(form_data["age"])
                if age < 0:
                    error = "Age cannot be negative."
            except ValueError:
                error = "Age must be a whole number."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    """
                    UPDATE patients
                    SET name = ?, age = ?, gender = ?, phone = ?, address = ?
                    WHERE id = ?
                    """,
                    (
                        form_data["name"],
                        age,
                        form_data["gender"],
                        form_data["phone"],
                        form_data["address"],
                        patient_id
                    )
                )
            return redirect(url_for("patients"))

    return render_template(
        "edit_patient.html",
        patient=form_data,
        error=error
    )
@app.route("/patients/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    return redirect(url_for("patients"))


@app.route("/doctors", methods=["GET", "POST"])
def doctors():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        specialization = request.form.get("specialization", "").strip()
        phone = request.form.get("phone", "").strip()
        availability = request.form.get("availability", "").strip()

        if not all([name, specialization, phone, availability]):
            error = "Please complete all fields."
        else:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO doctors (name, specialization, phone, availability)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, specialization, phone, availability)
                )
            return redirect(url_for("doctors"))

    with get_connection() as connection:
        doctor_list = connection.execute(
            "SELECT * FROM doctors ORDER BY id DESC"
        ).fetchall()

    return render_template("doctors.html", doctors=doctor_list, error=error)



@app.route("/doctors/<int:doctor_id>/edit", methods=["GET", "POST"])
def edit_doctor(doctor_id):
    with get_connection() as connection:
        doctor = connection.execute(
            "SELECT * FROM doctors WHERE id = ?",
            (doctor_id,)
        ).fetchone()

    if doctor is None:
        return redirect(url_for("doctors"))

    form_data = {
        "name": doctor["name"],
        "specialization": doctor["specialization"],
        "phone": doctor["phone"],
        "availability": doctor["availability"]
    }
    error = None

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "specialization": request.form.get("specialization", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "availability": request.form.get("availability", "").strip()
        }

        if not all(form_data.values()):
            error = "Please complete all fields."
        elif form_data["availability"] not in ["Available", "Unavailable"]:
            error = "Please select a valid availability."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    """
                    UPDATE doctors
                    SET name = ?, specialization = ?, phone = ?, availability = ?
                    WHERE id = ?
                    """,
                    (
                        form_data["name"],
                        form_data["specialization"],
                        form_data["phone"],
                        form_data["availability"],
                        doctor_id
                    )
                )
            return redirect(url_for("doctors"))

    return render_template(
        "edit_doctor.html",
        doctor=form_data,
        error=error
    )
@app.route("/doctors/<int:doctor_id>/delete", methods=["POST"])
def delete_doctor(doctor_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    return redirect(url_for("doctors"))


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    error = None

    if request.method == "POST":
        patient_id_text = request.form.get("patient_id", "").strip()
        doctor_id_text = request.form.get("doctor_id", "").strip()
        appointment_date = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()

        try:
            patient_id = int(patient_id_text)
            doctor_id = int(doctor_id_text)
        except ValueError:
            error = "Please select a patient and a doctor."

        if not appointment_date or not appointment_time:
            error = "Please select a date and time."

        if error is None:
            with get_connection() as connection:
                patient = connection.execute(
                    "SELECT id FROM patients WHERE id = ?",
                    (patient_id,)
                ).fetchone()
                doctor = connection.execute(
                    "SELECT id, availability FROM doctors WHERE id = ?",
                    (doctor_id,)
                ).fetchone()

                if patient is None:
                    error = "The selected patient was not found."
                elif doctor is None:
                    error = "The selected doctor was not found."
                elif doctor["availability"] != "Available":
                    error = "The selected doctor is not available."
                else:
                    conflict = connection.execute(
                        """
                        SELECT id FROM appointments
                        WHERE appointment_date = ?
                          AND appointment_time = ?
                          AND status = 'Scheduled'
                          AND (patient_id = ? OR doctor_id = ?)
                        """,
                        (appointment_date, appointment_time, patient_id, doctor_id)
                    ).fetchone()

                    if conflict:
                        error = "The patient or doctor already has an appointment at that time."
                    else:
                        connection.execute(
                            """
                            INSERT INTO appointments
                                (patient_id, doctor_id, appointment_date, appointment_time)
                            VALUES (?, ?, ?, ?)
                            """,
                            (patient_id, doctor_id, appointment_date, appointment_time)
                        )

            if error is None:
                return redirect(url_for("appointments"))

    with get_connection() as connection:
        patient_list = connection.execute(
            "SELECT id, name FROM patients ORDER BY name"
        ).fetchall()
        doctor_list = connection.execute(
            "SELECT id, name, specialization FROM doctors "
            "WHERE availability = 'Available' ORDER BY name"
        ).fetchall()
        appointment_list = connection.execute("""
            SELECT appointments.id, patients.name AS patient_name,
                   doctors.name AS doctor_name, doctors.specialization,
                   appointments.appointment_date, appointments.appointment_time,
                   appointments.status
            FROM appointments
            JOIN patients ON patients.id = appointments.patient_id
            JOIN doctors ON doctors.id = appointments.doctor_id
            ORDER BY appointments.appointment_date, appointments.appointment_time
        """).fetchall()

    return render_template(
        "appointments.html",
        patients=patient_list,
        doctors=doctor_list,
        appointments=appointment_list,
        error=error
    )



@app.route("/appointments/<int:appointment_id>/edit", methods=["GET", "POST"])
def edit_appointment(appointment_id):
    with get_connection() as connection:
        appointment = connection.execute(
            "SELECT * FROM appointments WHERE id = ?",
            (appointment_id,)
        ).fetchone()

    if appointment is None or appointment["status"] != "Scheduled":
        return redirect(url_for("appointments"))

    form_data = {
        "patient_id": str(appointment["patient_id"]),
        "doctor_id": str(appointment["doctor_id"]),
        "appointment_date": appointment["appointment_date"],
        "appointment_time": appointment["appointment_time"]
    }
    error = None

    if request.method == "POST":
        form_data = {
            "patient_id": request.form.get("patient_id", "").strip(),
            "doctor_id": request.form.get("doctor_id", "").strip(),
            "appointment_date": request.form.get("appointment_date", "").strip(),
            "appointment_time": request.form.get("appointment_time", "").strip()
        }

        try:
            patient_id = int(form_data["patient_id"])
            doctor_id = int(form_data["doctor_id"])
        except ValueError:
            error = "Please select a patient and a doctor."

        if not form_data["appointment_date"] or not form_data["appointment_time"]:
            error = "Please select a date and time."

        if error is None:
            with get_connection() as connection:
                patient = connection.execute(
                    "SELECT id FROM patients WHERE id = ?", (patient_id,)
                ).fetchone()
                doctor = connection.execute(
                    "SELECT id, availability FROM doctors WHERE id = ?", (doctor_id,)
                ).fetchone()

                if patient is None:
                    error = "The selected patient was not found."
                elif doctor is None:
                    error = "The selected doctor was not found."
                elif doctor["availability"] != "Available":
                    error = "The selected doctor is not available."
                else:
                    conflict = connection.execute(
                        """
                        SELECT id FROM appointments
                        WHERE appointment_date = ?
                          AND appointment_time = ?
                          AND status = 'Scheduled'
                          AND id != ?
                          AND (patient_id = ? OR doctor_id = ?)
                        """,
                        (
                            form_data["appointment_date"],
                            form_data["appointment_time"],
                            appointment_id,
                            patient_id,
                            doctor_id
                        )
                    ).fetchone()

                    if conflict:
                        error = "The patient or doctor already has an appointment at that time."
                    else:
                        connection.execute(
                            """
                            UPDATE appointments
                            SET patient_id = ?, doctor_id = ?,
                                appointment_date = ?, appointment_time = ?
                            WHERE id = ?
                            """,
                            (
                                patient_id,
                                doctor_id,
                                form_data["appointment_date"],
                                form_data["appointment_time"],
                                appointment_id
                            )
                        )

            if error is None:
                return redirect(url_for("appointments"))

    with get_connection() as connection:
        patient_list = connection.execute(
            "SELECT id, name FROM patients ORDER BY name"
        ).fetchall()
        doctor_list = connection.execute(
            "SELECT id, name, specialization FROM doctors ORDER BY name"
        ).fetchall()

    return render_template(
        "edit_appointment.html",
        appointment=form_data,
        patients=patient_list,
        doctors=doctor_list,
        error=error
    )
@app.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
def cancel_appointment(appointment_id):
    with get_connection() as connection:
        connection.execute(
            "UPDATE appointments SET status = 'Cancelled' WHERE id = ?",
            (appointment_id,)
        )
    return redirect(url_for("appointments"))


if __name__ == "__main__":
    app.run(debug=True)








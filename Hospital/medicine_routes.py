from flask import Blueprint, render_template, request, redirect, url_for
import os
import sqlite3

medicines_bp = Blueprint("medicines", __name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hospital.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@medicines_bp.before_request
def prepare_medicine_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)


@medicines_bp.route("/medicines", methods=["GET", "POST"])
def medicine_list():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        quantity_text = request.form.get("quantity", "").strip()
        price_text = request.form.get("price", "").strip()

        if not all([name, quantity_text, price_text]):
            error = "Please complete all fields."
        else:
            try:
                quantity = int(quantity_text)
                price = float(price_text)
                if quantity < 0 or price < 0:
                    error = "Quantity and price cannot be negative."
            except ValueError:
                error = "Quantity must be a whole number and price must be numeric."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    "INSERT INTO medicines (name, quantity, price) VALUES (?, ?, ?)",
                    (name, quantity, price)
                )
            return redirect(url_for("medicines.medicine_list"))

    with get_connection() as connection:
        medicines = connection.execute(
            "SELECT * FROM medicines ORDER BY name"
        ).fetchall()

    return render_template("medicines.html", medicines=medicines, error=error)


@medicines_bp.route("/medicines/<int:medicine_id>/edit", methods=["GET", "POST"])
def edit_medicine(medicine_id):
    with get_connection() as connection:
        medicine = connection.execute(
            "SELECT * FROM medicines WHERE id = ?",
            (medicine_id,)
        ).fetchone()

    if medicine is None:
        return redirect(url_for("medicines.medicine_list"))

    form_data = {
        "name": medicine["name"],
        "quantity": medicine["quantity"],
        "price": medicine["price"]
    }
    error = None

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "quantity": request.form.get("quantity", "").strip(),
            "price": request.form.get("price", "").strip()
        }

        if not all(form_data.values()):
            error = "Please complete all fields."
        else:
            try:
                quantity = int(form_data["quantity"])
                price = float(form_data["price"])
                if quantity < 0 or price < 0:
                    error = "Quantity and price cannot be negative."
            except ValueError:
                error = "Quantity must be a whole number and price must be numeric."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    """
                    UPDATE medicines
                    SET name = ?, quantity = ?, price = ?
                    WHERE id = ?
                    """,
                    (form_data["name"], quantity, price, medicine_id)
                )
            return redirect(url_for("medicines.medicine_list"))

    return render_template(
        "edit_medicine.html",
        medicine=form_data,
        error=error
    )


@medicines_bp.route("/medicines/<int:medicine_id>/delete", methods=["POST"])
def delete_medicine(medicine_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM medicines WHERE id = ?",
            (medicine_id,)
        )

    return redirect(url_for("medicines.medicine_list"))

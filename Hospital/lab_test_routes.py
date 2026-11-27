from flask import Blueprint, render_template, request, redirect, url_for
import os
import sqlite3

lab_tests_bp = Blueprint("lab_tests", __name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hospital.db")


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@lab_tests_bp.before_request
def prepare_lab_test_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS laboratory_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                test_type TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)


@lab_tests_bp.route("/lab-tests", methods=["GET", "POST"])
def test_list():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        test_type = request.form.get("test_type", "").strip()
        price_text = request.form.get("price", "").strip()

        if not all([name, test_type, price_text]):
            error = "Please complete all fields."
        else:
            try:
                price = float(price_text)
                if price < 0:
                    error = "Price cannot be negative."
            except ValueError:
                error = "Price must be numeric."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO laboratory_tests (name, test_type, price)
                    VALUES (?, ?, ?)
                    """,
                    (name, test_type, price)
                )
            return redirect(url_for("lab_tests.test_list"))

    with get_connection() as connection:
        tests = connection.execute(
            "SELECT * FROM laboratory_tests ORDER BY name"
        ).fetchall()

    return render_template("lab_tests.html", tests=tests, error=error)



@lab_tests_bp.route("/lab-tests/<int:test_id>/edit", methods=["GET", "POST"])
def edit_test(test_id):
    with get_connection() as connection:
        test = connection.execute(
            "SELECT * FROM laboratory_tests WHERE id = ?",
            (test_id,)
        ).fetchone()

    if test is None:
        return redirect(url_for("lab_tests.test_list"))

    form_data = {
        "name": test["name"],
        "test_type": test["test_type"],
        "price": test["price"]
    }
    error = None

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "test_type": request.form.get("test_type", "").strip(),
            "price": request.form.get("price", "").strip()
        }

        if not all(form_data.values()):
            error = "Please complete all fields."
        else:
            try:
                price = float(form_data["price"])
                if price < 0:
                    error = "Price cannot be negative."
            except ValueError:
                error = "Price must be numeric."

        if error is None:
            with get_connection() as connection:
                connection.execute(
                    """
                    UPDATE laboratory_tests
                    SET name = ?, test_type = ?, price = ?
                    WHERE id = ?
                    """,
                    (form_data["name"], form_data["test_type"], price, test_id)
                )
            return redirect(url_for("lab_tests.test_list"))

    return render_template(
        "edit_lab_test.html",
        test=form_data,
        error=error
    )
@lab_tests_bp.route("/lab-tests/<int:test_id>/delete", methods=["POST"])
def delete_test(test_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM laboratory_tests WHERE id = ?",
            (test_id,)
        )

    return redirect(url_for("lab_tests.test_list"))


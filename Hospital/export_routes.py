from flask import Blueprint, send_file
from pathlib import Path
from io import BytesIO, StringIO
import csv
import sqlite3

exports_bp = Blueprint("exports", __name__)
DATABASE = Path(__file__).resolve().parent / "hospital.db"


@exports_bp.route("/patients/export.csv")
def export_patients():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM patients ORDER BY id").fetchall()

    output = StringIO()
    if rows:
        writer = csv.writer(output)
        writer.writerow(rows[0].keys())
        for row in rows:
            writer.writerow(tuple(row))

    file_data = BytesIO(output.getvalue().encode("utf-8-sig"))
    return send_file(
        file_data,
        mimetype="text/csv",
        as_attachment=True,
        download_name="patients.csv"
    )

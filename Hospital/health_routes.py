from flask import Blueprint, jsonify
from pathlib import Path
import sqlite3

health_bp = Blueprint("health", __name__)
DATABASE = Path(__file__).resolve().parent / "hospital.db"


@health_bp.route("/health")
def health_check():
    try:
        with sqlite3.connect(DATABASE) as connection:
            connection.execute("SELECT 1")
        return jsonify({"status": "ok", "database": "connected"}), 200
    except sqlite3.Error:
        return jsonify({"status": "error", "database": "unavailable"}), 503

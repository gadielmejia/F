from flask import jsonify
from sqlalchemy import text

from app.database.database import db

health_bp = __import__("flask").Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    try:
        db.session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    status = "ok" if db_ok else "db_error"
    return jsonify({"status": status}), 200

from flask import render_template
from app.admin import admin_bp
from app.db import get_db_connection
from app.utils.decorators import role_required

@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        result = {}
        for table in ("users", "students", "companies", "placements"):
            cur.execute(f"SELECT COUNT(*) AS total FROM {table}")
            result[table] = cur.fetchone()["total"]
    finally:
        cur.close()
        conn.close()
    return render_template("admin/dashboard.html", counts=result)
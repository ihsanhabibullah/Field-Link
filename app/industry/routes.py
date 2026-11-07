from flask import render_template, session
from app.industry import industry_bp
from app.db import get_db_connection
from app.utils.decorators import role_required

@industry_bp.get("/dashboard")
@role_required("industry")
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """SELECT p.placement_id, s.student_code, s.full_name, c.company_name,
                      p.start_date, p.end_date, p.status
               FROM placements p JOIN students s ON s.student_id=p.student_id
               JOIN companies c ON c.company_id=p.company_id
               WHERE p.industry_supervisor_id=%s ORDER BY s.full_name""",
            (session["user_id"],),
        )
        students = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return render_template("industry/dashboard.html", students=students)
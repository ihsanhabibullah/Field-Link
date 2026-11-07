import bcrypt
from flask import render_template, request, redirect, url_for, session, flash
from app.auth import auth_bp
from app.db import get_db_connection

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT user_id, full_name, password_hash, role FROM users WHERE username=%s OR email=%s LIMIT 1",
                (identity, identity),
            )
            user = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        valid = False
        if user:
            try:
                valid = bcrypt.checkpw(password.encode(), user["password_hash"].encode())
            except (ValueError, AttributeError):
                valid = False
        if not valid:
            flash("Identitas atau kata sandi tidak sesuai.", "error")
            return render_template("auth/login.html")
        session.clear()
        session.permanent = True
        session["user_id"] = user["user_id"]
        session["full_name"] = user["full_name"]
        session["role"] = user["role"]
        return redirect(url_for("index"))
    return render_template("auth/login.html")

@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
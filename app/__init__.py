from flask import Flask, redirect, url_for, session, render_template
from flask_wtf.csrf import CSRFProtect
from config import Config

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    Config.validate()
    csrf.init_app(app)

    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.teacher import teacher_bp
    from app.industry import industry_bp
    from app.integration import integration_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(industry_bp)
    app.register_blueprint(integration_bp)

    @app.get("/")
    def index():
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        endpoint = {"admin": "admin.dashboard", "teacher": "teacher.dashboard", "industry": "industry.dashboard"}
        return redirect(url_for(endpoint.get(session.get("role"), "auth.login")))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html"), 500
    return app
from flask import Blueprint
integration_bp = Blueprint("integration", __name__, url_prefix="/integration")
from app.integration import routes
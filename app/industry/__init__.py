from flask import Blueprint
industry_bp = Blueprint("industry", __name__, url_prefix="/industry")
from app.industry import routes
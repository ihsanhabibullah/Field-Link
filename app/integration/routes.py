from flask import jsonify
from app.integration import integration_bp
from app.integration.actrace_client import check_health
from app.utils.decorators import role_required

@integration_bp.get("/health")
@role_required("admin", "teacher", "industry")
def health():
    result = check_health()
    return jsonify(result), 200 if result["available"] else 503
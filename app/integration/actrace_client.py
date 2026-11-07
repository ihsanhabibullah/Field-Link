import requests
from flask import current_app

def get_student_summary(student_code):
    base = current_app.config.get("ACTRACE_API_URL", "")
    key = current_app.config.get("SHARED_API_KEY", "")
    if not base or not key:
        return {"success": False, "available": False, "message": "Integrasi ACTRACE belum dikonfigurasi."}
    try:
        response = requests.get(
            f"{base}/api/students/{student_code}/summary",
            headers={"X-API-Key": key},
            timeout=current_app.config["API_TIMEOUT"],
        )
        response.raise_for_status()
        data = response.json()
        data["available"] = True
        return data
    except (requests.RequestException, ValueError) as exc:
        current_app.logger.warning("ACTRACE API gagal diakses: %s", exc)
        return {"success": False, "available": False, "message": "ACTRACE sedang tidak dapat dihubungi."}

def check_health():
    base = current_app.config.get("ACTRACE_API_URL", "")
    if not base:
        return {"available": False, "message": "ACTRACE_API_URL belum diisi."}
    try:
        response = requests.get(f"{base}/api/health", timeout=current_app.config["API_TIMEOUT"])
        response.raise_for_status()
        return {"available": True, "message": "ACTRACE online."}
    except requests.RequestException:
        return {"available": False, "message": "ACTRACE offline atau tidak dapat dijangkau."}
# ===============================
# dashboard.py
# ===============================

from flask import Blueprint, jsonify
import datetime

dashboard_bp = Blueprint("dashboard", __name__)

# Temporary in-memory stats (replace with DB later)
stats = {
    "total_logins": 0,
    "failed_logins": 0,
    "simulations_run": 0,
    "attacks_detected": 0
}


@dashboard_bp.route("/stats", methods=["GET"])
def get_stats():
    return jsonify(stats)


# Helper functions (you can call these from other routes)

def log_login(success=True):
    if success:
        stats["total_logins"] += 1
    else:
        stats["failed_logins"] += 1


def log_simulation(attack=False, detected=False):
    stats["simulations_run"] += 1
    if attack and detected:
        stats["attacks_detected"] += 1
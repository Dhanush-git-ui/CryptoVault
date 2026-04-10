# ===============================
# crypto_routes.py
# ===============================

from flask import Blueprint, jsonify, request, current_app, send_from_directory
import datetime
import os
import json
from flask_login import login_required, current_user
from models import db, FileVault, User
from crypto.mdh import run_mdh
from crypto.rsa import run_rsa
from routes.dashboard import log_simulation

crypto_bp = Blueprint("crypto", __name__)


@crypto_bp.route("/simulate", methods=["POST"])
def simulate():

    data = request.get_json() or {}
    attack = data.get("attack", False)

    # Run MDH
    mdh_result = run_mdh(attack=attack)
    msg = data.get("message", "CryptoVault-Secure-Data")

    # If secure → run RSA
    if mdh_result["secure"]:
        rsa_result = run_rsa(mdh_result["P"], mdh_result["Q"], msg=msg)
    else:
        rsa_result = None

    # Log simulation stats
    log_simulation(attack=attack, detected=not mdh_result["secure"])

    return jsonify({
        "mdh": mdh_result,
        "rsa": rsa_result
    })

@crypto_bp.route("/generate_report", methods=["GET"])
def generate_report():
    # 1. Mock Report Data
    report_data = f"CryptoVault SECURE REPORT\n==================\nDate: {datetime.date.today()}\nInstitution: CryptoVault Global\nTotal Assets: $5,240,000,000\nStatus: VERIFIED\n"
    
    # 2. Get Keys (Using fixed primes for the demo signing)
    rsa_keys = run_rsa(17, 41, msg=report_data)
    
    # 3. Create the "Signed" payload
    signed_report = (
        f"{report_data}\n"
        f"--- DIGITAL SIGNATURE ---\n"
        f"RSA_N: {rsa_keys['n']}\n"
        f"RSA_E: {rsa_keys['e']}\n"
        f"CIPHER_HASH: {rsa_keys['encrypted']}\n"
        f"-------------------------\n"
        f"Verified by CryptoVault Engine"
    )

    return jsonify({"file_content": signed_report})

@crypto_bp.route("/vault/send", methods=["POST"])
@login_required
def vault_send():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    shared_with_id_str = request.form.get("shared_with_id")
    shared_with_id = int(shared_with_id_str) if shared_with_id_str else None

    # Simulate encryption by wrapping filename/content in a "secure" container (or timestamp it)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"SECURE_{timestamp}_{file.filename}"
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    # Save to Database
    new_file = FileVault(
        filename=filename,
        owner_id=current_user.id,
        shared_with_id=shared_with_id
    )
    db.session.add(new_file)
    db.session.commit()

    # Log transfer
    return jsonify({
        "status": "Encrypted & Transferred",
        "filename": filename,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    })

@crypto_bp.route("/vault/list", methods=["GET"])
@login_required
def vault_list():
    # Only get files owned by the user or shared with the user
    files = FileVault.query.filter(
        (FileVault.owner_id == current_user.id) | 
        (FileVault.shared_with_id == current_user.id)
    ).all()
    
    output = []
    for f in files:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], f.filename)
        size = os.path.getsize(filepath) if os.path.exists(filepath) else 0

        # Determine how to display the ownership
        if f.owner_id == current_user.id:
            if f.shared_with_id:
                shared_user = db.session.get(User, f.shared_with_id)
                owner_display = f"You -> {shared_user.username}"
            else:
                owner_display = "You (Private)"
        else:
            owner_user = db.session.get(User, f.owner_id)
            owner_display = f"From: {owner_user.username}"
        
        output.append({
            "name": f.filename,
            "size": size,
            "owner": owner_display
        })

    return jsonify(output)

@crypto_bp.route("/vault/download/<filename>", methods=["GET"])
@login_required
def vault_download(filename):
    file = FileVault.query.filter_by(filename=filename).first()
    if not file:
        return jsonify({"error": "File not found"}), 404
        
    # Security check to make sure they have access
    if file.owner_id != current_user.id and file.shared_with_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
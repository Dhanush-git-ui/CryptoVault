# ===============================
# rsa.py
# ===============================

from .utils import gcd, mod_inverse, mod_exp
import random

def text_to_int(text):
    return int.from_bytes(text.encode('utf-8'), 'big')

def int_to_text(n):
    try:
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8')
    except:
        return "[Decoding Error]"

def run_rsa(P, Q, msg="Secret"):

    n = P * Q
    phi = (P - 1) * (Q - 1)

    # Choose e
    e = 3
    while gcd(e, phi) != 1:
        e += 2

    # Compute d
    d = mod_inverse(e, phi)

    # Convert message to int
    if isinstance(msg, str):
        message_int = text_to_int(msg) % n
    else:
        message_int = msg

    # Encrypt
    encrypted = mod_exp(message_int, e, n)

    # Decrypt
    decrypted_int = mod_exp(encrypted, d, n)
    decrypted_text = int_to_text(decrypted_int) if isinstance(msg, str) else str(decrypted_int)

    return {
        "n": n,
        "phi": phi,
        "e": e,
        "d": d,
        "message": msg,
        "encrypted": encrypted,
        "decrypted": decrypted_text
    }
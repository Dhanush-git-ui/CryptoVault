# ===============================
# utils.py
# ===============================

import random

# Check if number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Generate random prime
def generate_prime(start=5, end=50):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num

# Modular exponentiation
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# GCD
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Modular inverse
def mod_inverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None
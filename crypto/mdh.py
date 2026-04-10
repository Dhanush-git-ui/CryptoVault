# ===============================
# mdh.py
# ===============================

from .utils import generate_prime, mod_exp
import random

def run_mdh(attack=False):

    # Step 1: Generate P
    P = generate_prime()

    # Step 2: Send Pn
    Pn = P * 2

    # Step 3: Generate Q
    Q = generate_prime()

    # Step 4: Send Qn
    Qn = P + Q

    # Step 5: Recover Q
    recovered_Q = Qn - P

    # Private keys
    Pa = random.randint(2, 6)
    Pb = random.randint(2, 6)

    # Public keys
    PubA = mod_exp(P, Pa, Q)
    PubB = mod_exp(P, Pb, Q)

    # Secret keys
    SecA = mod_exp(PubB, Pa, Q)
    SecB = mod_exp(PubA, Pb, Q)

    # Simulate attack
    if attack:
        SecB += 1

    # Validation
    secure = (SecA == SecB)

    return {
        "P": P,
        "Q": Q,
        "Pn": Pn,
        "Qn": Qn,
        "PubA": PubA,
        "PubB": PubB,
        "SecA": SecA,
        "SecB": SecB,
        "secure": secure
    }
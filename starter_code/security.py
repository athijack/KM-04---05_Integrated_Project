"""
security.py
------------
Task 6: A basic access-control gate for Thabo's sales reports.

This module covers KM-04 KT08: Data Security (the CIA triad —
Confidentiality, Integrity, Availability — and practical protections
like hashing and access control).

IMPORTANT SECURITY LESSON:
    NEVER store a password as plain text. Always store a HASH of the
    password. We use hashlib.sha256() here for learning purposes.
    In production you would use bcrypt or argon2.

The password for this project is: spaza2026
(The hash below was generated with hash_password("spaza2026"))
"""

import hashlib
import getpass


# SHA-256 hash of the password "spaza2026".
# In a real system this would be stored in the database, not in code.
# See the CIA-triad reflection in README.md for why that would be better.
STORED_PASSWORD_HASH = "13e90618c7fd397a02e6233cfeaca899463a9e9f99c851d6763c63c76b32e620"


def hash_password(plain_text_password: str) -> str:
    """
    Turn a plain-text password into a SHA-256 hash — a fixed-length
    string that CANNOT be reversed back into the original password.

    Args:
        plain_text_password: the password as typed by the user

    Returns:
        the hex-digest string of the SHA-256 hash
    """
    return hashlib.sha256(plain_text_password.encode()).hexdigest()


def check_password(attempt: str, stored_hash: str) -> bool:
    """
    Check whether a login attempt matches the stored hash WITHOUT
    ever comparing plain-text passwords.

    Args:
        attempt: the plain-text password the user just typed
        stored_hash: the hash stored with hash_password()

    Returns:
        True if the attempt's hash matches stored_hash, False otherwise
    """
    return hash_password(attempt) == stored_hash


def login_gate(stored_hash: str, max_attempts: int = 3) -> bool:
    """
    Prompt the user for a password (hidden input via getpass) and
    check it against stored_hash. Allows up to max_attempts tries.

    Returns:
        True if the user authenticated successfully.
        False if they ran out of attempts.
    """
    print("\n" + "=" * 50)
    print("  SECURE AREA — Reports require authentication")
    print("=" * 50)

    for attempt_number in range(1, max_attempts + 1):
        attempt = getpass.getpass(
            f"  Enter password (attempt {attempt_number}/{max_attempts}): "
        )
        if check_password(attempt, stored_hash):
            print("  Access granted. Loading reports...\n")
            return True
        else:
            remaining = max_attempts - attempt_number
            if remaining > 0:
                print(f"  Incorrect password. {remaining} attempt(s) remaining.")
            else:
                print("  Access denied — too many failed attempts.")

    return False


# ---------------------------------------------------------------------
# CIA-TRIAD REFLECTION
# (Answers are in README.md — see the "Data Security" section)
#
# Q1. Confidentiality — how does this login gate support it?
# Q2. Integrity — the login gate does NOT protect data integrity.
#     What in database.py helps with integrity instead?
# Q3. Availability — what is one risk to availability for a project
#     stored only on a laptop, and what would you recommend?
# ---------------------------------------------------------------------


if __name__ == "__main__":
    # Quick test: hash the password and print it
    pw = "spaza2026"
    hashed = hash_password(pw)
    print(f"Hash of '{pw}':\n{hashed}")
    print(f"\nStored hash matches: {check_password(pw, STORED_PASSWORD_HASH)}")

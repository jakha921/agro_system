import hashlib
import os


def hash_password(password, salt):
    # salt convert to bytes
    salted_password = salt.encode('utf-8') + password.encode('utf-8')
    return hashlib.sha256(salted_password).hexdigest()


def verify_password(password, salt, hashed_password):
    salted_password = salt.encode('utf-8') + password.encode('utf-8')
    rehashed_password = hashlib.sha256(salted_password).hexdigest()

    return rehashed_password == hashed_password

# # Example usage
# password = "myPassword123"
# salt, hashed_password = hash_password(password, SALT)
# print("Salt:", salt)
# print("Hashed password:", hashed_password)
#
# # Verify a password
# entered_password = "myPassword123"
# is_match = verify_password(entered_password, SALT, hashed_password)
# print("Password match:", is_match)

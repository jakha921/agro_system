import hashlib
import os


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # Generate a random salt

    password = password.encode('utf-8')
    salted_password = salt + password

    hashed_password = hashlib.sha256(salted_password).hexdigest()
    print('salt:', salt)
    print('hashed_password:', hashed_password)
    return salt, hashed_password


def verify_password(password, salt, hashed_password):
    salted_password = salt + password.encode('utf-8')
    rehashed_password = hashlib.sha256(salted_password).hexdigest()
    return rehashed_password == hashed_password

#
# # Example usage
# password = "myPassword123"
# salt, hashed_password = hash_password(password)
# print("Salt:", salt)
# print("Hashed password:", hashed_password)
#
# # Verify a password
# entered_password = "myPassword123"
# is_match = verify_password(entered_password, salt, hashed_password)
# print("Password match:", is_match)

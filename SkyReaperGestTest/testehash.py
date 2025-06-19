# test_hash.py
import hashlib

SALT = b"SkyReaperSalt2025"

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, 100000).hex()

print("Hash de 'admin123':", hash_password("admin123"))

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from base64 import urlsafe_b64encode
import os

SALT = b"SkyReaperSalt2025"
ITERATIONS = 100_000

def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=ITERATIONS,
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))
    
    
def encrypt_data(password: str, data: bytes) -> bytes:
    key = derive_key(password)
    fernet = Fernet(key)
    return fernet.encrypt(data)
    
    
def decrypt_data(password: str, data: bytes) -> bytes:
    key = derive_key(password)
    fernet = Fernet(key)
    try:
        return fernet.decrypt(data)
    except InvalidToken:
        raise ValueError("❌ Contraseña incorrecta o datos corruptos.")
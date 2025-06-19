import hashlib
import os
from pathlib import Path
from typing import Optional
from logic.config import HASH_PATH

# Salt fijo (deberías cambiarlo si deseas más seguridad por usuario)
SALT = b"SkyReaperSalt2025"

# Función que convierte una contraseña en hash
def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, 100000).hex()

# Guarda el hash de la contraseña maestra
def save_master_password(password: str):
    hashed = hash_password(password)
    os.makedirs(os.path.dirname(HASH_PATH), exist_ok=True)
    with open(HASH_PATH, "w") as f:
        f.write(hashed)
        
# Carga el hash de la contraseña desde archivo
def load_master_hash() -> Optional[str]:
    try:

        if os.path.exists(HASH_PATH):
            with open(HASH_PATH, "r") as f:
                contenido = f.read().strip()
                return contenido if contenido else None
    except Exception:
        
        return None
    
# Compara el hash generado con el hash almacenado
def verify_password(input_password: str, stored_hash: str) -> bool:
    return hash_password(input_password) == stored_hash
    
    
def check_password(password: str) -> bool:
    stored_hash = load_master_hash()
    if stored_hash is None:
        return False
        
    return verify_password(password, stored_hash)
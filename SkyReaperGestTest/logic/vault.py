import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from logic.crypto import encrypt_data, decrypt_data
from logic.config import VAULT_PATH

VAULT_PATH = os.path.join(os.getenv("APPDATA") or "system", "vault.enc")

def save_all_entries(password: str, entries: list) -> bool:
    try:
        encrypted = encrypt_data(password, json.dumps(entries).encode())
        with open(VAULT_PATH, "wb") as f:
            f.write(encrypted)
        return True
        
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el vault: {e}")
        return False

def raw_save_entry(password: str, new_entry: dict) -> bool:
    entries = load_entries(password)
    
    if entries is None:
        entries = []
    entries.append(new_entry)
    return save_all_entries(password, entries)
        
        
        
        
def load_entries(password: str) -> list[dict] | None:
    if not os.path.exists(VAULT_PATH):
        return []
        
        
        
    try:
        with open(VAULT_PATH, "rb") as f:
            encrypted = f.read()
        decrypted = decrypt_data(password, encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"[ERROR] No se pueden cargar las entradas: {e}")
        return []
        
        
        

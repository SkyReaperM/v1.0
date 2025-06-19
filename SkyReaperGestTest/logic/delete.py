import os 
import json
from cryptography.fernet import InvalidToken
from logic.crypto import encrypt_data, decrypt_data
from logic.config import VAULT_PATH
from .vault import load_entries




def delete_entry(password: str, servicio: str, usuario: str) -> bool:
    try:
        if not os.path.exists(VAULT_PATH):
            print("[INFO] Vault no encontrado" )
            return False
        
     # Leer y descifrar el vault
        with open(VAULT_PATH, "rb") as f:
            encrypted = f.read()
        decrypted = decrypt_data(password, encrypted)
        data = json.loads(decrypted.decode())
        
    
        #eliminar servicio por nombre
        updated_data = [
            entry for entry in data 
            if not (entry["servicio"] == servicio and entry["usuario"] == usuario)
        ]
        # Si no se eliminó nada
        if len(updated_data) == len(data):
            print("[INFO] No se encontró la entrada para eliminar")
            return False
         # Volver a cifrar y guardar
        encrypted_updated = encrypt_data(password, json.dumps(updated_data).encode())
        with open(VAULT_PATH, "wb") as f:
            f.write(encrypted_updated)
        return True
        
    except Exception as e:
        print(f"[ERROR] No se pudo eliminar la entrada: {e}")
        return False
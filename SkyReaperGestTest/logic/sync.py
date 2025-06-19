import asyncio
import json
from logic.vault import load_entries
from logic.vault import save_entry as save_entry_to_vault
from logic.vault import delete_entry as delete_entry_from_vault


#entrdas actualizadas

def get_fresh_entries(master_password: str):
    #carga entradas recientes
    try:
        return load_entries(master_password)
    except Exception as e:
        print(f"[SYNC ERROR] No se pudieron cargar entradas {e}")
        return []
        
        
        
#Auto-sync con refresco en background
async def auto_sync(callback, master_password: str, delay: int = 5):
    #sincroniza periodicamente llamando a callback con las nuevas entradas ( usar en on_mount).
    
    while True:
        await asyncio.sleep(delay)
        entries = get_fresh_entries(master_password)
        callback(entries)
        
        
        
#Funciones de subida/descarga externas dummy

def upload_vault(file_path: str):
    #simula subida a un server externo
    print(f"[SYNC] Vault subido desde {file_path}")
    # Aquí iría integración con Dropbox, Google Drive, etc.
    
def download_vault(file_path: str):
    #Simula descarga
    print(f"[SYNC] Vault descargado en {file_path}")
    # Integracion real con api externa
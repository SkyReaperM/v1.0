import os






from logic.vault import load_entries, save_all_entries 
 #"""
    #Guarda una nueva entrada en el vault si no existe una igual.
    #:param master_password: Contraseña maestra del usuario
    #:param new_entry: Diccionario con claves 'servicio', 'usuario', 'contraseña'
    #:return: True si se guardó correctamente, False si hubo error o ya existía
    #"""



def save_entry(master_password: str, new_entry: dict) -> bool:
    
    try:
        entries = load_entries(master_password)
        
        if entries is None:
            print("[ERROR] No se puede cargar el vault (contraseña incorrecta o datos corruptos)")
            return False
        
        for entry in entries:
            if (entry["servicio"] == new_entry["servicio"] and
                entry["usuario"] == new_entry["usuario"]):
                    print("[WARN] Ya existe una entrada igual")
                    return False
                    
        entries.append(new_entry)
        return save_all_entries(master_password, entries)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la entrada: {e}")
        return False
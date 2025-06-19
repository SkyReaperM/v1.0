import os
from logic.vault import load_entries, save_all_entries
from logic.crypto import encrypt_data, decrypt_data
from logic.config import VAULT_PATH, HASH_PATH
import json

TEST_PASSWORD = "TheMaster123"
TEST_ENTRY = {
    "servicio": "diagnostico_servicio",
    "usuario": "diagnostico_usuario",
    "contraseña": "1234"
    
}

def test_guardar_y_cargar():
    print("[*] Probando guardar y cargar entradas...")
    entries = [TEST_ENTRY]
    save_all_entries(TEST_PASSWORD, entries)
    
    loaded = load_entries(TEST_PASSWORD)
    assert any(e["servicio"] == TEST_ENTRY["servicio"] for e in loaded)
    print("[✓] Guardado y cargado exitosamente.")
    
    
    
def test_eliminar_entrada():
    print("[*] Probando eliminación de entradas...")
    #CArgar datos
    entries = load_entries(TEST_PASSWORD)
    entries = [e for e in entries if e["servicio"] != TEST_ENTRY["servicio"]]
    save_all_entries(TEST_PASSWORD, entries)
    
    loaded = load_entries(TEST_ENTRY)
    assert all(e["servicio"] != TEST_ENTRY["servicio"] for e in loaded)
    print("[✓] Eliminación exitosa.")
    
    
def test_encriptado():
    print("[*] Probando cifrado y descifrado...")
    data = json.dumps([TEST_ENTRY]).encode()
    encrypted = encrypt_data(TEST_PASSWORD, data)
    decrypted = encrypt_data(TEST_PASSWORD, encrypted)
    
    result = json.loads(decrypted.decode())
    assert result[0]["servicio"] == TEST_ENTRY["servicio"]
    print("[✓] Cifrado/Descifrado funcional.")
    try:
        decrypted = decrypt_data(password, encrypted)
        if not decrypted.strip():
            data = json.loads(decrypted.decode())
            print("💥 El contenido descifrado está vacío.")
            return
        
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
    
    
def test_archivos_existentes():
    print("[*] Comprobando archivos requeridos...")
    assert os.path.exists(VAULT_PATH), "Falta vault.enc"
    assert os.path.exists(HASH_PATH), "Falta master.hash"
    print("[✓] Archivos requeridos encontrados.")
    
    
def run_all_tests():
    print("🔍 Iniciando diagnóstico del gestor de contraseñas\n")
    try:
        test_guardar_y_cargar()
        test_encriptado()
        test_eliminar_entrada()
        test_archivos_existentes()
        
        print("\n✅ Todos los tests han pasado correctamente.")
    except AssertionError as e:
        print(f"\n❌ Test fallido: {e}")
    except Exception as ex:
        print(f"\n💥 Error inesperado: {ex}")

if __name__ == "__main__":
    run_all_tests()

import os
import traceback

print("🧪 Iniciando tests...")

# --------------------------------------------
# Validación de módulos
try:
    from logic.auth import hash_password, save_master_password, load_master_hash, verify_password, check_password
    from logic.vault import load_entries
    from logic.save import save_entry
    from logic.delete import delete_entry
    from logic.randomizer import generate_random_password
    from logic.setup import is_first_time_setup, setup_master_password
    print("✅ Módulos importados correctamente.")
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    exit(1)
    
# --------------------------------------------
# Validación de contraseña maestra

try:
    if not is_first_time_setup():
        print("⚠️ No existe hash maestro. Se creará uno de prueba.")
        setup_master_password("test_master", "test_master")
        
        
    else:
        print("🔐 Hash maestro detectado.")
    
    if check_password("test_master"):
        print("✅ Contraseña maestra válida.")
        
    else:
        print("❌ Contraseña maestra inválida. El hash guardado no coincide con 'test_master'.")
except Exception as e:
    print(f"❌ Error validando contraseña maestra: {e}")
    traceback.print_exc()
    
    
# --------------------------------------------
# Test de generación de contraseña


try:
    password = generate_random_password(16)
    assert len(password) == 16
    print(f"✅ Contraseña aleatoria generada: {password}")
    
except Exception as e:
    print(f"❌ Error generando contraseña aleatoria: {e}")
    
    
    
# --------------------------------------------
# Test de guardar y leer una entrada
test_entry = {
    "servicio": "test_service",
    "usuario": "test_user",
    "contraseña": "test_password"
}


try:
    save_success = save_entry("test_master", test_entry)
    if save_success:
        print("✅ Entrada guardada correctamente.")
    else:
        print("❌ Error guardando entrada.")
except Exception as e:
    print(f"❌ Excepción guardando entrada: {e}")
    traceback.print_exc()
    
    
# --------------------------------------------
# Test de lectura del vault

try:
    entries = load_entries("test_master")
    if entries:
        print(f"📄 {len(entries)} entradas cargadas.")
        for e in entries:
            print(f"  - {e['servicio']} / {e['usuario']} / {e['contraseña']}")
    else:
        print("⚠️ Vault vacío o no se pudo leer.")
except Exception as e:
    print(f"❌ Error leyendo vault: {e}")
    traceback.print_exc()
    
    
# --------------------------------------------
# Test de eliminación de entrada

try:
    result = delete_entry("test_master", "test_entry", "test_user")
    if result:
         print("✅ Entrada de prueba eliminada.")
    else:
        print("⚠️ Entrada no encontrada o no se eliminó.")
except Exception as e:
    print(f"❌ Error eliminando entrada: {e}")
    traceback.print_exc()

print("\n✅ Test finalizado.")
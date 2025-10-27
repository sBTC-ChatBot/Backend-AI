"""
🧪 Script de prueba para la integración IA + Supabase
Ejecuta este script para probar los comandos de la IA con la base de datos
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_separator():
    print("\n" + "="*80 + "\n")

def test_chat(message):
    """Envía un mensaje al endpoint de chat y muestra la respuesta"""
    print(f"💬 Usuario: {message}")
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message},
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print(f"🤖 IA Respuesta:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def main():
    print("🚀 Iniciando pruebas de IA + Supabase\n")
    print("Asegúrate de que el servidor está corriendo en http://localhost:5000")
    print_separator()
    
    # Test 1: Verificar que el servidor está funcionando
    print("📡 Test 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(json.dumps(response.json(), indent=2))
        print_separator()
    except Exception as e:
        print(f"❌ Error: No se pudo conectar al servidor. ¿Está corriendo?")
        print(f"   Ejecuta: python app.py")
        return
    
    # Test 2: Listar usuarios
    print("📋 Test 2: Listar todos los usuarios")
    test_chat("Muéstrame todos los usuarios")
    print_separator()
    time.sleep(2)
    
    # Test 3: Crear un usuario
    print("➕ Test 3: Crear un nuevo usuario")
    test_chat("Registra un usuario llamado TestUser con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6")
    print_separator()
    time.sleep(2)
    
    # Test 4: Buscar usuario por wallet
    print("🔍 Test 4: Buscar usuario por wallet")
    test_chat("Busca el usuario con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6")
    print_separator()
    time.sleep(2)
    
    # Test 5: Intentar crear usuario duplicado
    print("⚠️ Test 5: Intentar crear usuario duplicado (debería fallar)")
    test_chat("Crea un usuario llamado Duplicado con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6")
    print_separator()
    time.sleep(2)
    
    # Test 6: Consultar balance (blockchain)
    print("💰 Test 6: Consultar balance en blockchain")
    test_chat("¿Cuál es el balance de ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6?")
    print_separator()
    time.sleep(2)
    
    # Test 7: Listar usuarios de nuevo
    print("📋 Test 7: Listar usuarios después de crear uno nuevo")
    test_chat("¿Cuántos usuarios hay registrados?")
    print_separator()
    
    print("✅ Pruebas completadas!")
    print("\n💡 Nota: Si ves errores de Supabase, verifica que:")
    print("   1. Las variables SUPABASE_URL y SUPABASE_KEY estén configuradas en .env")
    print("   2. Las tablas 'users' y 'contacts' existan en Supabase")
    print("   3. Las políticas de RLS permitan acceso público (o ajusta según tu caso)")

if __name__ == "__main__":
    main()

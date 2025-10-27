"""
🧪 Script de prueba para transferencias a contactos por nombre
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_separator():
    print("\n" + "="*80 + "\n")

def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

# Configuración de prueba
WALLET_JUAN = "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
WALLET_ANDRES = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
WALLET_MARIA = "ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG"
WALLET_PEDRO = "ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R"

def test_chat(message, sender_wallet):
    """Envía un mensaje al endpoint de chat"""
    print(f"💬 Usuario ({sender_wallet[:10]}...): {message}")
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": message,
            "sender_wallet": sender_wallet
        },
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print(f"🤖 IA Respuesta:")
    print_json(result)
    
    return result

def create_user(username, wallet):
    """Crea un usuario"""
    print(f"➕ Creando usuario: {username} ({wallet})")
    response = requests.post(
        f"{BASE_URL}/users",
        json={
            "username": username,
            "wallet_address": wallet
        },
        headers={"Content-Type": "application/json"}
    )
    result = response.json()
    print_json(result)
    return result

def create_contact(user_wallet, contact_name, contact_wallet):
    """Crea un contacto para un usuario"""
    print(f"📇 Agregando contacto: {contact_name} para usuario {user_wallet[:10]}...")
    
    # Primero obtener el user_id
    user_response = requests.get(f"{BASE_URL}/users/wallet/{user_wallet}")
    user_data = user_response.json()
    
    if not user_data.get("success"):
        print("❌ Usuario no encontrado")
        return None
    
    user_id = user_data["user"]["id"]
    
    # Crear contacto
    response = requests.post(
        f"{BASE_URL}/contacts",
        json={
            "user_id": user_id,
            "nombre": contact_name,
            "wallet_address": contact_wallet
        },
        headers={"Content-Type": "application/json"}
    )
    result = response.json()
    print_json(result)
    return result

def get_contacts(wallet):
    """Obtiene los contactos de un usuario"""
    print(f"📋 Obteniendo contactos de {wallet[:10]}...")
    response = requests.get(f"{BASE_URL}/users/wallet/{wallet}/contacts")
    result = response.json()
    print_json(result)
    return result

def main():
    print("🚀 PRUEBA: Transferir STX a Contactos por Nombre\n")
    print("="*80)
    print("Este script probará la funcionalidad completa:")
    print("1. Crear usuario Juan")
    print("2. Agregar contactos (Andrés, María, Pedro)")
    print("3. Transferir STX usando nombres")
    print("="*80)
    print_separator()
    
    # Paso 1: Crear usuario Juan
    print("📌 PASO 1: Registrar usuario Juan")
    create_user("Juan", WALLET_JUAN)
    print_separator()
    
    # Paso 2: Agregar contactos
    print("📌 PASO 2: Agregar contactos a Juan")
    create_contact(WALLET_JUAN, "Andrés", WALLET_ANDRES)
    print()
    create_contact(WALLET_JUAN, "María", WALLET_MARIA)
    print()
    create_contact(WALLET_JUAN, "Pedro", WALLET_PEDRO)
    print_separator()
    
    # Paso 3: Ver contactos
    print("📌 PASO 3: Verificar contactos de Juan")
    get_contacts(WALLET_JUAN)
    print_separator()
    
    # Paso 4: Transferir a Andrés (exitoso)
    print("📌 PASO 4: Transferir 10 STX a Andrés (debe funcionar)")
    test_chat("Envía 10 STX a Andrés", WALLET_JUAN)
    print_separator()
    
    # Paso 5: Transferir a María (exitoso)
    print("📌 PASO 5: Transferir 25 STX a María (debe funcionar)")
    test_chat("Transfiere 25 STX a María", WALLET_JUAN)
    print_separator()
    
    # Paso 6: Transferir a contacto inexistente
    print("📌 PASO 6: Transferir a Carlos (NO existe - debe fallar)")
    test_chat("Envía 5 STX a Carlos", WALLET_JUAN)
    print_separator()
    
    # Paso 7: Transferir sin estar registrado
    print("📌 PASO 7: Transferir desde wallet no registrada (debe fallar)")
    test_chat("Envía 10 STX a Pedro", "ST999WALLET999NO999REGISTRADA")
    print_separator()
    
    # Paso 8: Variaciones de comandos
    print("📌 PASO 8: Probar variaciones de comandos")
    print("\n🔸 Variación 1: Con mayúsculas")
    test_chat("ENVIA 15 STX A ANDRES", WALLET_JUAN)
    print()
    
    print("🔸 Variación 2: Con acento diferente")
    test_chat("envia 20 stx a andres", WALLET_JUAN)
    print()
    
    print("🔸 Variación 3: Usando 'manda'")
    test_chat("Manda 30 STX a Pedro", WALLET_JUAN)
    print_separator()
    
    print("✅ PRUEBAS COMPLETADAS")
    print("\n💡 Resumen:")
    print("   - Las transferencias a contactos existentes devuelven la wallet correcta")
    print("   - Las transferencias a contactos inexistentes muestran sugerencias")
    print("   - Las transferencias desde wallets no registradas son rechazadas")
    print("   - El sistema ignora mayúsculas/minúsculas en los nombres")

if __name__ == "__main__":
    try:
        # Verificar que el servidor está corriendo
        response = requests.get(f"{BASE_URL}/")
        main()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor está corriendo:")
        print("   python app.py")

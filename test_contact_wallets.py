"""
Script de prueba para verificar la tabla contact_wallets en Supabase
"""
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("=== TEST: Conexión a Supabase ===")
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_KEY[:20]}...")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente Supabase creado exitosamente\n")
except Exception as e:
    print(f"❌ Error al crear cliente: {e}")
    exit(1)

# Test 1: Verificar si la tabla existe
print("=== TEST 1: Verificar tabla contact_wallets ===")
try:
    response = supabase.table("contact_wallets").select("*").limit(1).execute()
    print(f"✅ Tabla existe. Registros encontrados: {len(response.data)}")
    if response.data:
        print(f"Primer registro: {response.data[0]}")
    print()
except Exception as e:
    print(f"❌ Error al acceder a la tabla: {e}")
    print("⚠️ Asegúrate de crear la tabla con:")
    print("""
    create table public.contact_wallets (
      id uuid default gen_random_uuid() primary key,
      nombre_wallet_agregada text not null,
      wallet_agregada text not null,
      wallet_quien_agrego text not null,
      fecha_creacion timestamptz default now()
    );
    """)
    exit(1)

# Test 2: Insertar un registro de prueba
print("=== TEST 2: Insertar registro de prueba ===")
test_data = {
    "nombre_wallet_agregada": "Wallet de Prueba",
    "wallet_agregada": "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
    "wallet_quien_agrego": "0x2051ebdd86acc8f81989b7cad4b46de1f9536355"
}

try:
    response = supabase.table("contact_wallets").insert(test_data).execute()
    print(f"✅ Registro insertado exitosamente")
    print(f"Datos: {response.data}")
    print()
except Exception as e:
    print(f"❌ Error al insertar: {e}")
    print()

# Test 3: Verificar registros existentes
print("=== TEST 3: Listar todos los registros ===")
try:
    response = supabase.table("contact_wallets").select("*").execute()
    print(f"✅ Total de registros: {len(response.data)}")
    for idx, record in enumerate(response.data, 1):
        print(f"\n{idx}. ID: {record.get('id')}")
        print(f"   Nombre: {record.get('nombre_wallet_agregada')}")
        print(f"   Wallet agregada: {record.get('wallet_agregada')}")
        print(f"   Quien agregó: {record.get('wallet_quien_agrego')}")
        print(f"   Fecha: {record.get('fecha_creacion')}")
except Exception as e:
    print(f"❌ Error al listar: {e}")

print("\n=== FIN DE PRUEBAS ===")

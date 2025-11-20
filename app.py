from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json
from supabase import create_client, Client
from web3 import Web3

# ✅ Cargar variables del entorno (.env)
load_dotenv()

app = Flask(__name__)
CORS(app)

# ==========================
# 🔧 Configuración Scroll Sepolia
# ==========================

# Configuración de Scroll Sepolia
SCROLL_RPC_URL = os.getenv("SCROLL_RPC_URL", "https://sepolia-rpc.scroll.io")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0xD8c566986a9dD489369129b5156fEbF09b3751FD")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")  # Private key para firmar transacciones (opcional)
NETWORK = os.getenv("NETWORK", "scroll-sepolia")
CHAIN_ID = int(os.getenv("CHAIN_ID", "534351"))  # Scroll Sepolia Chain ID

# Inicializar Web3
w3 = Web3(Web3.HTTPProvider(SCROLL_RPC_URL))

# ABI del contrato STXTransfer
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "recipient", "type": "address"}],
        "name": "transferSTX",
        "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "transferSTXWithAmount",
        "outputs": [{"internalType": "bool", "name": "success", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "getBalance",
        "outputs": [{"internalType": "uint256", "name": "balance", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getSenderInfo",
        "outputs": [{"internalType": "address", "name": "sender", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getContractBalance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "recipient", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "TransferCompleted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "recipient", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "errorCode", "type": "uint256"}
        ],
        "name": "TransferFailed",
        "type": "event"
    },
    {"stateMutability": "payable", "type": "receive"},
    {"stateMutability": "payable", "type": "fallback"}
]

# Instanciar contrato
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicializar cliente de Supabase
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Supabase conectado: {SUPABASE_URL}")
    except Exception as e:
        print(f"⚠️ Error al conectar con Supabase: {e}")

# ==========================
# 🏠 Rutas del backend
# ==========================

@app.route("/", methods=["GET"])
def home():
    """Verifica que el servidor esté en funcionamiento."""
    return jsonify({"status": "ok", "message": "✅ Backend Flask funcionando correctamente"})


# ======================================
# 📊 Obtener información de la red
# ======================================
@app.route("/network-info", methods=["GET"])
def network_info():
    """Obtiene información sobre la red Scroll Sepolia."""
    try:
        is_connected = w3.is_connected()
        latest_block = w3.eth.block_number if is_connected else None
        
        return jsonify({
            "network": NETWORK,
            "chain_id": CHAIN_ID,
            "rpc_url": SCROLL_RPC_URL,
            "contract_address": CONTRACT_ADDRESS,
            "is_connected": is_connected,
            "latest_block": latest_block,
            "explorer_url": f"https://sepolia.scrollscan.com/address/{CONTRACT_ADDRESS}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================
# 🤖 Endpoint de chat con DeepSeek
# ======================================
@app.route("/chat", methods=["POST"])
def chat():
    """Interpreta comandos del usuario con IA y responde en formato JSON."""
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        sender_wallet = data.get("sender_wallet", "")  # Wallet del usuario conectado

        if not user_message:
            return jsonify({"action": "none", "message": "No se envió ningún mensaje."}), 400

        # Headers y body para DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente inteligente para interpretar comandos hacia contratos inteligentes "
                        "en la blockchain de Scroll Sepolia (una red compatible con Ethereum) y gestionar usuarios en la base de datos. "
                        f"La wallet del usuario conectado es: {sender_wallet if sender_wallet else 'NO PROPORCIONADA'}. "
                        "Analiza los comandos del usuario y extrae información relevante. "
                        "Devuelve SIEMPRE una respuesta JSON con las siguientes claves:\n\n"
                        
                        "ACCIONES DISPONIBLES:\n"
                        "- 'transfer': Transferir ETH a una wallet directamente (direcciones que empiezan con 0x)\n"
                        "- 'transfer_to_contact': Transferir ETH a un contacto por su nombre\n"
                        "- 'balance': Consultar balance de una wallet\n"
                        "- 'network_info': Obtener información de la red Scroll Sepolia\n"
                        "- 'list_users': Listar todos los usuarios\n"
                        "- 'get_user': Obtener info de un usuario específico\n"
                        "- 'create_user': Crear un nuevo usuario\n"
                        "- 'get_contacts': Obtener contactos de un usuario\n"
                        "- 'create_contact': Crear un nuevo contacto\n"
                        "- 'none': Ninguna acción específica\n\n"
                        
                        "ESTRUCTURA DE RESPUESTA:\n"
                        "- 'action': una de las acciones listadas arriba\n"
                        "- 'message': explicación breve de lo que se hará\n"
                        "- Campos adicionales según la acción:\n\n"
                        
                        "EJEMPLOS:\n\n"
                        
                        "1. Transferencia ETH (por wallet):\n"
                        "Usuario: 'Transfiere 0.5 ETH a 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'\n"
                        "Respuesta: {\"action\": \"transfer\", \"recipient\": \"0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb\", \"amount\": 0.5, \"message\": \"Transferir 0.5 ETH\"}\n\n"
                        
                        "1b. Transferencia ETH (por nombre de contacto):\n"
                        "Usuario: 'Envía 0.1 ETH a Andrés'\n"
                        "Respuesta: {\"action\": \"transfer_to_contact\", \"contact_name\": \"Andrés\", \"amount\": 0.1, \"sender_wallet\": \"0x123...\", \"message\": \"Buscar contacto Andrés y transferir 0.1 ETH\"}\n"
                        "IMPORTANTE: Para esta acción, SIEMPRE incluye el sender_wallet que viene en el contexto del mensaje.\n\n"
                        
                        "2. Balance:\n"
                        "Usuario: '¿Cuál es el balance de 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb?'\n"
                        "Respuesta: {\"action\": \"balance\", \"address\": \"0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb\", \"message\": \"Consultando balance\"}\n\n"
                        
                        "3. Listar usuarios:\n"
                        "Usuario: 'Muéstrame todos los usuarios' o '¿Cuántos usuarios hay?'\n"
                        "Respuesta: {\"action\": \"list_users\", \"message\": \"Obteniendo lista de usuarios\"}\n\n"
                        
                        "4. Buscar usuario:\n"
                        "Usuario: 'Busca el usuario con wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'\n"
                        "Respuesta: {\"action\": \"get_user\", \"wallet_address\": \"0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb\", \"message\": \"Buscando usuario\"}\n\n"
                        
                        "5. Crear usuario:\n"
                        "Usuario: 'Registra un usuario llamado Juan con wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'\n"
                        "Respuesta: {\"action\": \"create_user\", \"username\": \"Juan\", \"wallet_address\": \"0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb\", \"message\": \"Creando usuario Juan\"}\n\n"
                        
                        "6. Ver contactos:\n"
                        "Usuario: 'Muéstrame los contactos del usuario 123e4567-e89b-12d3-a456-426614174000'\n"
                        "Respuesta: {\"action\": \"get_contacts\", \"user_id\": \"123e4567-e89b-12d3-a456-426614174000\", \"message\": \"Obteniendo contactos\"}\n\n"
                        
                        "7. Crear contacto:\n"
                        "Usuario: 'Agrega a María con wallet 0x742d35... como contacto del usuario 123e4567...'\n"
                        "Respuesta: {\"action\": \"create_contact\", \"user_id\": \"123e4567...\", \"nombre\": \"María\", \"wallet_address\": \"0x742d35...\", \"message\": \"Agregando contacto\"}\n\n"
                        
                        "IMPORTANTE: Las direcciones Ethereum siempre empiezan con '0x' seguido de 40 caracteres hexadecimales."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        }

        # Petición a DeepSeek
        response = requests.post(DEEPSEEK_URL, headers=headers, json=body)
        result = response.json()

        # --------------------------
        # 🔍 Extraer texto de la IA
        # --------------------------
        ia_text = None
        if "choices" in result:
            ia_text = result["choices"][0]["message"]["content"]
        elif "output_text" in result:
            ia_text = result["output_text"]
        elif "data" in result and "output_text" in result["data"]:
            ia_text = result["data"]["output_text"]
        else:
            ia_text = str(result)

        # --------------------------
        # 🧹 Limpiar y parsear JSON
        # --------------------------
        ia_text = ia_text.strip()
        if ia_text.startswith("```"):
            ia_text = ia_text.replace("```json", "").replace("```", "").strip()

        try:
            ia_json = json.loads(ia_text)
        except Exception:
            # Si no es JSON, intentar deducir la acción
            action = "none"
            msg_lower = user_message.lower()
            
            # Detectar si menciona "enviar" o "transferir" con un nombre (no una wallet)
            if ("transferir" in msg_lower or "transfiere" in msg_lower or 
                "enviar" in msg_lower or "envía" in msg_lower or "envia" in msg_lower):
                # Si NO contiene una wallet address Ethereum (0x...)
                if "0x" not in user_message.lower():
                    action = "transfer_to_contact"
                else:
                    action = "transfer"
            elif "balance" in msg_lower or "saldo" in msg_lower:
                action = "balance"
            elif "red" in msg_lower or "network" in msg_lower or "info" in msg_lower:
                action = "network_info"
            elif "usuarios" in msg_lower or "listar usuarios" in msg_lower or "ver usuarios" in msg_lower:
                action = "list_users"
            elif "crear usuario" in msg_lower or "registrar usuario" in msg_lower or "nuevo usuario" in msg_lower:
                action = "create_user"
            elif "contactos" in msg_lower or "ver contactos" in msg_lower:
                action = "get_contacts"
            elif "crear contacto" in msg_lower or "agregar contacto" in msg_lower or "nuevo contacto" in msg_lower:
                action = "create_contact"
            elif "buscar usuario" in msg_lower or "encontrar usuario" in msg_lower:
                action = "get_user"

            ia_json = {"action": action, "message": ia_text}

        # Asegurar que sender_wallet esté presente si fue proporcionado
        if sender_wallet and "sender_wallet" not in ia_json:
            ia_json["sender_wallet"] = sender_wallet

        # ========================================
        # 🤖 EJECUTAR ACCIONES DE BASE DE DATOS
        # ========================================
        action = ia_json.get("action")
        
        # ==========================================
        # 💸 TRANSFERENCIA A CONTACTO POR NOMBRE
        # ==========================================
        if action == "transfer_to_contact":
            contact_name = ia_json.get("contact_name")
            amount = ia_json.get("amount")
            sender_wallet_from_json = ia_json.get("sender_wallet")
            
            # Usar sender_wallet del request si no viene en el JSON de la IA
            if not sender_wallet_from_json and sender_wallet:
                sender_wallet_from_json = sender_wallet
            
            if not sender_wallet_from_json:
                ia_json["error"] = "Se requiere la wallet del remitente (sender_wallet)"
                ia_json["message"] = "❌ Debes proporcionar tu wallet conectada para buscar tus contactos"
            elif not contact_name:
                ia_json["error"] = "No se pudo identificar el nombre del contacto"
                ia_json["message"] = "❌ Por favor especifica el nombre del contacto"
            elif not amount or amount <= 0:
                ia_json["error"] = "No se pudo identificar la cantidad a transferir"
                ia_json["message"] = "❌ Por favor especifica una cantidad válida de STX"
            elif supabase:
                try:
                    # 1. Buscar el usuario por su wallet
                    user_response = supabase.table("users").select("id, username").eq("wallet_address", sender_wallet_from_json).execute()
                    
                    if not user_response.data:
                        ia_json["error"] = "No se encontró un usuario con esa wallet"
                        ia_json["message"] = f"❌ Tu wallet {sender_wallet_from_json} no está registrada. Regístrate primero."
                    else:
                        user_id = user_response.data[0]["id"]
                        username = user_response.data[0]["username"]
                        
                        # 2. Buscar el contacto por nombre (case-insensitive)
                        contacts_response = supabase.table("contacts").select("*").eq("user_id", user_id).execute()
                        
                        if not contacts_response.data:
                            ia_json["error"] = "No tienes contactos registrados"
                            ia_json["message"] = f"❌ {username}, aún no tienes contactos. Agrega algunos primero."
                        else:
                            # Buscar contacto por nombre (ignorando mayúsculas/minúsculas y espacios)
                            contact_found = None
                            search_name = contact_name.strip().lower()
                            
                            for contact in contacts_response.data:
                                if contact["nombre"].strip().lower() == search_name:
                                    contact_found = contact
                                    break
                            
                            if not contact_found:
                                # Intentar búsqueda parcial
                                for contact in contacts_response.data:
                                    if search_name in contact["nombre"].strip().lower():
                                        contact_found = contact
                                        break
                            
                            if contact_found:
                                # ✅ Contacto encontrado, preparar transferencia
                                ia_json["action"] = "transfer"  # Cambiar a acción de transferencia
                                ia_json["recipient"] = contact_found["wallet_address"]
                                ia_json["recipient_name"] = contact_found["nombre"]
                                ia_json["amount"] = amount
                                ia_json["sender"] = sender_wallet_from_json
                                ia_json["contact_id"] = contact_found["id"]
                                ia_json["message"] = f"✅ Contacto '{contact_found['nombre']}' encontrado. Preparando transferencia de {amount} STX a {contact_found['wallet_address']}"
                                ia_json["success"] = True
                            else:
                                # Listar contactos disponibles
                                available_contacts = [c["nombre"] for c in contacts_response.data]
                                ia_json["error"] = f"Contacto '{contact_name}' no encontrado"
                                ia_json["message"] = f"❌ No encontré a '{contact_name}' en tus contactos."
                                ia_json["available_contacts"] = available_contacts
                                ia_json["suggestion"] = f"Contactos disponibles: {', '.join(available_contacts)}"
                
                except Exception as e:
                    ia_json["error"] = f"Error al buscar contacto: {str(e)}"
                    ia_json["message"] = "❌ Hubo un error al buscar en tus contactos"
            else:
                ia_json["error"] = "Supabase no está configurado"
                ia_json["message"] = "❌ La base de datos no está disponible"
        
        # Listar usuarios
        elif action == "list_users":
            try:
                if supabase:
                    response = supabase.table("users").select("*").execute()
                    ia_json["users"] = response.data
                    ia_json["count"] = len(response.data)
                    ia_json["message"] = f"Se encontraron {len(response.data)} usuarios registrados"
                else:
                    ia_json["error"] = "Supabase no está configurado"
            except Exception as e:
                ia_json["error"] = f"Error al obtener usuarios: {str(e)}"
        
        # Buscar usuario por wallet
        elif action == "get_user":
            wallet = ia_json.get("wallet_address")
            if wallet and supabase:
                try:
                    response = supabase.table("users").select("*").eq("wallet_address", wallet).execute()
                    if response.data:
                        ia_json["user"] = response.data[0]
                        ia_json["message"] = f"Usuario encontrado: {response.data[0].get('username')}"
                    else:
                        ia_json["message"] = "No se encontró ningún usuario con esa wallet"
                except Exception as e:
                    ia_json["error"] = f"Error al buscar usuario: {str(e)}"
        
        # Crear usuario
        elif action == "create_user":
            username = ia_json.get("username")
            wallet = ia_json.get("wallet_address")
            if username and wallet and supabase:
                try:
                    response = supabase.table("users").insert({
                        "username": username,
                        "wallet_address": wallet
                    }).execute()
                    ia_json["user"] = response.data[0]
                    ia_json["message"] = f"✅ Usuario '{username}' creado exitosamente"
                except Exception as e:
                    error_msg = str(e)
                    if "duplicate" in error_msg.lower():
                        ia_json["error"] = "Esta wallet ya está registrada"
                    else:
                        ia_json["error"] = f"Error al crear usuario: {error_msg}"
        
        # Obtener contactos de un usuario
        elif action == "get_contacts":
            user_id = ia_json.get("user_id")
            if user_id and supabase:
                try:
                    response = supabase.table("contacts").select("*").eq("user_id", user_id).execute()
                    ia_json["contacts"] = response.data
                    ia_json["count"] = len(response.data)
                    ia_json["message"] = f"Se encontraron {len(response.data)} contactos"
                except Exception as e:
                    ia_json["error"] = f"Error al obtener contactos: {str(e)}"
        
        # Crear contacto
        elif action == "create_contact":
            user_id = ia_json.get("user_id")
            nombre = ia_json.get("nombre")
            wallet = ia_json.get("wallet_address")
            if user_id and nombre and wallet and supabase:
                try:
                    response = supabase.table("contacts").insert({
                        "user_id": user_id,
                        "nombre": nombre,
                        "wallet_address": wallet
                    }).execute()
                    ia_json["contact"] = response.data[0]
                    ia_json["message"] = f"✅ Contacto '{nombre}' agregado exitosamente"
                except Exception as e:
                    error_msg = str(e)
                    if "duplicate" in error_msg.lower():
                        ia_json["error"] = "Este contacto ya existe"
                    else:
                        ia_json["error"] = f"Error al crear contacto: {error_msg}"

        return jsonify(ia_json)

    except Exception as e:
        return jsonify({"action": "none", "message": f"Error: {str(e)}"}), 500


# ======================================
# 💰 Verificar balance de una wallet
# ======================================
@app.route("/api/balance/<address>", methods=["GET"])
def get_balance(address):
    """Consulta el balance de ETH de una dirección en Scroll Sepolia."""
    try:
        if not address:
            return jsonify({"error": "Se requiere una dirección"}), 400
        
        # Validar formato de dirección Ethereum
        if not Web3.is_address(address):
            return jsonify({"error": "Dirección inválida. Debe ser una dirección Ethereum válida"}), 400
        
        # Convertir a checksum address
        checksum_address = Web3.to_checksum_address(address)
        
        # Obtener balance nativo (ETH)
        balance_wei = w3.eth.get_balance(checksum_address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        # Obtener balance según el contrato (si es diferente)
        try:
            contract_balance_wei = contract.functions.getBalance(checksum_address).call()
            contract_balance_eth = w3.from_wei(contract_balance_wei, 'ether')
        except:
            contract_balance_wei = balance_wei
            contract_balance_eth = balance_eth
        
        return jsonify({
            "address": checksum_address,
            "balance": float(balance_eth),
            "balance_wei": str(balance_wei),
            "contract_balance": float(contract_balance_eth),
            "contract_balance_wei": str(contract_balance_wei),
            "message": f"Balance: {balance_eth} ETH",
            "network": NETWORK,
            "chain_id": CHAIN_ID
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta alternativa POST para compatibilidad
@app.route("/get-balance", methods=["POST"])
def get_balance_post():
    """Consulta el balance de ETH (versión POST)."""
    try:
        data = request.get_json()
        address = data.get("address", "")
        
        if not address:
            return jsonify({"error": "Se requiere una dirección"}), 400
        
        # Redirigir a la función principal
        return get_balance(address)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================
# 💸 Preparar transacción de transferencia
# ======================================
@app.route("/prepare-transfer", methods=["POST"])
def prepare_transfer():
    """Prepara los datos para una transferencia de ETH en Scroll Sepolia."""
    try:
        data = request.get_json()
        recipient = data.get("recipient", "")
        amount = data.get("amount", 0)
        sender = data.get("sender", "")
        
        # Validaciones
        if not recipient or not sender:
            return jsonify({
                "error": "Se requieren las direcciones del remitente y destinatario"
            }), 400
        
        if not Web3.is_address(recipient) or not Web3.is_address(sender):
            return jsonify({
                "error": "Dirección inválida. Deben ser direcciones Ethereum válidas"
            }), 400
        
        if amount <= 0:
            return jsonify({
                "error": "El monto debe ser mayor a 0 ETH"
            }), 400
        
        # Convertir a checksum addresses
        recipient_checksum = Web3.to_checksum_address(recipient)
        sender_checksum = Web3.to_checksum_address(sender)
        
        # Convertir ETH a Wei
        amount_wei = w3.to_wei(amount, 'ether')
        
        # Estimar gas
        try:
            gas_estimate = contract.functions.transferSTX(recipient_checksum).estimate_gas({
                'from': sender_checksum,
                'value': amount_wei
            })
            
            gas_price = w3.eth.gas_price
            estimated_fee_wei = gas_estimate * gas_price
            estimated_fee_eth = w3.from_wei(estimated_fee_wei, 'ether')
        except Exception as e:
            gas_estimate = 100000  # Estimación por defecto
            gas_price = w3.eth.gas_price
            estimated_fee_wei = gas_estimate * gas_price
            estimated_fee_eth = w3.from_wei(estimated_fee_wei, 'ether')
        
        # Preparar los datos de la transacción
        transaction_data = {
            "contract_address": CONTRACT_ADDRESS,
            "function_name": "transferSTX",
            "sender": sender_checksum,
            "recipient": recipient_checksum,
            "amount": amount,
            "amount_wei": str(amount_wei),
            "network": NETWORK,
            "chain_id": CHAIN_ID,
            "gas_estimate": gas_estimate,
            "gas_price_wei": str(gas_price),
            "gas_price_gwei": float(w3.from_wei(gas_price, 'gwei')),
            "estimated_fee_eth": float(estimated_fee_eth),
            "estimated_fee_wei": str(estimated_fee_wei),
            "explorer_url": f"https://sepolia.scrollscan.com/address/{CONTRACT_ADDRESS}",
            "message": f"¿Deseas aprobar la transferencia de {amount} ETH a {recipient_checksum}?"
        }
        
        return jsonify(transaction_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================
# ✅ Verificar estado de transacción
# ======================================
@app.route("/check-transaction", methods=["POST"])
def check_transaction():
    """Verifica el estado de una transacción en Scroll Sepolia."""
    try:
        data = request.get_json()
        txid = data.get("txid", "")
        
        if not txid:
            return jsonify({"error": "Se requiere el ID de la transacción"}), 400
        
        # Obtener recibo de transacción
        try:
            tx_receipt = w3.eth.get_transaction_receipt(txid)
            tx = w3.eth.get_transaction(txid)
            
            # Determinar status
            if tx_receipt['status'] == 1:
                status = "success"
                message = "✅ Transacción completada correctamente"
            else:
                status = "failed"
                message = "❌ Transacción fallida"
            
            # Construir URL del explorer
            explorer_url = f"https://sepolia.scrollscan.com/tx/{txid}"
            
            result = {
                "txid": txid,
                "status": status,
                "block_number": tx_receipt['blockNumber'],
                "block_hash": tx_receipt['blockHash'].hex(),
                "from": tx_receipt['from'],
                "to": tx_receipt['to'],
                "gas_used": tx_receipt['gasUsed'],
                "effective_gas_price": tx_receipt['effectiveGasPrice'],
                "value": str(tx['value']),
                "value_eth": float(w3.from_wei(tx['value'], 'ether')),
                "explorer_url": explorer_url,
                "message": message,
                "network": NETWORK,
                "chain_id": CHAIN_ID
            }
            
            return jsonify(result)
            
        except Exception as e:
            # Si no se encuentra el recibo, la transacción está pendiente
            error_str = str(e)
            if "not found" in error_str.lower() or "not been mined" in error_str.lower():
                return jsonify({
                    "txid": txid,
                    "status": "pending",
                    "message": "⏳ Transacción pendiente de confirmación",
                    "explorer_url": f"https://sepolia.scrollscan.com/tx/{txid}",
                    "network": NETWORK,
                    "chain_id": CHAIN_ID
                })
            else:
                raise e
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================
# 🚀 Ejecutar transferencia (endpoint simplificado)
# ======================================
@app.route("/api/transfer", methods=["POST"])
def execute_transfer():
    """Ejecuta una transferencia de ETH usando el contrato en Scroll Sepolia."""
    try:
        data = request.get_json()
        recipient = data.get("recipient", "")
        amount = data.get("amount", 0)
        
        # Validaciones
        if not recipient:
            return jsonify({
                "success": False,
                "error": "Se requiere la dirección del destinatario"
            }), 400
        
        if not Web3.is_address(recipient):
            return jsonify({
                "success": False,
                "error": "Dirección de destinatario inválida"
            }), 400
        
        if amount <= 0:
            return jsonify({
                "success": False,
                "error": "El monto debe ser mayor a 0 ETH"
            }), 400
        
        # Convertir a checksum address
        recipient_checksum = Web3.to_checksum_address(recipient)
        amount_wei = w3.to_wei(amount, 'ether')
        
        # Verificar que tengamos private key configurada
        if not PRIVATE_KEY:
            return jsonify({
                "success": False,
                "error": "Private key no configurada. Esta es una operación de solo lectura."
            }), 500
        
        # Obtener cuenta del remitente
        account = w3.eth.account.from_key(PRIVATE_KEY)
        sender_address = account.address
        
        # Verificar balance suficiente
        balance = w3.eth.get_balance(sender_address)
        if balance < amount_wei:
            return jsonify({
                "success": False,
                "error": f"Balance insuficiente. Tienes {w3.from_wei(balance, 'ether')} ETH"
            }), 400
        
        # Construir transacción
        nonce = w3.eth.get_transaction_count(sender_address)
        
        transaction = contract.functions.transferSTX(recipient_checksum).build_transaction({
            'from': sender_address,
            'value': amount_wei,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': CHAIN_ID
        })
        
        # Firmar transacción
        signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        
        # Enviar transacción
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hash_hex = tx_hash.hex()
        
        # Esperar confirmación (opcional, comentado para no bloquear)
        # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return jsonify({
            "success": True,
            "txHash": tx_hash_hex,
            "amount": amount,
            "recipient": recipient_checksum,
            "explorer_url": f"https://sepolia.scrollscan.com/tx/{tx_hash_hex}",
            "message": f"Transferencia de {amount} ETH enviada correctamente",
            "network": NETWORK
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ======================================
# 👥 ENDPOINTS DE SUPABASE - USUARIOS
# ======================================

@app.route("/users", methods=["GET"])
def get_users():
    """Obtiene todos los usuarios de Supabase."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # Obtener todos los usuarios
        response = supabase.table("users").select("*").execute()
        
        return jsonify({
            "success": True,
            "count": len(response.data),
            "users": response.data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """Obtiene un usuario específico por su ID."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # Obtener usuario por ID
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not response.data:
            return jsonify({
                "success": False,
                "error": "Usuario no encontrado"
            }), 404
        
        return jsonify({
            "success": True,
            "user": response.data[0]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/users/wallet/<wallet_address>", methods=["GET"])
def get_user_by_wallet(wallet_address):
    """Obtiene un usuario por su dirección de wallet."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # Obtener usuario por wallet address
        response = supabase.table("users").select("*").eq("wallet_address", wallet_address).execute()
        
        if not response.data:
            return jsonify({
                "success": False,
                "error": "Usuario no encontrado"
            }), 404
        
        return jsonify({
            "success": True,
            "user": response.data[0]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/users/<user_id>/contacts", methods=["GET"])
def get_user_contacts(user_id):
    """Obtiene todos los contactos de un usuario específico."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # Obtener contactos del usuario
        response = supabase.table("contacts").select("*").eq("user_id", user_id).execute()
        
        return jsonify({
            "success": True,
            "count": len(response.data),
            "contacts": response.data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/users/wallet/<wallet_address>/contacts", methods=["GET"])
def get_user_contacts_by_wallet(wallet_address):
    """Obtiene todos los contactos de un usuario por su wallet address."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # 1. Buscar el usuario por wallet
        user_response = supabase.table("users").select("id, username").eq("wallet_address", wallet_address).execute()
        
        if not user_response.data:
            return jsonify({
                "success": False,
                "error": "Usuario no encontrado con esa wallet"
            }), 404
        
        user_id = user_response.data[0]["id"]
        username = user_response.data[0]["username"]
        
        # 2. Obtener contactos del usuario
        contacts_response = supabase.table("contacts").select("*").eq("user_id", user_id).execute()
        
        return jsonify({
            "success": True,
            "user": {
                "id": user_id,
                "username": username,
                "wallet_address": wallet_address
            },
            "count": len(contacts_response.data),
            "contacts": contacts_response.data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/users", methods=["POST"])
def create_user():
    """Crea un nuevo usuario."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        data = request.get_json()
        username = data.get("username")
        wallet_address = data.get("wallet_address")
        
        # Validaciones
        if not username or not wallet_address:
            return jsonify({
                "success": False,
                "error": "Se requieren username y wallet_address"
            }), 400
        
        if not Web3.is_address(wallet_address):
            return jsonify({
                "success": False,
                "error": "Dirección de wallet inválida. Debe ser una dirección Ethereum válida (0x...)"
            }), 400
        
        # Normalizar a checksum address
        wallet_address = Web3.to_checksum_address(wallet_address)
        
        # Crear usuario
        response = supabase.table("users").insert({
            "username": username,
            "wallet_address": wallet_address
        }).execute()
        
        return jsonify({
            "success": True,
            "message": "Usuario creado correctamente",
            "user": response.data[0]
        }), 201
        
    except Exception as e:
        error_message = str(e)
        if "duplicate key value" in error_message:
            return jsonify({
                "success": False,
                "error": "Esta wallet ya está registrada"
            }), 409
        return jsonify({
            "success": False,
            "error": error_message
        }), 500


@app.route("/contacts", methods=["POST"])
def create_contact():
    """Crea un nuevo contacto para un usuario."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        data = request.get_json()
        user_id = data.get("user_id")
        nombre = data.get("nombre")
        wallet_address = data.get("wallet_address")
        
        # Validaciones
        if not user_id or not nombre or not wallet_address:
            return jsonify({
                "success": False,
                "error": "Se requieren user_id, nombre y wallet_address"
            }), 400
        
        if not Web3.is_address(wallet_address):
            return jsonify({
                "success": False,
                "error": "Dirección de wallet inválida. Debe ser una dirección Ethereum válida (0x...)"
            }), 400
        
        # Normalizar a checksum address
        wallet_address = Web3.to_checksum_address(wallet_address)
        
        # Crear contacto
        response = supabase.table("contacts").insert({
            "user_id": user_id,
            "nombre": nombre,
            "wallet_address": wallet_address
        }).execute()
        
        return jsonify({
            "success": True,
            "message": "Contacto creado correctamente",
            "contact": response.data[0]
        }), 201
        
    except Exception as e:
        error_message = str(e)
        if "duplicate key value" in error_message:
            return jsonify({
                "success": False,
                "error": "Este contacto ya existe para el usuario"
            }), 409
        return jsonify({
            "success": False,
            "error": error_message
        }), 500


# ======================================
# 💸 ENDPOINTS DE TRANSACCIONES
# ======================================

@app.route("/transacciones", methods=["GET"])
def get_transacciones():
    """Obtiene todas las transacciones."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado"
            }), 500
        
        response = supabase.table("transacciones").select("*").order("fecha", desc=True).execute()
        
        return jsonify({
            "success": True,
            "count": len(response.data),
            "transacciones": response.data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/transacciones/<wallet>", methods=["GET"])
def get_transacciones_by_wallet(wallet):
    """Obtiene transacciones de una wallet específica (como emisor o receptor)."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado"
            }), 500
        
        # Buscar transacciones donde la wallet sea emisor o receptor
        response = supabase.table("transacciones").select("*").or_(
            f"wallet_emisor.eq.{wallet},wallet_receptor.eq.{wallet}"
        ).order("fecha", desc=True).execute()
        
        return jsonify({
            "success": True,
            "wallet": wallet,
            "count": len(response.data),
            "transacciones": response.data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/transacciones", methods=["POST"])
def create_transaccion():
    """Crea una nueva transacción."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado"
            }), 500
        
        data = request.get_json()
        wallet_emisor = data.get("wallet_emisor")
        wallet_receptor = data.get("wallet_receptor")
        monto = data.get("monto")
        estado = data.get("estado", "pendiente")  # Default: pendiente
        link_verificacion = data.get("link_verificacion", "")
        
        # Validaciones
        if not wallet_emisor or not wallet_receptor:
            return jsonify({
                "success": False,
                "error": "Se requieren wallet_emisor y wallet_receptor"
            }), 400
        
        if not monto or monto <= 0:
            return jsonify({
                "success": False,
                "error": "El monto debe ser mayor a 0"
            }), 400
        
        # Validar direcciones Ethereum
        if not Web3.is_address(wallet_emisor) or not Web3.is_address(wallet_receptor):
            return jsonify({
                "success": False,
                "error": "Las direcciones deben ser válidas (formato 0x...)"
            }), 400
        
        # Normalizar direcciones
        wallet_emisor = Web3.to_checksum_address(wallet_emisor)
        wallet_receptor = Web3.to_checksum_address(wallet_receptor)
        
        # Crear transacción
        from datetime import datetime
        response = supabase.table("transacciones").insert({
            "wallet_emisor": wallet_emisor,
            "wallet_receptor": wallet_receptor,
            "monto": float(monto),
            "estado": estado,
            "fecha": datetime.now().isoformat(),
            "link_verificacion": link_verificacion
        }).execute()
        
        return jsonify({
            "success": True,
            "message": "Transacción registrada correctamente",
            "transaccion": response.data[0]
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/transacciones/<transaccion_id>", methods=["PUT"])
def update_transaccion(transaccion_id):
    """Actualiza el estado de una transacción."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado"
            }), 500
        
        data = request.get_json()
        estado = data.get("estado")
        link_verificacion = data.get("link_verificacion")
        
        if not estado:
            return jsonify({
                "success": False,
                "error": "Se requiere el campo 'estado'"
            }), 400
        
        # Validar estado
        if estado not in ["pendiente", "progreso", "completado"]:
            return jsonify({
                "success": False,
                "error": "Estado inválido. Debe ser: pendiente, progreso o completado"
            }), 400
        
        # Actualizar transacción
        update_data = {"estado": estado}
        if link_verificacion:
            update_data["link_verificacion"] = link_verificacion
        
        response = supabase.table("transacciones").update(update_data).eq("id", transaccion_id).execute()
        
        if not response.data:
            return jsonify({
                "success": False,
                "error": "Transacción no encontrada"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Transacción actualizada correctamente",
            "transaccion": response.data[0]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================
# 🚀 Ejecutar servidor Flask
# ==========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

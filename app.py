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


# ======================================
# 📇 ENDPOINTS DE CONTACT_WALLETS
# ======================================

@app.route("/contact-wallets", methods=["POST"])
def add_contact_wallet():
    """Agrega un nuevo contacto a la tabla contact_wallets."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        data = request.get_json()
        nombre_wallet_agregada = data.get("nombre_wallet_agregada")
        wallet_agregada = data.get("wallet_agregada")
        wallet_quien_agrego = data.get("wallet_quien_agrego")
        
        # Validaciones
        if not nombre_wallet_agregada or not wallet_agregada or not wallet_quien_agrego:
            return jsonify({
                "success": False,
                "error": "Se requieren nombre_wallet_agregada, wallet_agregada y wallet_quien_agrego"
            }), 400
        
        if not Web3.is_address(wallet_agregada):
            return jsonify({
                "success": False,
                "error": "wallet_agregada inválida. Debe ser una dirección Ethereum válida (0x...)"
            }), 400
        
        if not Web3.is_address(wallet_quien_agrego):
            return jsonify({
                "success": False,
                "error": "wallet_quien_agrego inválida. Debe ser una dirección Ethereum válida (0x...)"
            }), 400
        
        # Normalizar a checksum address
        wallet_agregada = Web3.to_checksum_address(wallet_agregada)
        wallet_quien_agrego = Web3.to_checksum_address(wallet_quien_agrego)
        
        # Crear contacto en contact_wallets
        response = supabase.table("contact_wallets").insert({
            "nombre_wallet_agregada": nombre_wallet_agregada,
            "wallet_agregada": wallet_agregada,
            "wallet_quien_agrego": wallet_quien_agrego
        }).execute()
        
        return jsonify({
            "success": True,
            "message": "Contacto agregado correctamente",
            "contact": response.data[0]
        }), 201
        
    except Exception as e:
        error_message = str(e)
        if "duplicate key value" in error_message:
            return jsonify({
                "success": False,
                "error": "Este contacto ya existe"
            }), 409
        return jsonify({
            "success": False,
            "error": error_message
        }), 500


@app.route("/contact-wallets/<wallet_address>", methods=["GET"])
def get_contact_wallets(wallet_address):
    """Obtiene todos los contactos agregados por una wallet específica."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # Validar formato de wallet
        if not Web3.is_address(wallet_address):
            return jsonify({
                "success": False,
                "error": "Dirección de wallet inválida"
            }), 400
        
        # Normalizar a checksum address
        wallet_address = Web3.to_checksum_address(wallet_address)
        
        # Obtener contactos de la wallet
        response = supabase.table("contact_wallets").select("*").eq(
            "wallet_quien_agrego", wallet_address
        ).order("fecha_creacion", desc=True).execute()
        
        return jsonify({
            "success": True,
            "wallet": wallet_address,
            "count": len(response.data),
            "contacts": response.data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/contact-wallets", methods=["GET"])
def get_all_contact_wallets():
    """Obtiene todos los contactos de la tabla contact_wallets."""
    try:
        if not supabase:
            return jsonify({
                "error": "Supabase no está configurado. Verifica las variables SUPABASE_URL y SUPABASE_KEY"
            }), 500
        
        # Obtener todos los contactos
        response = supabase.table("contact_wallets").select("*").order(
            "fecha_creacion", desc=True
        ).execute()
        
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


# ======================================
# 💹 ENDPOINTS DE PYTH NETWORK - PRECIOS EN TIEMPO REAL
# ======================================

# Pyth Hermes API URL
PYTH_HERMES_URL = "https://hermes.pyth.network"

# Price Feed IDs más comunes (Pyth Network)
PRICE_FEEDS = {
    "eth": "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",  # ETH/USD
    "btc": "0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",  # BTC/USD
    "usdc": "0xeaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a",  # USDC/USD
    "usdt": "0x2b89b9dc8fdf9f34709a5b106b472f0f39bb6ca9ce04b0fd7f2e971688e2e53b",  # USDT/USD
    "bnb": "0x2f95862b045670cd22bee3114c39763a4a08beeb663b145d283c31d7d1101c4f",   # BNB/USD
    "sol": "0xef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",   # SOL/USD
    "matic": "0x5de33a9112c2b700b8d30b8a3402c103578ccfa2765696471cc672bd5cf6ac52", # MATIC/USD
    "avax": "0x93da3352f9f1d105fdfe4971cfa80e9dd777bfc5d0f683ebb6e1294b92137bb7",  # AVAX/USD
    "ada": "0x2a01deaec9e51a579277b34b122399984d0bbf57e2458a7e42fecd2829867a0d",   # ADA/USD
    "doge": "0xdcef50dd0a4cd2dcc17e45df1676dcb336a11a61c69df7a0299b0150c672d25c",  # DOGE/USD
}

@app.route("/pyth/price/<symbol>", methods=["GET"])
def get_pyth_price(symbol):
    """Obtiene el precio en tiempo real de Pyth Network usando Hermes API."""
    try:
        symbol_lower = symbol.lower()
        
        # Verificar si el símbolo existe
        if symbol_lower not in PRICE_FEEDS:
            return jsonify({
                "success": False,
                "error": f"Symbol '{symbol}' not supported. Available: {', '.join(PRICE_FEEDS.keys())}"
            }), 400
        
        price_feed_id = PRICE_FEEDS[symbol_lower]
        
        # Llamar a Hermes API
        hermes_url = f"{PYTH_HERMES_URL}/v2/updates/price/latest"
        params = {"ids[]": price_feed_id}
        
        response = requests.get(hermes_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("parsed"):
            return jsonify({
                "success": False,
                "error": "No price data available"
            }), 404
        
        # Parsear datos del precio
        price_feed = data["parsed"][0]
        price_data = price_feed["price"]
        
        # Calcular precio real
        price_raw = int(price_data["price"])
        expo = int(price_data["expo"])
        price = price_raw * (10 ** expo)
        
        # Calcular confianza
        conf_raw = int(price_data["conf"])
        confidence = conf_raw * (10 ** expo)
        
        return jsonify({
            "success": True,
            "symbol": symbol.upper(),
            "price": float(price),
            "confidence": float(confidence),
            "expo": expo,
            "publish_time": price_data["publish_time"],
            "price_feed_id": price_feed_id,
            "message": f"Current {symbol.upper()} price: ${price:.2f} USD"
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Error fetching price from Hermes API: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing price data: {str(e)}"
        }), 500


@app.route("/pyth/prices", methods=["GET"])
def get_multiple_prices():
    """Obtiene precios de múltiples criptomonedas usando Hermes API."""
    try:
        symbols = request.args.get("symbols", "eth,btc").split(",")
        max_symbols = 10
        
        if len(symbols) > max_symbols:
            return jsonify({
                "success": False,
                "error": f"Maximum {max_symbols} symbols allowed"
            }), 400
        
        # Construir lista de IDs para Hermes
        price_ids = []
        symbol_map = {}
        
        for symbol in symbols:
            symbol = symbol.strip().lower()
            if symbol in PRICE_FEEDS:
                price_ids.append(PRICE_FEEDS[symbol])
                symbol_map[PRICE_FEEDS[symbol]] = symbol
        
        if not price_ids:
            return jsonify({
                "success": False,
                "error": "No valid symbols provided"
            }), 400
        
        # Llamar a Hermes API con múltiples IDs
        hermes_url = f"{PYTH_HERMES_URL}/v2/updates/price/latest"
        params = [("ids[]", price_id) for price_id in price_ids]
        
        response = requests.get(hermes_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        results = []
        errors = []
        
        if data.get("parsed"):
            for price_feed in data["parsed"]:
                try:
                    price_data = price_feed["price"]
                    feed_id = price_feed["id"]
                    
                    # Calcular precio real
                    price_raw = int(price_data["price"])
                    expo = int(price_data["expo"])
                    price = price_raw * (10 ** expo)
                    
                    symbol = symbol_map.get(feed_id, "UNKNOWN")
                    
                    results.append({
                        "symbol": symbol.upper(),
                        "price": float(price),
                        "price_usd": f"${price:.2f}"
                    })
                except Exception as e:
                    errors.append({
                        "symbol": symbol_map.get(feed_id, "UNKNOWN").upper(),
                        "error": str(e)
                    })
        
        return jsonify({
            "success": True,
            "count": len(results),
            "prices": results,
            "errors": errors if errors else None
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Error fetching prices from Hermes API: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/pyth/chat", methods=["POST"])
def pyth_chat_ai():
    """Chat con IA para consultar precios usando Pyth Network (en inglés)."""
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
        
        if not DEEPSEEK_API_KEY:
            return jsonify({
                "success": False,
                "error": "AI API key not configured"
            }), 500
        
        # Obtener precios actuales para contexto
        available_symbols = list(PRICE_FEEDS.keys())
        
        # Prompt mejorado para la IA (en inglés con consejos de transferencia)
        system_prompt = f"""You are an expert cryptocurrency advisor and price assistant. You help users get real-time cryptocurrency prices using Pyth Network and provide smart advice for making transfers and transactions.

Available cryptocurrencies: {', '.join([s.upper() for s in available_symbols])}

Your capabilities:
1. Get real-time cryptocurrency prices
2. Provide advice on the best time to transfer based on current prices
3. Give recommendations on transaction strategies
4. Help users understand market conditions
5. Calculate portfolio value with multiple cryptocurrencies

Response formats:

**For price queries:**
{{"action": "get_price", "symbol": "eth", "message": "Getting ETH price..."}}

**For multiple prices:**
{{"action": "get_multiple_prices", "symbols": ["eth", "btc"], "message": "Getting prices..."}}

**For transfer advice:**
{{"action": "transfer_advice", "symbol": "eth", "amount": 0.5, "message": "Analyzing transfer conditions..."}}

**For portfolio calculation:**
{{"action": "calculate_portfolio", "holdings": {{"eth": 2, "btc": 0.5, "sol": 10}}, "message": "Calculating your portfolio value..."}}

**For general advice:**
{{"action": "advice", "message": "Your personalized advice here..."}}

Examples:
- User: "What's the price of ETH?"
  Response: {{"action": "get_price", "symbol": "eth", "message": "Fetching current ETH price..."}}

- User: "Should I transfer 0.5 ETH now?"
  Response: {{"action": "transfer_advice", "symbol": "eth", "amount": 0.5, "message": "Let me check the current ETH price to advise you..."}}

- User: "Calculate my portfolio: 2 ETH, 0.5 BTC, 10 SOL"
  Response: {{"action": "calculate_portfolio", "holdings": {{"eth": 2, "btc": 0.5, "sol": 10}}, "message": "Calculating your portfolio value..."}}

- User: "How much is my crypto worth: 1.5 ETH and 100 USDC"
  Response: {{"action": "calculate_portfolio", "holdings": {{"eth": 1.5, "usdc": 100}}, "message": "Getting current prices to calculate your portfolio..."}}

- User: "Show me ETH and BTC prices for a transfer"
  Response: {{"action": "get_multiple_prices", "symbols": ["eth", "btc"], "message": "Getting prices for your transfer decision..."}}

Always respond in English and with valid JSON only."""

        # Llamar a DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        ai_response = response.json()
        ai_message = ai_response["choices"][0]["message"]["content"].strip()
        
        # Parsear respuesta JSON de la IA
        try:
            ai_json = json.loads(ai_message)
        except:
            ai_json = {"action": "none", "message": ai_message}
        
        # Procesar acciones
        action = ai_json.get("action", "none")
        
        if action == "get_price":
            symbol = ai_json.get("symbol", "").lower()
            if symbol in PRICE_FEEDS:
                try:
                    price_feed_id = PRICE_FEEDS[symbol]
                    
                    # Llamar a Hermes API
                    hermes_url = f"{PYTH_HERMES_URL}/v2/updates/price/latest"
                    params = {"ids[]": price_feed_id}
                    
                    price_response = requests.get(hermes_url, params=params, timeout=10)
                    price_response.raise_for_status()
                    
                    price_json = price_response.json()
                    
                    if price_json.get("parsed"):
                        price_feed = price_json["parsed"][0]
                        price_data = price_feed["price"]
                        
                        price_raw = int(price_data["price"])
                        expo = int(price_data["expo"])
                        price = price_raw * (10 ** expo)
                        
                        # Calcular confianza
                        conf_raw = int(price_data["conf"])
                        confidence = conf_raw * (10 ** expo)
                        confidence_pct = (confidence / price * 100) if price > 0 else 0
                        
                        # Determinar volatilidad
                        if confidence_pct < 0.1:
                            volatility = "Very Low"
                        elif confidence_pct < 0.5:
                            volatility = "Low"
                        elif confidence_pct < 1.0:
                            volatility = "Moderate"
                        elif confidence_pct < 2.0:
                            volatility = "High"
                        else:
                            volatility = "Very High"
                        
                        # Timestamp legible
                        from datetime import datetime
                        publish_timestamp = datetime.fromtimestamp(price_data["publish_time"]).strftime("%Y-%m-%d %H:%M:%S UTC")
                        
                        ai_json["price_data"] = {
                            "symbol": symbol.upper(),
                            "price": float(price),
                            "price_usd": f"${price:.2f}",
                            "confidence": float(confidence),
                            "confidence_usd": f"±${confidence:.4f}",
                            "confidence_percentage": f"{confidence_pct:.3f}%",
                            "volatility": volatility,
                            "publish_time": price_data["publish_time"],
                            "publish_timestamp": publish_timestamp,
                            "expo": expo,
                            "price_feed_id": price_feed["id"],
                            "source": "Pyth Network (Hermes API)"
                        }
                        ai_json["message"] = f"The current price of {symbol.upper()} is ${price:.2f} USD (±${confidence:.4f}, {volatility} volatility)"
                except Exception as e:
                    ai_json["error"] = f"Error fetching price: {str(e)}"
        
        elif action == "get_multiple_prices":
            symbols = ai_json.get("symbols", [])
            prices_result = []
            
            # Construir lista de IDs
            price_ids = [PRICE_FEEDS[s.lower()] for s in symbols if s.lower() in PRICE_FEEDS]
            
            if price_ids:
                try:
                    hermes_url = f"{PYTH_HERMES_URL}/v2/updates/price/latest"
                    params = [("ids[]", price_id) for price_id in price_ids]
                    
                    price_response = requests.get(hermes_url, params=params, timeout=10)
                    price_response.raise_for_status()
                    
                    price_json = price_response.json()
                    
                    if price_json.get("parsed"):
                        for price_feed in price_json["parsed"]:
                            price_data = price_feed["price"]
                            feed_id = price_feed["id"]
                            
                            price_raw = int(price_data["price"])
                            expo = int(price_data["expo"])
                            price = price_raw * (10 ** expo)
                            
                            # Calcular confianza
                            conf_raw = int(price_data["conf"])
                            confidence = conf_raw * (10 ** expo)
                            confidence_pct = (confidence / price * 100) if price > 0 else 0
                            
                            # Volatilidad
                            if confidence_pct < 0.5:
                                volatility = "Low"
                            elif confidence_pct < 1.0:
                                volatility = "Moderate"
                            else:
                                volatility = "High"
                            
                            # Encontrar símbolo por feed_id
                            symbol = next((k for k, v in PRICE_FEEDS.items() if v == feed_id), "UNKNOWN")
                            
                            prices_result.append({
                                "symbol": symbol.upper(),
                                "price": float(price),
                                "price_usd": f"${price:.2f}",
                                "confidence": float(confidence),
                                "confidence_usd": f"±${confidence:.4f}",
                                "volatility": volatility,
                                "publish_time": price_data["publish_time"]
                            })
                except Exception as e:
                    ai_json["error"] = f"Error fetching prices: {str(e)}"
            
            ai_json["prices"] = prices_result
            if prices_result:
                price_list = ", ".join([f"{p['symbol']}: {p['price_usd']}" for p in prices_result])
                ai_json["message"] = f"Current prices - {price_list}"
        
        elif action == "transfer_advice":
            symbol = ai_json.get("symbol", "").lower()
            amount = ai_json.get("amount", 0)
            
            if symbol in PRICE_FEEDS:
                try:
                    price_feed_id = PRICE_FEEDS[symbol]
                    
                    # Obtener precio actual
                    hermes_url = f"{PYTH_HERMES_URL}/v2/updates/price/latest"
                    params = {"ids[]": price_feed_id}
                    
                    price_response = requests.get(hermes_url, params=params, timeout=10)
                    price_response.raise_for_status()
                    
                    price_json = price_response.json()
                    
                    if price_json.get("parsed"):
                        price_feed = price_json["parsed"][0]
                        price_data = price_feed["price"]
                        
                        price_raw = int(price_data["price"])
                        expo = int(price_data["expo"])
                        price = price_raw * (10 ** expo)
                        conf_raw = int(price_data["conf"])
                        confidence = conf_raw * (10 ** expo)
                        
                        # Calcular valor de la transferencia
                        transfer_value_usd = price * amount if amount > 0 else 0
                        
                        # Generar consejo con IA
                        advice_prompt = f"""Based on the current {symbol.upper()} price of ${price:.2f} USD with a confidence interval of ±${confidence:.2f}, provide brief advice (2-3 sentences) about:
1. Whether it's a good time to transfer {amount if amount > 0 else 'some'} {symbol.upper()}
2. Any considerations about transaction fees (gas fees on Scroll Sepolia are typically low, ~$0.01-0.10)
3. Market volatility considerations

Keep advice practical and concise."""

                        advice_payload = {
                            "model": "deepseek-chat",
                            "messages": [
                                {"role": "system", "content": "You are a cryptocurrency advisor. Provide brief, practical advice."},
                                {"role": "user", "content": advice_prompt}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 200
                        }
                        
                        advice_response = requests.post(DEEPSEEK_URL, headers=headers, json=advice_payload, timeout=30)
                        advice_response.raise_for_status()
                        advice_result = advice_response.json()
                        advice_text = advice_result["choices"][0]["message"]["content"].strip()
                        
                        ai_json["price_data"] = {
                            "symbol": symbol.upper(),
                            "price": float(price),
                            "price_usd": f"${price:.2f}",
                            "confidence": float(confidence),
                            "confidence_usd": f"±${confidence:.2f}",
                            "source": "Pyth Network (Hermes API)"
                        }
                        
                        ai_json["transfer_info"] = {
                            "amount": amount,
                            "estimated_value_usd": f"${transfer_value_usd:.2f}" if amount > 0 else "N/A",
                            "estimated_gas_fee": "$0.01 - $0.10 (Scroll Sepolia)",
                            "network": "Scroll Sepolia Testnet"
                        }
                        
                        ai_json["advice"] = advice_text
                        ai_json["message"] = f"Current {symbol.upper()} price: ${price:.2f} USD. Analysis complete."
                        
                except Exception as e:
                    ai_json["error"] = f"Error generating transfer advice: {str(e)}"
        
        elif action == "calculate_portfolio":
            holdings = ai_json.get("holdings", {})
            
            if not holdings:
                ai_json["error"] = "No holdings provided for portfolio calculation"
            else:
                try:
                    # Obtener símbolos válidos
                    valid_holdings = {k.lower(): v for k, v in holdings.items() if k.lower() in PRICE_FEEDS}
                    
                    if not valid_holdings:
                        ai_json["error"] = "No valid cryptocurrencies found in portfolio"
                    else:
                        # Construir lista de IDs para Hermes
                        price_ids = [PRICE_FEEDS[symbol] for symbol in valid_holdings.keys()]
                        
                        # Obtener precios de todas las criptos del portfolio
                        hermes_url = f"{PYTH_HERMES_URL}/v2/updates/price/latest"
                        params = [("ids[]", price_id) for price_id in price_ids]
                        
                        price_response = requests.get(hermes_url, params=params, timeout=10)
                        price_response.raise_for_status()
                        
                        price_json = price_response.json()
                        
                        if price_json.get("parsed") and len(price_json["parsed"]) > 0:
                            portfolio_items = []
                            total_value_usd = 0
                            
                            for price_feed in price_json["parsed"]:
                                price_data = price_feed["price"]
                                feed_id = price_feed["id"]
                                
                                # Calcular precio
                                price_raw = int(price_data["price"])
                                expo = int(price_data["expo"])
                                price = price_raw * (10 ** expo)
                                
                                # Encontrar símbolo y cantidad
                                symbol = next((k for k, v in PRICE_FEEDS.items() if v == feed_id), None)
                                if symbol and symbol in valid_holdings:
                                    amount = valid_holdings[symbol]
                                    value_usd = price * amount
                                    total_value_usd += value_usd
                                    
                                    portfolio_items.append({
                                        "symbol": symbol.upper(),
                                        "amount": amount,
                                        "price": float(price),
                                        "price_usd": f"${price:.2f}",
                                        "value_usd": float(value_usd),
                                        "value_formatted": f"${value_usd:,.2f}"
                                    })
                            
                            if len(portfolio_items) == 0:
                                ai_json["error"] = "No price data available for the cryptocurrencies in your portfolio"
                            else:
                                # Calcular porcentajes
                                for item in portfolio_items:
                                    item["percentage"] = (item["value_usd"] / total_value_usd * 100) if total_value_usd > 0 else 0
                                    item["percentage_formatted"] = f"{item['percentage']:.2f}%"
                                
                                # Ordenar por valor descendente
                                portfolio_items.sort(key=lambda x: x["value_usd"], reverse=True)
                                
                                # Generar resumen con IA solo si hay items
                                summary_text = ""
                                if len(portfolio_items) > 0:
                                    try:
                                        summary_prompt = f"""Based on this crypto portfolio analysis:
- Total Value: ${total_value_usd:,.2f}
- Holdings: {len(portfolio_items)} different cryptocurrencies
- Top holding: {portfolio_items[0]['symbol']} ({portfolio_items[0]['percentage_formatted']})

Provide a brief summary (2-3 sentences) about:
1. Portfolio diversification quality
2. Risk level based on distribution
3. Any quick recommendation"""

                                        summary_payload = {
                                            "model": "deepseek-chat",
                                            "messages": [
                                                {"role": "system", "content": "You are a crypto portfolio advisor. Provide brief, actionable insights."},
                                                {"role": "user", "content": summary_prompt}
                                            ],
                                            "temperature": 0.7,
                                            "max_tokens": 150
                                        }
                                        
                                        summary_response = requests.post(DEEPSEEK_URL, headers=headers, json=summary_payload, timeout=30)
                                        summary_response.raise_for_status()
                                        summary_result = summary_response.json()
                                        summary_text = summary_result["choices"][0]["message"]["content"].strip()
                                    except:
                                        summary_text = "Portfolio calculated successfully. Review your holdings distribution above."
                                
                                ai_json["portfolio"] = {
                                    "total_value_usd": float(total_value_usd),
                                    "total_value_formatted": f"${total_value_usd:,.2f}",
                                    "holdings_count": len(portfolio_items),
                                    "items": portfolio_items
                                }
                                
                                ai_json["summary"] = summary_text
                                ai_json["message"] = f"Portfolio calculated: {len(portfolio_items)} assets worth ${total_value_usd:,.2f} USD"
                        else:
                            ai_json["error"] = "No price data received from Pyth Network"
                            
                except Exception as e:
                    ai_json["error"] = f"Error calculating portfolio: {str(e)}"
        
        elif action == "advice":
            # Consejo general sin precio específico
            ai_json["message"] = ai_json.get("message", "Please specify which cryptocurrency you want advice about.")
        
        return jsonify(ai_json)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/pyth/supported", methods=["GET"])
def get_supported_symbols():
    """Obtiene la lista de criptomonedas soportadas."""
    return jsonify({
        "success": True,
        "count": len(PRICE_FEEDS),
        "symbols": list(PRICE_FEEDS.keys()),
        "message": f"Supported cryptocurrencies: {', '.join([s.upper() for s in PRICE_FEEDS.keys()])}"
    })


# ==========================
# 🚀 Ejecutar servidor Flask
# ==========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

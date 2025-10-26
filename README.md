# 🚀 Clarity Backend - API para Contratos Inteligentes en Stacks

Backend Flask que proporciona una API REST para interactuar con contratos inteligentes en la blockchain de Stacks, integrado con inteligencia artificial de DeepSeek para interpretar comandos en lenguaje natural.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## ✨ Características

- 🔗 **Integración con Stacks Blockchain**: Lee y ejecuta funciones de contratos inteligentes en Clarity
- 💸 **Transferencias de STX**: Sistema completo para transferir STX entre wallets
- 🤖 **IA con DeepSeek**: Interpreta comandos en lenguaje natural y los convierte en acciones sobre el contrato
- 🌐 **API REST**: Endpoints simples y bien documentados
- 🔒 **CORS habilitado**: Listo para integrarse con frontends web
- 📊 **Parseo inteligente**: Convierte respuestas de Clarity a formatos legibles
- 💰 **Consulta de balances**: Verifica el balance de cualquier wallet en Stacks
- ✅ **Verificación de transacciones**: Monitorea el estado de transacciones en tiempo real
- 🛠️ **Fácil configuración**: Variables de entorno mediante archivo `.env`

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una cuenta en [DeepSeek](https://platform.deepseek.com/) para obtener tu API Key
- Un contrato inteligente desplegado en Stacks (testnet o mainnet)

## 📦 Instalación

1. **Clona el repositorio**

```bash
git clone https://github.com/JHAMILCALI/clarity-backend.git
cd clarity-backend
```

2. **Crea un entorno virtual (recomendado)**

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. **Crea un archivo `.env` en la raíz del proyecto** con las siguientes variables:

```env
# Configuración del Contrato de Stacks
CONTRACT_ADDRESS=tu_direccion_del_contrato
CONTRACT_NAME=nombre_del_contrato
STACKS_NETWORK=testnet  # o mainnet

# API Key de DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

2. **Ejemplo de configuración**:

```env
CONTRACT_ADDRESS=ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM
CONTRACT_NAME=counter-contract
STACKS_NETWORK=testnet
DEEPSEEK_API_KEY=sk-f984577379764c759173c5762d9c25ec
```

## 🚀 Uso

1. **Inicia el servidor**

```bash
python app.py
```

El servidor estará disponible en `http://127.0.0.1:5000`

2. **Verifica que el servidor está funcionando**

```bash
curl http://127.0.0.1:5000/
```

Respuesta esperada:
```json
{
  "status": "ok",
  "message": "✅ Backend Flask funcionando correctamente"
}
```

## 📡 Endpoints de la API

### 1. **GET /** - Health Check

Verifica que el servidor está funcionando.

**Request:**
```bash
GET http://127.0.0.1:5000/
```

**Response:**
```json
{
  "status": "ok",
  "message": "✅ Backend Flask funcionando correctamente"
}
```

---

### 2. **GET /get-count** - Leer Contador

Lee el valor actual del contador desde el contrato inteligente en Stacks.

**Request:**
```bash
GET http://127.0.0.1:5000/get-count
```

**Response:**
```json
{
  "count": 7,
  "raw_debug": "0x0703..."
}
```

**Descripción:**
- Realiza una llamada de solo lectura al contrato de Stacks
- Parsea la respuesta de Clarity (formato `u7`, `ok u7`, etc.)
- Devuelve el valor como un número entero natural

---

### 3. **POST /chat** - Chat con IA

Envía un mensaje en lenguaje natural a la IA de DeepSeek para interpretar comandos sobre el contrato.

**Request:**
```bash
POST http://127.0.0.1:5000/chat
Content-Type: application/json

{
  "message": "Transfiere 50 STX a ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
}
```

**Response:**
```json
{
  "action": "transfer",
  "recipient": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "amount": 50,
  "message": "Transferir 50 STX a la wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
}
```

**Acciones posibles:**
- `"transfer"`: Transferir STX a otra wallet
- `"balance"`: Consultar balance de una wallet
- `"increment"`: Incrementar el contador
- `"read"`: Leer el valor actual
- `"none"`: Ninguna acción específica

**Ejemplos de mensajes:**

| Mensaje del usuario | Acción detectada | Datos extraídos |
|---------------------|------------------|-----------------|
| "Transfiere 50 STX a ST2..." | `transfer` | amount: 50, recipient: ST2... |
| "¿Cuál es el balance de ST1...?" | `balance` | address: ST1... |
| "incrementa el contador" | `increment` | - |
| "cuánto vale el contador" | `read` | - |

---

### 4. **POST /get-balance** - Consultar Balance

Consulta el balance de STX de una dirección específica.

**Request:**
```bash
POST http://127.0.0.1:5000/get-balance
Content-Type: application/json

{
  "address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
}
```

**Response:**
```json
{
  "address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "balance": 125.5,
  "balance_microstx": 125500000,
  "message": "Balance: 125.5 STX"
}
```

---

### 5. **POST /prepare-transfer** - Preparar Transferencia

Prepara los datos necesarios para ejecutar una transferencia de STX desde el frontend.

**Request:**
```bash
POST http://127.0.0.1:5000/prepare-transfer
Content-Type: application/json

{
  "sender": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "recipient": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "amount": 50
}
```

**Response:**
```json
{
  "contract_address": "ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R",
  "contract_name": "traspaso-v2",
  "function_name": "transfer-stx",
  "function_args": ["'ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6", "u50000000"],
  "sender": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "recipient": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "amount": 50,
  "amount_microstx": 50000000,
  "network": "testnet",
  "message": "¿Deseas aprobar la transferencia de 50 STX a ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6?"
}
```

---

### 6. **POST /check-transaction** - Verificar Transacción

Verifica el estado de una transacción en la blockchain de Stacks.

**Request:**
```bash
POST http://127.0.0.1:5000/check-transaction
Content-Type: application/json

{
  "txid": "0x123456789abcdef..."
}
```

**Response:**
```json
{
  "txid": "0x123456789abcdef...",
  "status": "success",
  "block_height": 12345,
  "block_hash": "0xabc...",
  "explorer_url": "https://explorer.hiro.so/txid/0x123456789abcdef...?chain=testnet",
  "message": "✅ Transacción completada correctamente"
}
```

---

## 📁 Estructura del Proyecto

```
clarity-backend/
│
├── app.py                     # Aplicación principal de Flask
├── requirements.txt           # Dependencias de Python
├── .env                       # Variables de entorno (NO subir a Git)
├── .gitignore                # Archivos a ignorar en Git
├── README.md                 # Documentación principal
└── INTEGRATION_GUIDE.md      # Guía de integración con frontend
```

---

## 🛠️ Tecnologías

Este proyecto utiliza las siguientes tecnologías:

| Tecnología | Versión | Descripción |
|-----------|---------|-------------|
| **Python** | 3.8+ | Lenguaje de programación principal |
| **Flask** | 3.0.0 | Framework web minimalista |
| **Flask-CORS** | 4.0.0 | Manejo de CORS para peticiones cross-origin |
| **python-dotenv** | 1.0.0 | Carga de variables de entorno |
| **requests** | 2.31.0 | Cliente HTTP para peticiones a APIs externas |
| **DeepSeek API** | - | IA para procesamiento de lenguaje natural |
| **Stacks Blockchain** | - | Blockchain para contratos inteligentes en Clarity |

---

## 🔍 Detalles Técnicos

### Contrato de Transferencias STX

El backend interactúa con el contrato desplegado en:
- **Dirección**: `ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R.traspaso-v2`
- **Red**: Testnet/Mainnet (configurable)

**Funciones del contrato:**
- `transfer-stx(recipient, amount)`: Transferir STX entre wallets
- `get-balance(address)`: Consultar balance de una dirección

### Parseo de Respuestas de Clarity

El contrato inteligente en Stacks devuelve valores en formato Clarity:

- `u7` → unsigned integer 7
- `ok u7` → resultado exitoso con valor 7
- `0x0703...` → valor hexadecimal codificado

El backend realiza el parseo automático de estos formatos para devolver números enteros naturales.

### Conversión STX ↔ microSTX

- **1 STX** = 1,000,000 microSTX
- El contrato trabaja con microSTX internamente
- El backend convierte automáticamente entre ambos formatos

### Integración con DeepSeek

La IA de DeepSeek se configura con un prompt de sistema específico que le permite:

1. Interpretar comandos en lenguaje natural
2. Extraer parámetros (montos, direcciones)
3. Identificar la acción a realizar (transfer, balance, etc.)
4. Devolver respuestas estructuradas en JSON

Esto garantiza respuestas estructuradas y predecibles.

---

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'flask'`

**Solución:** Instala las dependencias
```bash
pip install -r requirements.txt
```

### Error: `KeyError: 'CONTRACT_ADDRESS'`

**Solución:** Asegúrate de tener el archivo `.env` configurado correctamente con todas las variables necesarias.

### Error SSL con DeepSeek API

**Solución:** Verifica que tu `DEEPSEEK_API_KEY` sea válida y esté correctamente configurada en el `.env`.

### El contador devuelve un número gigante

**Solución:** El código ya incluye parseo automático. Si persiste el problema, verifica la consola para ver los logs de debug.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si deseas contribuir:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 👤 Autor

**JHAMILCALI**

- GitHub: [@JHAMILCALI](https://github.com/JHAMILCALI)
- Repositorio: [clarity-backend](https://github.com/JHAMILCALI/clarity-backend)

---

## 🌟 Agradecimientos

- [Stacks](https://www.stacks.co/) - Blockchain para contratos inteligentes
- [DeepSeek](https://www.deepseek.com/) - IA para procesamiento de lenguaje natural
- [Flask](https://flask.palletsprojects.com/) - Framework web para Python

---

## 📞 Soporte

Si tienes problemas o preguntas, por favor:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Abre un [Issue](https://github.com/JHAMILCALI/clarity-backend/issues) en GitHub
3. Consulta la [documentación de Stacks](https://docs.stacks.co/)

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ por JHAMILCALI

</div>

# 💸 Guía de Integración - Transferencias STX

## 🎯 Endpoints Disponibles

### 1. **POST /chat** - Interpretar comandos con IA

Interpreta comandos en lenguaje natural y extrae información de transferencias.

**Request:**
```json
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

---

### 2. **POST /get-balance** - Consultar balance

Consulta el balance de STX de una dirección.

**Request:**
```json
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

### 3. **POST /prepare-transfer** - Preparar transferencia

Prepara los datos necesarios para ejecutar una transferencia desde el frontend.

**Request:**
```json
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
  "function_args": [
    "'ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "u50000000"
  ],
  "sender": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "recipient": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "amount": 50,
  "amount_microstx": 50000000,
  "network": "testnet",
  "post_condition_mode": "allow",
  "message": "¿Deseas aprobar la transferencia de 50 STX a ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6?"
}
```

---

### 4. **POST /check-transaction** - Verificar transacción

Verifica el estado de una transacción en la blockchain.

**Request:**
```json
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

## 🔄 Flujo Completo de Transferencia

### Paso 1: Usuario envía comando
```javascript
const response = await fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Transfiere 50 STX a ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
  })
});

const data = await response.json();
// data = { action: "transfer", recipient: "ST2...", amount: 50, ... }
```

### Paso 2: Preparar la transacción
```javascript
if (data.action === "transfer") {
  const prepareResponse = await fetch('http://localhost:5000/prepare-transfer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sender: userAddress,  // Dirección del usuario conectado
      recipient: data.recipient,
      amount: data.amount
    })
  });
  
  const txData = await prepareResponse.json();
  // txData contiene todos los datos para ejecutar la transacción
}
```

### Paso 3: Ejecutar con @stacks/connect (Frontend)
```javascript
import { openContractCall } from '@stacks/connect';

const txOptions = {
  network: txData.network === 'mainnet' ? new StacksMainnet() : new StacksTestnet(),
  contractAddress: txData.contract_address,
  contractName: txData.contract_name,
  functionName: txData.function_name,
  functionArgs: [
    principalCV(txData.recipient),
    uintCV(txData.amount_microstx)
  ],
  postConditionMode: PostConditionMode.Allow,
  onFinish: (data) => {
    console.log('Transaction ID:', data.txId);
    // Verificar estado de la transacción
    checkTransactionStatus(data.txId);
  },
  onCancel: () => {
    console.log('Usuario canceló la transacción');
  }
};

await openContractCall(txOptions);
```

### Paso 4: Verificar estado de la transacción
```javascript
async function checkTransactionStatus(txid) {
  const statusResponse = await fetch('http://localhost:5000/check-transaction', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ txid })
  });
  
  const status = await statusResponse.json();
  console.log(status.message);
  console.log('Ver en explorer:', status.explorer_url);
}
```

---

## 🛡️ Validaciones Implementadas

El backend incluye las siguientes validaciones:

✅ **Direcciones válidas**: Deben comenzar con `ST` o `SP`  
✅ **Monto mayor a 0**: No se permiten transferencias de 0 o valores negativos  
✅ **Conversión automática**: De STX a microSTX (1 STX = 1,000,000 microSTX)  
✅ **Manejo de errores**: Respuestas claras en caso de error

---

## 📝 Ejemplos de Comandos Naturales

El endpoint `/chat` puede interpretar:

| Comando del usuario | Acción detectada | Parámetros extraídos |
|---------------------|------------------|----------------------|
| "Transfiere 50 STX a ST2..." | `transfer` | amount: 50, recipient: ST2... |
| "Envía 100 STX a la wallet SP3..." | `transfer` | amount: 100, recipient: SP3... |
| "¿Cuál es mi balance?" | `balance` | - |
| "Saldo de ST1..." | `balance` | address: ST1... |

---

## 🚀 Variables de Entorno Necesarias

Asegúrate de tener en tu archivo `.env`:

```env
# Contrato de transferencias (Ya configurado en el código)
# No es necesario agregarlo al .env

# Red de Stacks
STACKS_NETWORK=testnet  # o mainnet

# API de DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

---

## 🔗 URLs Útiles

- **Testnet Explorer**: https://explorer.hiro.so/?chain=testnet
- **Mainnet Explorer**: https://explorer.hiro.so/?chain=mainnet
- **API Testnet**: https://api.testnet.hiro.so
- **API Mainnet**: https://api.hiro.so

---

## ⚠️ Notas Importantes

1. **Wallet del Usuario**: El frontend debe conectarse a la wallet del usuario (Xverse, Hiro, Leather) usando `@stacks/connect`.

2. **Firma de Transacciones**: Las transacciones se firman en el frontend con la wallet del usuario, NO en el backend.

3. **Post Conditions**: Se recomienda agregar post-conditions para mayor seguridad.

4. **Confirmaciones**: Las transacciones en Stacks pueden tardar varios minutos en confirmarse.

5. **Fees**: Las transacciones tienen un costo en STX (fee) que se descuenta automáticamente.

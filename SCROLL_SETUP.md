# 🚀 Backend para Scroll Sepolia con RainbowKit

Backend Flask adaptado para trabajar con el contrato **STXTransfer** deployado en **Scroll Sepolia**.

## 📋 Características

- ✅ Integración con **Scroll Sepolia** (EVM-compatible)
- ✅ Soporte para **RainbowKit** en el frontend
- ✅ API de chat con **DeepSeek AI** para comandos en lenguaje natural
- ✅ Base de datos **Supabase** para usuarios y contactos
- ✅ Endpoints para transferencias, balance y transacciones
- ✅ Validación de direcciones Ethereum

## 🔧 Configuración

### 1. Instalar dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# o
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia `.env.example` a `.env` y completa:

```env
# Scroll Sepolia
CONTRACT_ADDRESS=0xD8c566986a9dD489369129b5156fEbF09b3751FD
SCROLL_RPC_URL=https://sepolia-rpc.scroll.io
NETWORK=scroll-sepolia
CHAIN_ID=534351

# DeepSeek AI
DEEPSEEK_API_KEY=sk-tu-api-key-aqui

# Supabase (opcional)
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-supabase-anon-key
```

### 3. Ejecutar el servidor

```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

## 📡 Endpoints disponibles

### Información de la red
```
GET /network-info
```

### Balance de wallet
```
POST /get-balance
Body: { "address": "0x..." }
```

### Preparar transferencia
```
POST /prepare-transfer
Body: {
  "sender": "0x...",
  "recipient": "0x...",
  "amount": 0.1
}
```

### Verificar transacción
```
POST /check-transaction
Body: { "txid": "0x..." }
```

### Chat con IA
```
POST /chat
Body: {
  "message": "Transfiere 0.5 ETH a 0x...",
  "sender_wallet": "0x..."
}
```

### Gestión de usuarios y contactos
```
GET /users
POST /users
GET /users/wallet/{address}/contacts
POST /contacts
```

## 🎯 Contrato en Scroll Sepolia

**Dirección**: `0xD8c566986a9dD489369129b5156fEbF09b3751FD`
**Explorer**: https://sepolia.scrollscan.com/address/0xD8c566986a9dD489369129b5156fEbF09b3751FD

### Funciones principales

- `transferSTX(address recipient)` - Transferir ETH (con msg.value)
- `transferSTXWithAmount(address recipient, uint256 amount)` - Transferir cantidad específica
- `getBalance(address account)` - Consultar balance
- `getContractBalance()` - Balance del contrato

## 🌐 Integración con RainbowKit

En tu frontend con RainbowKit:

```typescript
import { useWalletClient } from 'wagmi';
import { parseEther } from 'viem';

// 1. Obtener datos de transferencia del backend
const response = await fetch('http://localhost:5000/prepare-transfer', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sender: address,
    recipient: '0x...',
    amount: 0.1
  })
});
const data = await response.json();

// 2. Ejecutar transacción con RainbowKit
const { data: walletClient } = useWalletClient();
const hash = await walletClient?.writeContract({
  address: '0xD8c566986a9dD489369129b5156fEbF09b3751FD',
  abi: contractAbi,
  functionName: 'transferSTX',
  args: [data.recipient],
  value: parseEther(data.amount.toString()),
  chain: scrollSepolia,
});

// 3. Verificar transacción
const checkResponse = await fetch('http://localhost:5000/check-transaction', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ txid: hash })
});
```

## 🔗 Configuración de Scroll Sepolia en RainbowKit

```typescript
import { scrollSepolia } from 'wagmi/chains';

const config = getDefaultConfig({
  appName: 'Tu App',
  projectId: 'TU_WALLETCONNECT_PROJECT_ID',
  chains: [scrollSepolia],
  ssr: true,
});
```

## 📚 Recursos

- [RainbowKit Docs](https://rainbowkit.com/docs/connect-button)
- [Scroll Sepolia Explorer](https://sepolia.scrollscan.com/)
- [Scroll Docs](https://docs.scroll.io/)
- [Web3.py Docs](https://web3py.readthedocs.io/)

## 🛠️ Desarrollo

### Estructura del proyecto

```
Backend-AI/
├── app.py                 # Backend Flask principal
├── requirements.txt       # Dependencias Python
├── .env.example          # Template de variables de entorno
├── SCROLL_SETUP.md       # Esta guía
└── README.md            # Documentación general
```

### Comandos útiles

```bash
# Verificar conexión a Scroll Sepolia
curl http://localhost:5000/network-info

# Consultar balance
curl -X POST http://localhost:5000/get-balance \
  -H "Content-Type: application/json" \
  -d '{"address":"0x..."}'

# Chat con IA
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"¿Cuál es mi balance?","sender_wallet":"0x..."}'
```

## ⚠️ Notas importantes

1. **Red de prueba**: Scroll Sepolia es una testnet. Usa ETH de prueba.
2. **Gas fees**: Las transacciones requieren ETH para gas.
3. **RPC público**: El RPC público puede tener límites de tasa. Considera usar uno privado para producción.
4. **Direcciones**: Todas las direcciones deben empezar con `0x` y tener 42 caracteres.

## 🎨 Diferencias con Stacks

| Aspecto | Stacks | Scroll Sepolia |
|---------|--------|----------------|
| Formato de dirección | ST... / SP... | 0x... |
| Moneda nativa | STX | ETH |
| Unidad mínima | microSTX (1e-6) | Wei (1e-18) |
| Smart contracts | Clarity | Solidity |
| Wallet | Leather, Xverse | MetaMask, RainbowKit |

## 🤝 Contribuir

Este backend está diseñado para trabajar con el contrato STXTransfer en Scroll Sepolia. Si necesitas adaptarlo para otra red EVM, solo cambia las variables de entorno.

---

**Desarrollado con ❤️ para Scroll Sepolia**

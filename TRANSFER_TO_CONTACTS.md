# 💸 Transferir STX a Contactos por Nombre

Esta funcionalidad permite que los usuarios envíen STX a sus contactos usando **solo el nombre**, sin necesidad de recordar las wallets completas.

## 🎯 Cómo Funciona

1. El usuario conecta su wallet (ej: `ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6`)
2. El usuario dice: **"Envía 10 STX a Andrés"**
3. La IA:
   - Identifica que es una transferencia a contacto
   - Busca al usuario en la BD usando su wallet conectada
   - Busca el contacto "Andrés" en sus contactos
   - Obtiene la wallet de Andrés automáticamente
   - Prepara la transacción con la wallet correcta

---

## 📋 Flujo Completo

### Paso 1: Registrar Usuario

Primero, el usuario debe estar registrado en la base de datos.

**Request:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Juan",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Usuario creado correctamente",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "Juan",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "created_at": "2025-10-26T10:30:00Z"
  }
}
```

---

### Paso 2: Agregar Contactos

El usuario agrega contactos a su lista.

**Request:**
```bash
curl -X POST http://localhost:5000/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Andrés",
    "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Contacto creado correctamente",
  "contact": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Andrés",
    "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    "created_at": "2025-10-26T12:00:00Z"
  }
}
```

Agregar más contactos:

```bash
# María
curl -X POST http://localhost:5000/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "María",
    "wallet_address": "ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG"
  }'

# Pedro
curl -X POST http://localhost:5000/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Pedro",
    "wallet_address": "ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R"
  }'
```

---

### Paso 3: Transferir usando Nombre

Ahora el usuario puede transferir STX usando solo el nombre del contacto.

**Request:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Envía 10 STX a Andrés",
    "sender_wallet": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
  }'
```

**Response (Exitosa):**
```json
{
  "action": "transfer",
  "contact_name": "Andrés",
  "recipient": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "recipient_name": "Andrés",
  "amount": 10,
  "sender": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "contact_id": "770e8400-e29b-41d4-a716-446655440002",
  "message": "✅ Contacto 'Andrés' encontrado. Preparando transferencia de 10 STX a ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "success": true
}
```

---

## 🎨 Ejemplos de Comandos

### ✅ Comandos Válidos

```javascript
// Variaciones del mismo comando
"Envía 10 STX a Andrés"
"Transfiere 25 STX a María"
"Manda 50 STX a Pedro"
"Envia 5 STX a andres"  // ⚠️ No importan mayúsculas
"Envía 100 stx a MARÍA"
```

### ❌ Errores Comunes

**1. Usuario no registrado:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Envía 10 STX a Andrés",
    "sender_wallet": "ST999WALLET999NO999REGISTRADA"
  }'
```

**Response:**
```json
{
  "action": "transfer_to_contact",
  "error": "No se encontró un usuario con esa wallet",
  "message": "❌ Tu wallet ST999WALLET999NO999REGISTRADA no está registrada. Regístrate primero."
}
```

---

**2. Contacto no existe:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Envía 10 STX a Carlos",
    "sender_wallet": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
  }'
```

**Response:**
```json
{
  "action": "transfer_to_contact",
  "error": "Contacto 'Carlos' no encontrado",
  "message": "❌ No encontré a 'Carlos' en tus contactos.",
  "available_contacts": ["Andrés", "María", "Pedro"],
  "suggestion": "Contactos disponibles: Andrés, María, Pedro"
}
```

---

**3. Sin contactos:**
```json
{
  "action": "transfer_to_contact",
  "error": "No tienes contactos registrados",
  "message": "❌ Juan, aún no tienes contactos. Agrega algunos primero."
}
```

---

## 🔍 Ver Contactos por Wallet

Para ver los contactos de un usuario sin conocer su ID:

**Request:**
```bash
curl http://localhost:5000/users/wallet/ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6/contacts
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "Juan",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
  },
  "count": 3,
  "contacts": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Andrés",
      "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
      "created_at": "2025-10-26T12:00:00Z"
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "María",
      "wallet_address": "ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG",
      "created_at": "2025-10-26T12:30:00Z"
    },
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Pedro",
      "wallet_address": "ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R",
      "created_at": "2025-10-26T13:00:00Z"
    }
  ]
}
```

---

## 💻 Integración con Frontend (React/JavaScript)

### Ejemplo Completo

```javascript
// 1. Estado en tu componente React
const [userWallet, setUserWallet] = useState("ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6");
const [message, setMessage] = useState("");
const [response, setResponse] = useState(null);

// 2. Función para enviar comando a la IA
async function sendCommand() {
  try {
    const res = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        sender_wallet: userWallet  // ⚠️ IMPORTANTE: Pasar la wallet conectada
      })
    });
    
    const data = await res.json();
    setResponse(data);
    
    // Si la transferencia fue exitosa, mostrar detalles
    if (data.success && data.action === "transfer") {
      console.log(`✅ Transferir ${data.amount} STX a ${data.recipient_name}`);
      console.log(`   Wallet destino: ${data.recipient}`);
      
      // Aquí llamarías a tu función de Stacks para ejecutar la transacción
      // await executeTransfer(data.recipient, data.amount);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// 3. Componente UI
return (
  <div>
    <h2>Enviar STX a Contactos</h2>
    
    <p>Wallet conectada: {userWallet}</p>
    
    <input
      type="text"
      value={message}
      onChange={(e) => setMessage(e.target.value)}
      placeholder="Ej: Envía 10 STX a Andrés"
    />
    
    <button onClick={sendCommand}>Enviar</button>
    
    {response && (
      <div>
        <h3>Respuesta:</h3>
        <pre>{JSON.stringify(response, null, 2)}</pre>
      </div>
    )}
  </div>
);
```

### Con Leather Wallet (Stacks)

```javascript
import { showConnect } from '@stacks/connect';
import { openContractCall } from '@stacks/connect';

// 1. Conectar wallet
async function connectWallet() {
  const userSession = await showConnect({
    appDetails: {
      name: 'Mi DApp',
      icon: window.location.origin + '/logo.png',
    },
    onFinish: ({ userSession }) => {
      const wallet = userSession.loadUserData().profile.stxAddress.testnet;
      setUserWallet(wallet);
    },
  });
}

// 2. Ejecutar transferencia después de que la IA encuentre el contacto
async function executeTransfer(recipient, amount) {
  const options = {
    contractAddress: 'ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R',
    contractName: 'traspaso-v2',
    functionName: 'transfer-stx',
    functionArgs: [
      `'${recipient}`,
      `u${amount * 1000000}`  // Convertir a microSTX
    ],
    onFinish: (data) => {
      console.log('Transacción enviada:', data.txId);
    },
  };
  
  await openContractCall(options);
}
```

---

## 🚀 Flujo Completo en Frontend

```javascript
async function transferToContact(contactName, amount, senderWallet) {
  // 1. Preguntar a la IA por el contacto
  const aiResponse = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: `Envía ${amount} STX a ${contactName}`,
      sender_wallet: senderWallet
    })
  });
  
  const data = await aiResponse.json();
  
  // 2. Verificar que el contacto fue encontrado
  if (data.success && data.action === "transfer") {
    console.log(`Contacto encontrado: ${data.recipient_name}`);
    console.log(`Wallet: ${data.recipient}`);
    
    // 3. Mostrar confirmación al usuario
    const confirmed = confirm(
      `¿Deseas transferir ${amount} STX a ${data.recipient_name}?\n` +
      `Wallet: ${data.recipient}`
    );
    
    if (confirmed) {
      // 4. Ejecutar la transacción en Stacks
      await executeTransfer(data.recipient, amount);
      return { success: true, txId: 'xxx' };
    }
  } else {
    // Mostrar error al usuario
    alert(data.message);
    
    // Si hay contactos sugeridos, mostrarlos
    if (data.available_contacts) {
      console.log('Contactos disponibles:', data.available_contacts);
    }
    
    return { success: false, error: data.message };
  }
}

// Uso
await transferToContact("Andrés", 10, "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6");
```

---

## 📝 Notas Importantes

1. **`sender_wallet` es obligatorio**: El frontend debe enviar la wallet conectada del usuario en cada request al endpoint `/chat`

2. **Búsqueda flexible**: La IA busca nombres ignorando mayúsculas/minúsculas y hace búsqueda parcial si no encuentra coincidencia exacta

3. **Validaciones automáticas**:
   - Verifica que el usuario esté registrado
   - Verifica que tenga contactos
   - Busca el contacto por nombre
   - Valida que la cantidad sea válida

4. **Seguridad**: Asegúrate de que solo la wallet conectada pueda acceder a sus propios contactos (ya implementado)

5. **UX Mejorada**: Si el contacto no existe, la IA sugiere los contactos disponibles

---

## 🎯 Casos de Uso

- **DApp de Pagos**: "Pagar 50 STX a Café Central"
- **App de Remesas**: "Enviar 100 STX a Mamá"
- **Juegos**: "Transferir 25 STX a Player123"
- **E-commerce**: "Pagar 75 STX a TiendaOnline"

---

## ✨ Próximas Mejoras

- [ ] Agregar apodos/aliases para contactos
- [ ] Historial de transferencias a contactos
- [ ] Grupos de contactos
- [ ] Transferencias programadas
- [ ] Multi-firma con contactos

¡Ahora tus usuarios pueden enviar STX tan fácil como enviar un mensaje! 💬💸

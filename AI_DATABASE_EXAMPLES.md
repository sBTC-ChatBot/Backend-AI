# 🤖 Ejemplos de Interacción IA + Base de Datos

Tu IA de DeepSeek ahora puede interpretar comandos en lenguaje natural y ejecutar acciones tanto en la blockchain de Stacks como en tu base de datos de Supabase.

## 📝 Cómo Funciona

Envía un mensaje en lenguaje natural al endpoint `/chat` y la IA:
1. Interpreta tu intención
2. Identifica la acción a realizar
3. Extrae los parámetros necesarios
4. **Ejecuta automáticamente** la acción en la base de datos (si corresponde)
5. Devuelve el resultado

---

## 🗄️ Comandos de Base de Datos

### 1. **Listar Usuarios**

**Ejemplos de comandos:**
```
"Muéstrame todos los usuarios"
"¿Cuántos usuarios hay registrados?"
"Lista de usuarios"
"Ver usuarios"
"Quiero ver todos los usuarios"
```

**Petición:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Muéstrame todos los usuarios"}'
```

**Respuesta:**
```json
{
  "action": "list_users",
  "message": "Se encontraron 3 usuarios registrados",
  "count": 3,
  "users": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
      "created_at": "2025-10-26T10:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "username": "janedoe",
      "wallet_address": "ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R",
      "created_at": "2025-10-26T11:00:00Z"
    }
  ]
}
```

---

### 2. **Buscar Usuario por Wallet**

**Ejemplos de comandos:**
```
"Busca el usuario con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
"¿Quién tiene la wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6?"
"Encuentra el usuario ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
"Información del usuario con dirección ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
```

**Petición:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Busca el usuario con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"}'
```

**Respuesta:**
```json
{
  "action": "get_user",
  "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "message": "Usuario encontrado: johndoe",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "created_at": "2025-10-26T10:30:00Z"
  }
}
```

---

### 3. **Crear Usuario**

**Ejemplos de comandos:**
```
"Registra un usuario llamado Juan con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
"Crea un usuario Pedro con dirección ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
"Nuevo usuario María con wallet ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG"
"Quiero registrar a Carlos con la wallet ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R"
```

**Petición:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Registra un usuario llamado Juan con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"}'
```

**Respuesta exitosa:**
```json
{
  "action": "create_user",
  "username": "Juan",
  "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "message": "✅ Usuario 'Juan' creado exitosamente",
  "user": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "username": "Juan",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "created_at": "2025-10-26T14:30:00Z"
  }
}
```

**Respuesta si la wallet ya existe:**
```json
{
  "action": "create_user",
  "username": "Juan",
  "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "message": "Creando usuario Juan",
  "error": "Esta wallet ya está registrada"
}
```

---

### 4. **Ver Contactos de un Usuario**

**Ejemplos de comandos:**
```
"Muéstrame los contactos del usuario 550e8400-e29b-41d4-a716-446655440000"
"¿Qué contactos tiene el usuario 550e8400-e29b-41d4-a716-446655440000?"
"Lista los contactos de 550e8400-e29b-41d4-a716-446655440000"
"Ver contactos del usuario 550e8400-e29b-41d4-a716-446655440000"
```

**Petición:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Muéstrame los contactos del usuario 550e8400-e29b-41d4-a716-446655440000"}'
```

**Respuesta:**
```json
{
  "action": "get_contacts",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Se encontraron 2 contactos",
  "count": 2,
  "contacts": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Alice",
      "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
      "created_at": "2025-10-26T12:00:00Z"
    },
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Bob",
      "wallet_address": "ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG",
      "created_at": "2025-10-26T12:30:00Z"
    }
  ]
}
```

---

### 5. **Crear Contacto**

**Ejemplos de comandos:**
```
"Agrega a María con wallet ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM como contacto del usuario 550e8400-e29b-41d4-a716-446655440000"
"Crea un contacto llamado Pedro con dirección ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG para el usuario 550e8400-e29b-41d4-a716-446655440000"
"Nuevo contacto Carlos con wallet ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R para 550e8400-e29b-41d4-a716-446655440000"
```

**Petición:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Agrega a María con wallet ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM como contacto del usuario 550e8400-e29b-41d4-a716-446655440000"}'
```

**Respuesta:**
```json
{
  "action": "create_contact",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "nombre": "María",
  "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
  "message": "✅ Contacto 'María' agregado exitosamente",
  "contact": {
    "id": "aa0e8400-e29b-41d4-a716-446655440005",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "María",
    "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    "created_at": "2025-10-26T15:00:00Z"
  }
}
```

---

## ⛓️ Comandos de Blockchain (Ya existentes)

### 6. **Transferir STX**

**Ejemplos:**
```
"Transfiere 50 STX a ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
"Envía 100 STX a la wallet ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
"Quiero transferir 25 STX a ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG"
```

**Respuesta:**
```json
{
  "action": "transfer",
  "recipient": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "amount": 50,
  "message": "Transferir 50 STX"
}
```

---

### 7. **Consultar Balance**

**Ejemplos:**
```
"¿Cuál es el balance de ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6?"
"Saldo de la wallet ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
"Consulta el balance de ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG"
```

**Respuesta:**
```json
{
  "action": "balance",
  "address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
  "message": "Consultando balance"
}
```

---

## 🔄 Ejemplo de Flujo Completo con JavaScript

```javascript
// 1. Crear un usuario
fetch('http://localhost:5000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Registra un usuario llamado Juan con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6'
  })
})
.then(res => res.json())
.then(data => {
  console.log('Usuario creado:', data);
  const userId = data.user.id;
  
  // 2. Agregar un contacto al usuario creado
  return fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: `Agrega a María con wallet ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM como contacto del usuario ${userId}`
    })
  });
})
.then(res => res.json())
.then(data => {
  console.log('Contacto agregado:', data);
  
  // 3. Listar todos los usuarios
  return fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: 'Muéstrame todos los usuarios'
    })
  });
})
.then(res => res.json())
.then(data => {
  console.log('Lista de usuarios:', data);
});
```

---

## 💡 Ventajas de esta Integración

1. **Interfaz Natural**: Los usuarios pueden interactuar con tu base de datos usando lenguaje natural
2. **Automatización**: La IA ejecuta automáticamente las acciones en Supabase
3. **Flexibilidad**: Puedes hacer las mismas preguntas de diferentes formas
4. **Integración Completa**: Combina blockchain + base de datos + IA en un solo endpoint
5. **Respuestas Inteligentes**: La IA contextualiza los resultados con mensajes amigables

---

## 🎯 Casos de Uso

- **Chatbot para DApp**: Los usuarios pueden gestionar su perfil con comandos de voz/texto
- **Panel de Administración**: Consultas rápidas a la base de datos sin SQL
- **Onboarding Conversacional**: "Registra mi cuenta con mi wallet de Leather"
- **Búsquedas Inteligentes**: "¿Cuántos usuarios se registraron hoy?"
- **Gestión de Contactos**: "Agrega a todos mis amigos del chat grupal"

---

## ⚠️ Notas Importantes

1. La IA interpreta el lenguaje natural, así que sé lo más claro posible
2. Para acciones de base de datos, asegúrate de proporcionar todos los datos necesarios
3. Los IDs de usuario son UUIDs (generados automáticamente)
4. Las wallets deben empezar con ST (testnet) o SP (mainnet)
5. El endpoint `/chat` ahora ejecuta acciones automáticamente, no solo las interpreta

---

## 🚀 Próximos Pasos

Puedes extender esta funcionalidad agregando más acciones como:
- Actualizar usuarios
- Eliminar contactos
- Buscar usuarios por nombre
- Estadísticas de usuarios
- Filtros avanzados
- Y mucho más...

¡La IA de DeepSeek ahora es el cerebro de tu aplicación! 🧠✨

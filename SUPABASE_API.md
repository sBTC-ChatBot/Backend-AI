# 📚 Documentación de Endpoints de Usuarios (Supabase)

## Configuración

Asegúrate de tener las siguientes variables en tu archivo `.env`:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
```

---

## Endpoints Disponibles

### 1. **Obtener Todos los Usuarios**

**GET** `/users`

Obtiene todos los usuarios registrados en Supabase.

#### Respuesta exitosa:
```json
{
  "success": true,
  "count": 2,
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

### 2. **Obtener Usuario por ID**

**GET** `/users/<user_id>`

Obtiene un usuario específico por su ID UUID.

#### Parámetros de ruta:
- `user_id` (UUID): ID del usuario

#### Ejemplo:
```
GET /users/550e8400-e29b-41d4-a716-446655440000
```

#### Respuesta exitosa:
```json
{
  "success": true,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "created_at": "2025-10-26T10:30:00Z"
  }
}
```

#### Respuesta error (no encontrado):
```json
{
  "success": false,
  "error": "Usuario no encontrado"
}
```

---

### 3. **Obtener Usuario por Wallet Address**

**GET** `/users/wallet/<wallet_address>`

Obtiene un usuario por su dirección de wallet de Stacks.

#### Parámetros de ruta:
- `wallet_address` (string): Dirección de la wallet (debe empezar con ST o SP)

#### Ejemplo:
```
GET /users/wallet/ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6
```

#### Respuesta exitosa:
```json
{
  "success": true,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "created_at": "2025-10-26T10:30:00Z"
  }
}
```

---

### 4. **Obtener Contactos de un Usuario**

**GET** `/users/<user_id>/contacts`

Obtiene todos los contactos asociados a un usuario.

#### Parámetros de ruta:
- `user_id` (UUID): ID del usuario

#### Ejemplo:
```
GET /users/550e8400-e29b-41d4-a716-446655440000/contacts
```

#### Respuesta exitosa:
```json
{
  "success": true,
  "count": 2,
  "contacts": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Alice Cooper",
      "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
      "created_at": "2025-10-26T12:00:00Z"
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Bob Dylan",
      "wallet_address": "ST2CY5V39NHDPWSXMW9QDT3HC3GD6Q6XX4CFRK9AG",
      "created_at": "2025-10-26T12:30:00Z"
    }
  ]
}
```

---

### 5. **Crear un Nuevo Usuario**

**POST** `/users`

Crea un nuevo usuario en Supabase.

#### Body (JSON):
```json
{
  "username": "johndoe",
  "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
}
```

#### Validaciones:
- `username` y `wallet_address` son obligatorios
- `wallet_address` debe comenzar con ST o SP
- `wallet_address` debe ser único (no puede estar duplicado)

#### Respuesta exitosa (201):
```json
{
  "success": true,
  "message": "Usuario creado correctamente",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6",
    "created_at": "2025-10-26T10:30:00Z"
  }
}
```

#### Respuesta error (wallet duplicada - 409):
```json
{
  "success": false,
  "error": "Esta wallet ya está registrada"
}
```

#### Respuesta error (datos faltantes - 400):
```json
{
  "success": false,
  "error": "Se requieren username y wallet_address"
}
```

---

### 6. **Crear un Nuevo Contacto**

**POST** `/contacts`

Crea un nuevo contacto para un usuario.

#### Body (JSON):
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "nombre": "Alice Cooper",
  "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
}
```

#### Validaciones:
- `user_id`, `nombre` y `wallet_address` son obligatorios
- `wallet_address` debe comenzar con ST o SP
- La combinación de `user_id` y `wallet_address` debe ser única

#### Respuesta exitosa (201):
```json
{
  "success": true,
  "message": "Contacto creado correctamente",
  "contact": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Alice Cooper",
    "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM",
    "created_at": "2025-10-26T12:00:00Z"
  }
}
```

#### Respuesta error (contacto duplicado - 409):
```json
{
  "success": false,
  "error": "Este contacto ya existe para el usuario"
}
```

---

## Ejemplos de Uso con cURL

### Obtener todos los usuarios:
```bash
curl http://localhost:5000/users
```

### Obtener usuario por ID:
```bash
curl http://localhost:5000/users/550e8400-e29b-41d4-a716-446655440000
```

### Obtener usuario por wallet:
```bash
curl http://localhost:5000/users/wallet/ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6
```

### Crear un nuevo usuario:
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "wallet_address": "ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"
  }'
```

### Crear un contacto:
```bash
curl -X POST http://localhost:5000/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Alice Cooper",
    "wallet_address": "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
  }'
```

### Obtener contactos de un usuario:
```bash
curl http://localhost:5000/users/550e8400-e29b-41d4-a716-446655440000/contacts
```

---

## Ejemplos de Uso con JavaScript (Fetch)

### Obtener todos los usuarios:
```javascript
fetch('http://localhost:5000/users')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### Crear un nuevo usuario:
```javascript
fetch('http://localhost:5000/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'johndoe',
    wallet_address: 'ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6'
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

---

## Estructura de la Base de Datos

### Tabla: `users`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | ID único del usuario (generado automáticamente) |
| username | TEXT | Nombre de usuario |
| wallet_address | TEXT | Dirección de wallet de Stacks (único) |
| created_at | TIMESTAMPTZ | Fecha de creación |

### Tabla: `contacts`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | ID único del contacto (generado automáticamente) |
| user_id | UUID | ID del usuario (foreign key a users.id) |
| nombre | TEXT | Nombre del contacto |
| wallet_address | TEXT | Dirección de wallet del contacto |
| created_at | TIMESTAMPTZ | Fecha de creación |

**Restricción única:** La combinación de `user_id` y `wallet_address` debe ser única.

---

## Notas Importantes

1. **Seguridad**: Asegúrate de configurar correctamente las políticas de RLS (Row Level Security) en Supabase para proteger tus datos.

2. **CORS**: El backend tiene CORS habilitado para permitir peticiones desde el frontend.

3. **Validaciones**: Todas las wallet addresses deben comenzar con `ST` (testnet) o `SP` (mainnet).

4. **Errores**: Todos los endpoints manejan errores y devuelven mensajes descriptivos en formato JSON.

5. **IDs**: Los IDs son UUIDs generados automáticamente por Supabase.

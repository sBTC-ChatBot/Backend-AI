# 🚀 Despliegue en Render

## 📋 Variables de Entorno Requeridas

Configura estas variables en Render Dashboard → Environment:

```
CONTRACT_ADDRESS=tu_contract_address
CONTRACT_NAME=tu_contract_name
STACKS_NETWORK=testnet
DEEPSEEK_API_KEY=tu_deepseek_api_key
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
PORT=5000
```

---

## 🔧 Configuración en Render

### 1. **Crear Web Service**

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub

### 2. **Configuración del Service**

| Campo | Valor |
|-------|-------|
| **Name** | backend-ai (o el nombre que prefieras) |
| **Region** | Oregon (US West) o el más cercano |
| **Branch** | main |
| **Root Directory** | (dejar vacío) |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | Free |

### 3. **Variables de Entorno**

Agregar en la sección **Environment**:

```bash
CONTRACT_ADDRESS=ST3AQ7KXWA7KGQ67EX2MFYR1E3231B9S4KY6EFB1R
CONTRACT_NAME=contador-simple-v1
STACKS_NETWORK=testnet
DEEPSEEK_API_KEY=sk-xxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx
PORT=5000
```

### 4. **Desplegar**

Click en **"Create Web Service"** y espera a que termine el despliegue.

---

## 🌐 URL del Backend

Una vez desplegado, tu backend estará disponible en:

```
https://tu-servicio.onrender.com
```

### Endpoints disponibles:

```bash
# Health check
https://tu-servicio.onrender.com/

# Usuarios
https://tu-servicio.onrender.com/users
https://tu-servicio.onrender.com/users/wallet/{wallet}

# Contactos
https://tu-servicio.onrender.com/users/wallet/{wallet}/contacts

# Chat con IA
https://tu-servicio.onrender.com/chat

# Transferencias
https://tu-servicio.onrender.com/prepare-transfer
```

---

## 🔄 Actualizar Frontend

Cambia la URL base en tu frontend:

```javascript
// Antes (desarrollo local)
const API_URL = 'http://localhost:5000';

// Después (producción en Render)
const API_URL = 'https://tu-servicio.onrender.com';
```

---

## ⚠️ Notas Importantes

### Free Tier de Render

- ⏰ El servicio se "duerme" después de 15 minutos de inactividad
- 🐌 La primera petición después de dormir puede tardar 30-60 segundos
- 💾 Límite de 750 horas/mes
- 🔄 Reinicia automáticamente si hay errores

### Recomendaciones

1. **Keep-Alive**: Considera usar un servicio como [UptimeRobot](https://uptimerobot.com/) para hacer ping cada 5 minutos y mantener el servicio activo

2. **CORS**: El backend ya tiene CORS habilitado (`CORS(app)`), así que funcionará con cualquier frontend

3. **Logs**: Revisa los logs en Render Dashboard si algo falla:
   - Dashboard → Tu servicio → **Logs**

4. **Verificar Despliegue**: Después de desplegar, prueba:
   ```bash
   curl https://tu-servicio.onrender.com/
   ```
   
   Debería devolver:
   ```json
   {
     "status": "ok",
     "message": "✅ Backend Flask funcionando correctamente"
   }
   ```

---

## 🐛 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` esté en la raíz del repositorio
- Asegúrate de que todas las dependencias estén listadas

### Error: "Application failed to start"
- Revisa los logs en Render Dashboard
- Verifica que todas las variables de entorno estén configuradas
- Confirma que el comando de inicio sea `gunicorn app:app`

### Error: "502 Bad Gateway"
- El servicio está iniciando (espera 1-2 minutos)
- O está "dormido" (espera 30-60 segundos en la primera petición)

### Error de CORS
- Ya está configurado en `app.py` con `CORS(app)`
- Si persiste, verifica que tu frontend use HTTPS

---

## 🔐 Seguridad

### Variables Sensibles

**NUNCA** commitear en Git:
- ❌ API keys (DeepSeek, Supabase)
- ❌ Credenciales
- ❌ Tokens

**SIEMPRE** usar variables de entorno en Render.

### .gitignore

Asegúrate de tener esto en `.gitignore`:

```
.env
.env.local
__pycache__/
*.pyc
.venv/
venv/
```

---

## 📊 Monitoreo

### Health Checks

Render hace health checks automáticos a tu endpoint `/`.

Si falla más de 3 veces seguidas, reinicia el servicio.

### Métricas

En el Dashboard de Render puedes ver:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🚀 Despliegue Automático

Render redespliega automáticamente cuando:
- Haces push a la rama `main` en GitHub
- Actualizas variables de entorno
- Cambias configuración del servicio

---

## 💡 Tips

1. **Prueba Local Primero**: 
   ```bash
   gunicorn app:app
   ```
   Si funciona local con gunicorn, funcionará en Render

2. **Usa un `.env.example`**:
   Crea este archivo para documentar las variables necesarias

3. **Backup de Variables**:
   Guarda las variables de entorno en un lugar seguro (no en Git)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los [logs en Render](https://dashboard.render.com/)
2. Consulta la [documentación de Render](https://render.com/docs)
3. Verifica que todas las variables de entorno estén configuradas
4. Prueba los endpoints con Postman o cURL

---

¡Tu backend está listo para producción! 🎉

# 🚀 Guía de Despliegue en Render

## Paso 1: Preparar el Repositorio

Asegúrate de tener estos archivos (ya los tienes):
- ✅ `requirements.txt` (con gunicorn)
- ✅ `app.py`
- ✅ `.gitignore` (para no subir .env)

## Paso 2: Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Haz clic en **Sign Up**
3. Conecta con tu cuenta de GitHub

## Paso 3: Crear Web Service

1. En el dashboard, haz clic en **New +**
2. Selecciona **Web Service**
3. Conecta tu repositorio: `JHAMILCALI/clarity-backend`
4. Haz clic en **Connect**

## Paso 4: Configurar el Servicio

Completa los campos:

### Información Básica:
- **Name**: `clarity-backend` (o el que prefieras)
- **Region**: Selecciona la más cercana (US West, por ejemplo)
- **Branch**: `main`
- **Root Directory**: (déjalo vacío)

### Build & Deploy:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

### Plan:
- Selecciona **Free** (0$/mes)

## Paso 5: Variables de Entorno

En la sección **Environment**, agrega:

| Key | Value |
|-----|-------|
| `DEEPSEEK_API_KEY` | `sk-f984577379764c759173c5762d9c25ec` |
| `STACKS_NETWORK` | `testnet` |
| `CONTRACT_ADDRESS` | `ST3MHY0Z6DK6KC137X9XZQ4R61Y1PNRDN90MB3YHW` |
| `CONTRACT_NAME` | `contador` |
| `PYTHON_VERSION` | `3.10.0` |

⚠️ **Importante**: NO incluyas el archivo `.env` en Git. Las variables se configuran aquí.

## Paso 6: Desplegar

1. Haz clic en **Create Web Service**
2. Render comenzará a construir tu aplicación
3. Espera 2-5 minutos
4. ¡Tu API estará en línea! 🎉

La URL será algo como: `https://clarity-backend-xxxx.onrender.com`

## Paso 7: Probar la API

```bash
# Health check
curl https://tu-app.onrender.com/

# Respuesta esperada:
{
  "status": "ok",
  "message": "✅ Backend Flask funcionando correctamente"
}
```

## 🔄 Despliegue Automático

Cada vez que hagas `git push` a tu repositorio, Render:
1. Detectará los cambios
2. Reconstruirá la aplicación automáticamente
3. Desplegará la nueva versión

## ⚠️ Limitaciones del Plan Gratuito

- Tu servicio se "duerme" después de 15 minutos de inactividad
- La primera petición después de dormir tardará ~30 segundos (cold start)
- 750 horas/mes de uso (suficiente para desarrollo)

## 💡 Tip: Mantener el Servicio Activo

Si quieres evitar el "cold start", puedes usar servicios como:
- [Uptime Robot](https://uptimerobot.com) - Hace ping cada 5 minutos (gratis)
- [Cron Job](https://cron-job.org) - Llama a tu API periódicamente

## 🔧 Solución de Problemas

### Error: "Application failed to respond"
- Verifica que el comando sea `gunicorn app:app` (no `python app.py`)
- Revisa los logs en el dashboard de Render

### Error: Variables de entorno
- Asegúrate de haber agregado todas las variables necesarias
- Verifica que no haya espacios extra en los valores

### Error: Build failed
- Revisa que `requirements.txt` esté correcto
- Verifica los logs de build en Render

## 📚 Documentación Oficial

- [Render Docs - Deploy Flask](https://render.com/docs/deploy-flask)
- [Render Docs - Environment Variables](https://render.com/docs/environment-variables)

---

## 🎉 ¡Listo!

Tu backend está desplegado y accesible desde cualquier parte del mundo.

**URL de tu API**: `https://clarity-backend-xxxx.onrender.com`

Actualiza esta URL en tu frontend para conectarte a la API en producción.

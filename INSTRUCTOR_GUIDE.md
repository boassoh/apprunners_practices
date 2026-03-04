# 📘 Guía del Instructor: App Runner + GitHub Integration

**⚠️ ESTE DOCUMENTO NO SE SUBE AL REPOSITORIO ⚠️**

Este documento contiene las instrucciones completas y testeadas para configurar App Runner con integración directa a GitHub.

---

## 🎯 Objetivo del Ejercicio

Los alumnos crearán un **segundo servicio de App Runner** que:
- Se conecta directamente a su repositorio personal de GitHub
- Despliega automáticamente cuando hacen push al repo
- No requiere ECR ni build local
- Demuestra CI/CD nativo de App Runner

---

## 📋 Pre-requisitos

### Para el Instructor (Testear antes):
- [ ] Cuenta de GitHub personal
- [ ] Repositorio de prueba creado
- [ ] Código de la aplicación subido al repo
- [ ] Permisos de AWS App Runner configurados

### Para los Alumnos:
- [ ] Cuenta de GitHub (gratuita)
- [ ] Git instalado localmente
- [ ] Acceso a AWS Console

---

## 🧪 Proceso de Testing (Instructor)

### Paso 1: Crear Repositorio en GitHub

1. Ir a **GitHub.com** y hacer login
2. Click en **New repository**
3. Configuración:
   - **Repository name:** `edem-app-github`
   - **Description:** `App Runner GitHub Integration Demo`
   - **Visibility:** Public (o Private si prefieres)
   - **Initialize:** ✅ Add a README file
4. Click **Create repository**

**✅ Verificación:** Repositorio creado en `https://github.com/boassoh/apprunners_practices`

---

### Paso 2: Subir Código de la Aplicación

**Opción A: Desde la línea de comandos**

```bash
# Clonar el repositorio
git clone https://github.com/<tu-usuario>/edem-app-github.git
cd edem-app-github

# Copiar archivos de la aplicación
cp /ruta/a/app.py .
cp /ruta/a/Dockerfile .
cp /ruta/a/requirements.txt .
cp -r /ruta/a/templates .

# Commit y push
git add .
git commit -m "Initial commit: Flask app"
git push origin main
```

**Opción B: Desde GitHub Web UI**

1. En el repositorio, click **Add file > Upload files**
2. Arrastrar: `app.py`, `Dockerfile`, `requirements.txt`, carpeta `templates/`
3. Commit message: `Initial commit: Flask app`
4. Click **Commit changes**

**✅ Verificación:** Los archivos aparecen en el repositorio

---

### ⚠️ Lecciones Aprendidas (Errores y Soluciones)

#### 1. `pip: command not found`
- **Problema:** La imagen base de App Runner no tiene `pip` en el PATH
- **Solución:** Usar `python3 -m pip` en lugar de `pip`

#### 2. `python: executable file not found`
- **Problema:** Solo existe `python3`, no `python`
- **Solución:** Usar siempre `python3` en Start command

#### 3. `No module named 'flask'` / `No module named 'pyramid'`
- **Problema:** Los módulos instalados en el build stage no están disponibles en el runtime si se instalan en la ruta por defecto
- **Solución:** Instalar con `--target /app/<source_directory>` para que persistan al runtime

#### 4. Error de JavaScript en la consola de AWS (`Cannot read properties of null`)
- **Problema:** Bug de la UI de App Runner al crear conexión con GitHub
- **Solución:** Refrescar la página y seleccionar la conexión existente desde el dropdown en lugar de crear una nueva

#### 5. Flask 3.0.0 incompatible
- **Problema:** Flask 3.0.0 causa problemas de build en App Runner
- **Solución:** Usar Flask 2.3.0 + Werkzeug 2.3.0, o mejor aún, usar Pyramid

#### 6. Usar Pyramid en lugar de Flask para source code deployment
- El ejemplo oficial de AWS usa Pyramid con `wsgiref.simple_server`
- Pyramid funciona sin necesidad de servidor WSGI externo (gunicorn, etc.)
- Más simple y compatible con el build nativo de App Runner

---

### ✅ Configuración Final Probada y Funcional

| Parámetro | Valor |
|-----------|-------|
| **Runtime** | Python 3 |
| **Source directory** | `/github-example` |
| **Build command** | `python3 -m pip install --target /app/github-example pyramid` |
| **Start command** | `python3 server.py` |
| **Port** | `8080` |

---

### Paso 3: Crear Servicio App Runner desde GitHub

#### 3.1. Acceder a App Runner Console

1. Ir a **AWS Console > App Runner**
2. Click **Create service**

#### 3.2. Configurar Source

1. **Source:**
   - Seleccionar: **Source code repository**
   
2. **Connect to GitHub:**
   - Click **Add new**
   - **Connection name:** `github-connection` (o el nombre que prefieras)
   - Click **Install another**
   - Se abrirá una ventana de GitHub para autorizar

3. **Autorización en GitHub:**
   - Login en GitHub si es necesario
   - Seleccionar la cuenta/organización
   - Elegir repositorios:
     - **All repositories** (más fácil para testing)
     - O **Only select repositories** → Seleccionar `edem-app-github`
   - Click **Install & Authorize**
   
4. **Volver a AWS Console:**
   - La conexión debería aparecer como **Available**
   - Click **Next**

5. **Repository settings:**
   - **Repository:** Seleccionar `<tu-usuario>/edem-app-github`
   - **Branch:** `main` (o `master` si es tu default)
   - **Deployment trigger:** **Automatic** ✅
   - Click **Next**

**✅ Verificación:** Conexión establecida y repositorio seleccionado

---

#### 3.3. Configurar Build

1. **Configuration file:**
   - Seleccionar: **Use a configuration file** (si tienes `apprunner.yaml`)
   - O seleccionar: **Configure all settings here** (más simple para empezar)

2. **Si eliges "Configure all settings here":**
   - **Runtime:** Python 3
   - **Build command:** `python3 -m pip install --target /app/github-example pyramid`
   - **Start command:** `python3 server.py`
   - **Port:** `8080`

> ⚠️ **Importante:** Usar `python3 -m pip` (no `pip`) y `--target /app/<source_directory>` para que los módulos estén disponibles en runtime.

3. Click **Next**

**✅ Verificación:** Configuración de build completada

---

#### 3.4. Configurar Service

1. **Service settings:**
   - **Service name:** `edem-app-github-service`
   - **Virtual CPU:** 1 vCPU
   - **Virtual memory:** 2 GB

2. **Environment variables (opcional):**
   - Agregar si necesitas (ej: `APP_VERSION=github-v1.0`)

3. **Auto scaling:**
   - **Max concurrency:** 5
   - **Max size:** 3 instances
   - **Min size:** 1 instance

4. Click **Next**

**✅ Verificación:** Configuración del servicio completada

---

#### 3.5. Review and Create

1. Revisar toda la configuración
2. Click **Create & deploy**
3. **Esperar 5-8 minutos** (el primer despliegue tarda más)

**Estados esperados:**
- `Operation in progress` → Construyendo y desplegando
- `Running` → Servicio activo

**✅ Verificación:** Servicio en estado `Running` con URL pública

---

### Paso 4: Verificar Despliegue

1. Copiar la **Service URL** (ej: `https://abc123.eu-central-1.awsapprunner.com`)
2. Abrir en el navegador
3. Verificar que la aplicación carga correctamente

**✅ Verificación:** Aplicación accesible y funcionando

---

### Paso 5: Probar CI/CD Automático

#### 5.1. Hacer un Cambio en el Código

**Opción A: Desde GitHub Web UI**

1. Ir al repositorio en GitHub
2. Abrir `templates/index.html`
3. Click en el ícono de lápiz (Edit)
4. Cambiar algo visible (ej: el título o color)
5. Commit message: `Update: cambio de color`
6. Click **Commit changes**

**Opción B: Desde línea de comandos**

```bash
cd edem-app-github

# Editar el archivo
nano templates/index.html  # O tu editor preferido

# Commit y push
git add templates/index.html
git commit -m "Update: cambio de color"
git push origin main
```

#### 5.2. Observar el Redespliegue Automático

1. Ir a **App Runner Console**
2. Seleccionar el servicio `edem-app-github-service`
3. Observar:
   - Estado cambia a `Operation in progress`
   - En la pestaña **Deployments** aparece un nuevo deployment
   - Logs muestran el build process

4. Esperar 3-5 minutos hasta que vuelva a `Running`

5. Refrescar la URL del servicio en el navegador
6. Verificar que el cambio se aplicó

**✅ Verificación:** Cambio visible sin intervención manual = CI/CD funcionando

---

## 📊 Comparación: ECR vs GitHub Source

| Aspecto | ECR (Fase 1-6) | GitHub Source (Nueva fase) |
|---------|----------------|---------------------------|
| **Build** | Local (Docker) | App Runner (automático) |
| **Registry** | ECR | No necesario |
| **CI/CD** | Manual push a ECR | Automático con git push |
| **Complejidad** | Media | Baja |
| **Control** | Alto | Medio |
| **Velocidad setup** | 30 min | 10 min |
| **Uso típico** | Producción | Desarrollo/Prototipos |

---

## 🐛 Troubleshooting

### Problema 1: "Connection failed" al conectar GitHub

**Causa:** Permisos insuficientes o autorización cancelada

**Solución:**
1. Ir a **GitHub Settings > Applications > AWS Connector for GitHub**
2. Verificar que está instalado
3. Revocar y reinstalar si es necesario

---

### Problema 2: Build falla con "requirements.txt not found"

**Causa:** Archivo no está en el root del repositorio

**Solución:**
1. Verificar que `requirements.txt` está en la raíz (no en subcarpeta)
2. Verificar que el branch seleccionado es el correcto

---

### Problema 3: App no responde en el puerto correcto

**Causa:** Puerto configurado incorrectamente

**Solución:**
1. Verificar que `app.py` usa `port=8080`
2. Verificar que la configuración de App Runner tiene `Port: 8080`

---

### Problema 4: "Deployment failed" sin detalles

**Causa:** Error en el código o dependencias

**Solución:**
1. Ir a **Logs** en App Runner Console
2. Buscar errores en el build log
3. Verificar que `requirements.txt` tiene versiones compatibles

---

## 📝 Notas para el Ejercicio de los Alumnos

### Lo que DEBEN hacer:
1. Crear su propio repositorio en GitHub
2. Subir el código de la aplicación
3. Conectar App Runner con su GitHub
4. Configurar despliegue automático
5. Hacer un cambio y verificar CI/CD

### Lo que NO deben hacer:
- No necesitan ECR para este ejercicio
- No necesitan Docker instalado localmente
- No necesitan AWS CLI (todo desde Console)

### Tiempo estimado:
- **Setup inicial:** 15 minutos
- **Prueba de CI/CD:** 10 minutos
- **Total:** 25 minutos

---

## ✅ Checklist de Testing del Instructor

Antes de dar el ejercicio a los alumnos, verificar:

- [ ] Repositorio de prueba creado y funcional
- [ ] Conexión GitHub-AWS establecida correctamente
- [ ] Servicio App Runner desplegado exitosamente
- [ ] URL pública accesible
- [ ] CI/CD automático funciona (cambio → push → redespliegue)
- [ ] Logs accesibles y comprensibles
- [ ] Troubleshooting documentado
- [ ] Tiempo estimado validado

---

## 🎓 Objetivos de Aprendizaje

Al completar este ejercicio, los alumnos habrán aprendido:

1. ✅ Integración de AWS con GitHub
2. ✅ CI/CD nativo sin herramientas externas
3. ✅ Diferencia entre container registry y source code deployment
4. ✅ Cuándo usar cada enfoque (ECR vs GitHub)
5. ✅ Gestión de conexiones y permisos entre servicios

---

**Última actualización:** [Fecha de testing]
**Testeado por:** [Tu nombre]
**Región AWS:** eu-central-1
**Cuenta AWS:** 822414985516

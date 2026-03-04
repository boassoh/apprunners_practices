# 🚀 Laboratorio: Despliegue de Aplicación con ECR y App Runner

Este ejercicio práctico cubre el ciclo completo de containerización y despliegue de una aplicación web usando Amazon ECR (Elastic Container Registry) y AWS App Runner.

---

## 🐳 Fase 1: Containerización y ECR

**Objetivo:** Crear una imagen Docker y subirla a Amazon ECR.

### 1.1. Crear Repositorio en ECR
* Ir a **Amazon ECR Console > Repositories > Create repository**.
* Nombre: `edem-app`.
* Configuración: Dejar opciones por defecto (privado).
* Copiar el URI del repositorio creado.

### 1.2. Autenticación con ECR
Autenticar Docker con ECR:
```bash
aws ecr get-login-password --region <tu-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

### 1.3. Construir Imagen Docker
Crear la imagen desde el Dockerfile:
```bash
docker build -t edem-app .
```

### 1.4. Probar Localmente
Antes de subir a ECR, verificar que la aplicación funciona correctamente:
```bash
docker run -d -p 8080:8080 --name edem-app-test edem-app
```

Acceder desde el navegador a **http://localhost:8080** para verificar que la aplicación carga correctamente.

Detener y eliminar el contenedor de prueba:
```bash
docker stop edem-app-test
docker rm edem-app-test
```

### 1.5. Etiquetar Imagen
Etiquetar la imagen con el URI del repositorio ECR:
```bash
docker tag edem-app:latest <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:latest
```

### 1.6. Subir Imagen a ECR
Push de la imagen al repositorio:
```bash
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:latest
```

> **Evidencia de éxito:** La imagen aparecerá en el repositorio ECR con el tag `latest`.

---

## 🔍 Fase 2: Escaneo de Vulnerabilidades

**Objetivo:** Verificar la seguridad de la imagen antes de desplegarla.

### 2.1. Ejecutar Escaneo
Verificar la seguridad de la imagen con el escaneo automático:
* En **ECR Console > Repositories > edem-app**, seleccionar la imagen con tag `latest`.
* Si no se escaneó automáticamente, hacer clic en **Scan**.
* Esperar 1-2 minutos y refrescar la página.

### 2.2. Revisar Resultados
* En la columna **Vulnerabilities** verás un resumen (ej: "5 Critical, 10 High, 20 Medium").
* Hacer clic en el número o en el **image digest** para ver detalles completos.
* Revisar los CVE IDs, severidad, y paquetes afectados.

> **Evidencia de éxito:** El escaneo muestra vulnerabilidades detectadas con su nivel de severidad y recomendaciones.

---

## 🔄 Fase 3: Lifecycle Policies y Versionado

**Objetivo:** Implementar políticas de ciclo de vida para gestión automática de imágenes.

### 3.1. Crear Lifecycle Policy
En ECR Console, seleccionar el repositorio `edem-app`:
* Ir a **Lifecycle policies > Create rule**.
* **Rule priority:** 1
* **Rule description:** `Mantener solo la última imagen`
* **Image status:** `Any`
* **Match criteria:** `Image count more than` → `1`
* **Action:** `Expire`
* Guardar la regla.

### 3.2. Modificar la Aplicación
Editar `templates/index.html` para cambiar el color del gradiente:
```css
/* Línea 16 - Cambiar de purple a orange */
background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
```

### 3.3. Construir Nueva Versión
Crear la imagen con tag v2.0:
```bash
docker build -t edem-app:v2.0 .
```

### 3.4. Etiquetar y Subir v1.0
Primero, etiquetar la imagen original como v1.0:
```bash
docker tag edem-app:latest <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:v1.0
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:v1.0
```

### 3.5. Etiquetar y Subir v2.0
Ahora subir la nueva versión:
```bash
docker tag edem-app:v2.0 <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:v2.0
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:v2.0
```

### 3.6. Verificar Lifecycle Policy
Esperar unos minutos y verificar en ECR Console:
* La imagen `v1.0` debería haber sido eliminada automáticamente.
* Solo `v2.0` permanece en el repositorio.

> **Evidencia de éxito:** El repositorio ECR muestra solo 1 imagen (v2.0), demostrando que la lifecycle policy funcionó.

---

## 🏃 Fase 4: Despliegue con App Runner

**Objetivo:** Desplegar la aplicación containerizada usando AWS App Runner.

### 4.1. Configuración de IAM Role
Crear un rol de IAM para App Runner (si no existe):
* Ir a **IAM Console > Roles > Create role**.
* Tipo: **AWS Service** > **App Runner**.
* Adjuntar política: `AWSAppRunnerServicePolicyForECRAccess`.
* Nombre del rol: `AppRunnerECRAccessRole`.

### 4.2. Crear Servicio en App Runner
* Ir a **App Runner Console > Create service**.
* **Source:** Container registry > Amazon ECR.
* **Container image URI:** Seleccionar la imagen de ECR `edem-app:latest`.
* **Deployment trigger:** **Automatic** (para CI/CD automático).
* **ECR access role:** Seleccionar el rol creado en el paso 1.

### 4.3. Configurar Servicio
* **Service name:** `edem-app-service`.
* **Port:** 8080 (o el puerto que use tu aplicación).
* **CPU & Memory:** 1 vCPU, 2 GB (ajustar según necesidad).
* **Environment variables:** Agregar variables si son necesarias.

### 4.4. Desplegar
* Revisar configuración y hacer clic en **Create & deploy**.
* Esperar a que el servicio esté en estado **Running** (puede tomar varios minutos).

> **Evidencia de éxito:** App Runner proporcionará una URL pública para acceder a la aplicación.

### 4.5. Verificación
Acceder a la URL proporcionada por App Runner para verificar que la aplicación está funcionando correctamente.

---

## 🔄 Fase 5: Despliegue Automático (CI/CD)

**Objetivo:** Experimentar el despliegue automático al actualizar la imagen en ECR.

### 5.1. Modificar la Aplicación
Editar `templates/index.html` para cambiar el color del gradiente:
```css
/* Línea 16 - Cambiar el segundo color */
background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
```

### 5.2. Reconstruir y Subir Nueva Imagen
Construir la nueva versión con el tag `latest`:
```bash
docker build -t edem-app:latest .
docker tag edem-app:latest <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/edem-app:latest
```

### 5.3. Observar Despliegue Automático
* Ir a **App Runner Console** y observar el servicio.
* El estado cambiará a **Operation in progress** automáticamente.
* App Runner detecta la nueva imagen y despliega automáticamente.
* Esperar a que vuelva a **Running** (2-3 minutos).

### 5.4. Verificar Cambios
Acceder nuevamente a la URL del servicio y verificar que el gradiente cambió de color.

> **Evidencia de éxito:** La aplicación muestra el nuevo color sin intervención manual, demostrando CI/CD automático.

---

## 📊 Fase 6: Observar Autoscaling

**Objetivo:** Generar carga para observar cómo App Runner escala automáticamente las instancias.

### 6.1. Configurar Autoscaling Personalizado
Antes de la prueba, asegúrate de tener una configuración de autoscaling personalizada:
* Ir a **App Runner Console > Auto scaling configurations > Create**.
* **Configuration name:** `edem-autoscaling`
* **Max concurrency:** `5` (requests concurrentes por instancia)
* **Max size:** `3` (máximo de instancias)
* **Min size:** `1` (mínimo de instancias)
* Asociar esta configuración a tu servicio.

### 6.2. Ejecutar Prueba de Carga
Usar el script proporcionado para generar carga:
```bash
chmod +x load_test.sh
./load_test.sh https://<tu-app-runner-url>
```

El script:
* Envía requests concurrentes durante **5 minutos**
* Mantiene suficiente carga para forzar el escalado
* Cada request tarda ~2 segundos (simulando procesamiento)

### 6.3. Observar el Escalado
Mientras el script corre:
* Abrir **App Runner Console** y ver el servicio
* Observar cómo el número de **Active instances** aumenta de 1 a 3
* Ir a **CloudWatch > Metrics** y buscar métricas de App Runner:
  - `ActiveInstances` - Instancias activas
  - `RequestCount` - Número de requests
  - `2xxStatusResponses` - Respuestas exitosas

### 6.4. Verificar Resultados
Después de la prueba:
* Las instancias deberían haber escalado a 3 durante la carga
* Después de unos minutos sin carga, volverán a 1 (scale down)

> **Evidencia de éxito:** CloudWatch muestra el aumento de instancias activas durante la prueba de carga.

---

## 🧹 Cleanup

**Objetivo:** Eliminar todos los recursos creados.

### 7.1. Eliminar Servicio de App Runner
* En App Runner Console, seleccionar el servicio y hacer clic en **Delete**.

### 7.2. Eliminar Imágenes de ECR
```bash
aws ecr batch-delete-image --repository-name edem-app --image-ids imageTag=latest --region <tu-region>
```

### 7.3. Eliminar Repositorio ECR
```bash
aws ecr delete-repository --repository-name edem-app --force --region <tu-region>
```

### 7.4. Eliminar IAM Role
* En IAM Console, eliminar el rol `AppRunnerECRAccessRole` si ya no es necesario.

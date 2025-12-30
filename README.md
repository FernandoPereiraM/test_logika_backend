
---

# 🚀 FastAPI Technical Test

Este proyecto es un backend desarrollado con **FastAPI**, usando **PostgreSQL en Docker**, **Alembic para migraciones** y **variables de entorno centralizadas**.

El entorno está pensado para levantarse fácilmente en desarrollo local.

---

## 📦 Requisitos previos

* **Python 3.10+**
* **Docker** y **Docker Compose**
* **Git**
* **Virtualenv**

---
## ⚡ Ejecución rápida (Windows)

Para Windows, el proyecto incluye un script que automatiza todo el flujo:

```bash
    inicializar.bat
```

Este script:

1. Levanta Docker
2. Espera a la base de datos
3. Aplica migraciones
4. Ejecuta el seed
5. Inicia el servidor FastAPI


## 📁 Estructura del proyecto (resumen)

```text
app/
api/ # routers / endpoints
core/ # configuración, seguridad, auth
db/ # sesión, conexión, migraciones
models/ # modelos SQLAlchemy
schemas/ # esquemas Pydantic
services/ # lógica de negocio
main.py
```

---

## ⚙️ Variables de entorno

El proyecto usa un archivo `.env` como **fuente única de configuración**, utilizado tanto por **FastAPI** como por **Docker Compose**.

### 1️⃣ Crear archivo `.env`

En la raíz del proyecto:

```bash
    .env
```

### 2️⃣ Contenido del `.env`

```env
# ==========================
# Base de Datos
# ==========================
DB_HOST=postgres
DB_PORT=5432
DB_NAME=technical_test
DB_USER=postgres
DB_PASSWORD=postgres

# ==========================
# Seguridad / JWT
# ==========================
SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256
```

📌 **Nota**

* `DB_HOST=postgres` corresponde al nombre del servicio en Docker Compose
* El archivo `.env` **no debe subirse al repositorio**

---

## 🐳 Base de Datos (Docker)

La base de datos PostgreSQL se levanta usando Docker Compose.

### Iniciar la base de datos

```bash
docker-compose up -d
```

Esto creará:

* Un contenedor PostgreSQL
* Un volumen persistente para los datos

La base de datos quedará disponible en:

```
localhost:5433
```

---

## 🐍 Entorno virtual de Python

### Crear entorno virtual

```bash
python -m venv env
```

### Activar entorno virtual

**Windows**

```bash
env\Scripts\activate
```

**Linux / Mac**

```bash
source env/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🧬 Migraciones de Base de Datos (Alembic)

### Aplicar migraciones

```bash
alembic upgrade head
```

Si es la primera vez:

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

---

## 🌱 Seed de datos iniciales

Para cargar datos de prueba:

```bash
python -m app.db.seed
```

Esto insertará datos básicos necesarios para pruebas y desarrollo.

---

## ▶️ Ejecutar el servidor FastAPI

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en:

* **API** → [http://localhost:8000](http://localhost:8000)
* **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔁 Flujo de ejecución resumido

```text
Docker → PostgreSQL → Alembic → Seed → FastAPI
```

Todo el proyecto utiliza el mismo archivo `.env`, garantizando coherencia entre infraestructura y backend.

---

## 🧠 Decisiones técnicas

* **FastAPI** por rendimiento y tipado
* **Docker** para aislar infraestructura
* **Alembic** para versionado del esquema
* **Pydantic Settings** para gestión de configuración
* **JWT** para autenticación

---

## 📌 Notas finales

* No se sube el archivo `.env`
* El proyecto está preparado para múltiples entornos
* La configuración está centralizada en `app/core/config.py`

---

## 👤 Autor

**Luis Pereira**
Backend / QA Engineer
Python · FastAPI · Docker · SQL

---
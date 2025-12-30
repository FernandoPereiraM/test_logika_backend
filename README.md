
---

# FastAPI Technical Test - Task API

Este proyecto es un backend desarrollado con **FastAPI**, usando **PostgreSQL en Docker**, **Alembic para migraciones** y **variables de entorno centralizadas**.

El entorno está pensado para levantarse fácilmente en desarrollo local.

**ABRIR LA CARPETA RAIZ & EJECUTAR EL SCRIPT**

---

## Requisitos previos

* **Python 3.10+**
* **Docker** y **Docker Compose**
* **Git**
* **Virtualenv**

---
## Ejecución rápida (Windows)

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


## Estructura del proyecto (resumen)

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

## Variables de entorno

El proyecto usa un archivo `.env` como **fuente única de configuración**, utilizado tanto por **FastAPI** como por **Docker Compose**.

### Crear archivo `.env`

En la raíz del proyecto:

```bash
    .env
```

### Contenido del `.env`

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

 **Nota**

* `DB_HOST=postgres` corresponde al nombre del servicio en Docker Compose
* El archivo `.env` **no debe subirse al repositorio**

---

## Base de Datos (Docker)

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

## Entorno virtual de Python

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

## Migraciones de Base de Datos (Alembic)

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

## Seed de datos iniciales

Para cargar datos de prueba:

```bash
python -m app.db.seed
```

Esto insertará datos básicos necesarios para pruebas y desarrollo.

---

## Ejecutar el servidor FastAPI

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en:

* **API** → [http://localhost:8000](http://localhost:8000)
* **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Flujo de ejecución resumido

```text
Docker → PostgreSQL → Alembic → Seed → FastAPI
```

Todo el proyecto utiliza el mismo archivo `.env`, garantizando coherencia entre infraestructura y backend.

---
#  Funcionamiento de la API.
---

##  Datos iniciales (Seed)

Durante la inicialización del proyecto se ejecuta un **script de seed**, cuyo objetivo es dejar el sistema listo para ser utilizado sin configuración manual.

### Usuario administrador inicial

Se crea automáticamente el siguiente usuario:

```text
Email:    admin@task.com
Password: admin
```

Este usuario se identifica por **email** y su contraseña se almacena de forma **hasheada** en la base de datos.

---

### Payload de autenticación

El siguiente payload puede utilizarse directamente en el endpoint de login para obtener un token JWT:

```json
{
  "email": "admin@task.com",
  "password": "admin"
}
```

**Endpoint:**

```http
POST /auth/login
```

---

### Datos adicionales creados

* Al usuario `admin@task.com` se le asocian automáticamente **6 tareas iniciales**
* Estas tareas se crean únicamente con fines de **desarrollo y prueba técnica**
* Permiten validar de inmediato los endpoints de Tasks sin crear datos manualmente

---

### Proceso de creación

1. El esquema de base de datos se crea mediante **Alembic**
2. Se ejecuta el seed:

   ```bash
   python -m app.db.seed
   ```
3. El script:

   * Verifica si el usuario ya existe
   * Crea el usuario administrador si no existe
   * Hashea la contraseña antes de guardarla
   * Inserta las tareas asociadas

---

### Nota de seguridad

Las credenciales iniciales están pensadas **exclusivamente para entornos de desarrollo o pruebas**.
En entornos productivos se recomienda cambiar o eliminar este usuario.

---

## Autenticación (Auth)

La API utiliza **JWT (Bearer Token)** para proteger los endpoints de tareas.

---

### Registrar usuario

**POST** `/auth/register`

#### Payload

```json
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

#### Descripción

* Crea un nuevo usuario
* El email debe ser único
* La contraseña se almacena hasheada

---

### Login

**POST** `/auth/login`

#### Payload

```json
{
  "email": "admin@task.com",
  "password": "admin"
}
```

#### Respuesta (ejemplo)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Uso del Token

Para acceder a los endpoints protegidos, se debe enviar el token en el header:

```http
Authorization: Bearer <access_token>
```

---

## Tasks API

Todos los endpoints de **Tasks** requieren autenticación.

---

### Crear tarea

**POST** `/tasks/`

#### Payload

```json
{
  "title": "Nueva tarea",
  "description": "Descripción de la tarea"
}
```

#### Descripción

* La tarea se asocia automáticamente al usuario autenticado

---

# 📘 Listar tareas (con paginación)

### `GET /tasks/`

Este endpoint devuelve las tareas del **usuario autenticado**, aplicando paginación mediante los parámetros `page` y `page_size`.

---

## 🔐 Autenticación

Requiere token JWT en el header:

```
Authorization: Bearer <token>
```

---

## 📥 Parámetros de consulta

| Parámetro   | Tipo | Por defecto | Descripción                                      |
| ----------- | ---- | ----------- | ------------------------------------------------ |
| `page`      | int  | 1           | Número de página a consultar. Debe ser ≥ 1.      |
| `page_size` | int  | 10          | Cantidad de elementos por página. Entre 1 y 100. |

---

## 📌 Descripción

* `page` indica **la página actual**.
* `page_size` indica **cuántos registros devuelve la API por página**.
* El backend convierte internamente estos parámetros a offset/limit.
* Además, la respuesta incluye:

  * `total` → total de tareas del usuario
  * `total_pages` → número de páginas disponibles
  * `next_page` → página siguiente (o `null`)
  * `prev_page` → página anterior (o `null`)
  * `items` → lista de tareas de la página actual

---

## 📤 Ejemplo de solicitud

```
GET http://127.0.0.1:8000/tasks/?page=1&page_size=5
```

---

## 📥 Ejemplo de respuesta

```json
{
  "total": 42,
  "page": 1,
  "page_size": 5,
  "total_pages": 9,
  "next_page": 2,
  "prev_page": null,
  "items": [
    {
      "id": 12,
      "title": "Pagar servicios",
      "description": "Antes del viernes",
      "status": 0,
      "created_at": "2025-01-01T10:00:00"
    }
  ]
}
```

---

## 🧠 ¿Cómo funciona la paginación internamente?

El backend convierte:

```
skip = (page - 1) * page_size
limit = page_size
```

Ejemplo para `page=3` y `page_size=10`:

* salta → `20` registros
* devuelve → `10` registros (IDs 21 al 30)

---

## 📎 Notas

* Solo se devuelven tareas del **usuario autenticado**.
* Si la página solicitada excede el número real de páginas, `items` será una lista vacía.
* `next_page` y `prev_page` son `null` cuando no aplican.

---

### Obtener tarea por ID

**GET** `/tasks/{task_id}`

#### Descripción

* Retorna la tarea si pertenece al usuario autenticado
* Si no existe o no es del usuario → `404`

---

### Actualizar tarea

**PUT** `/tasks/{task_id}`

#### Payload

```json
{
  "title": "Tarea actualizada",
  "description": "Descripción actualizada",
  "status": (0 = pending | 1 = in_progress | 2 = done)
}
```

#### Descripción

* Actualiza solo las tareas del usuario autenticado

---

### Eliminar tarea

**DELETE** `/tasks/{task_id}`

#### Descripción

* Elimina la tarea si pertenece al usuario autenticado

---

## Flujo típico de uso

```text
1. Login
2. Obtener JWT
3. Usar Authorization: Bearer <token>
4. Consumir endpoints de Tasks
```

---

## Notas técnicas

* El email es el identificador único del usuario
* JWT configurable mediante variables de entorno
* Passwords almacenados con hash seguro
* Acceso a tareas restringido por usuario
* El proyecto está preparado para múltiples entornos
* La configuración está centralizada en `app/core/config.py`
* La paginación está implementada a nivel de consulta, lo que permite manejar grandes volúmenes de datos de forma eficiente y controlada.

---

##  Autor

**Luis Pereira**
Backend / QA Engineer
---
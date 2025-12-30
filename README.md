---

# FastAPI Technical Test - Task API

Este proyecto es un backend desarrollado con FastAPI, usando PostgreSQL en Docker, Alembic para migraciones y variables de entorno centralizadas.

El entorno está preparado para levantarse fácilmente en desarrollo local.

Abrir la carpeta raíz y ejecutar el script.

---

# Requisitos previos

* Python 3.10<=3.11.8
* Docker y Docker Compose
* Git
* Virtualenv

---

# Ejecución rápida (Windows)

Para Windows, el proyecto incluye un script que automatiza todo el flujo:

```
inicializar.bat
```

Este script:

1. Levanta Docker
2. Espera a la base de datos
3. Aplica migraciones
4. Ejecuta el seed
5. Inicia el servidor FastAPI

---

# Estructura del proyecto (resumen)

```
app/
    api/          # Routers / endpoints
    core/         # Configuración, seguridad, auth
    db/           # Sesión, conexión, migraciones
    models/       # Modelos SQLAlchemy
    schemas/      # Esquemas Pydantic
    services/     # Lógica de negocio
main.py
```

---

# Variables de entorno

El proyecto usa un archivo `.env` como fuente única de configuración, utilizado tanto por FastAPI como por Docker Compose.

## Crear archivo `.env`

En la raíz del proyecto:

```
.env
```

## Contenido del archivo `.env`

```
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

Nota:

* `DB_HOST=postgres` corresponde al nombre del servicio en Docker Compose.
* El archivo `.env` no debe subirse al repositorio.

---

# Base de Datos (Docker)

La base de datos PostgreSQL se levanta usando Docker Compose.

## Iniciar la base de datos

```
docker-compose up -d
```

Esto creará:

* Un contenedor PostgreSQL
* Un volumen persistente para los datos

La base de datos estará disponible en:

```
localhost:5433
```

---

# Entorno virtual de Python

## Crear entorno virtual

```
python -m venv env
```

## Activar entorno virtual

Windows:

```
env\Scripts\activate
```

Linux / Mac:

```
source env/bin/activate
```

## Instalar dependencias

```
pip install -r requirements.txt
```

---

# Migraciones de Base de Datos (Alembic)

## Aplicar migraciones
Para crear tablas y cargar datos de prueba:

```

```
alembic upgrade head
---

---
# Ejecutar el servidor FastAPI

```
uvicorn app.main:app --reload
```

El servidor estará disponible en:

* API: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# Flujo de ejecución resumido

```
Docker → PostgreSQL → Alembic → FastAPI
```

Todo el proyecto utiliza el mismo archivo `.env`, garantizando coherencia entre infraestructura y backend.

---

# Funcionamiento de la API

---

# Datos iniciales (Seed)

Durante la inicialización del proyecto se ejecuta un script de **seed** cuyo objetivo es preparar completamente el sistema para su uso inmediato.

El script realiza automáticamente:

* **Ejecución de migraciones** para crear todas las tablas necesarias.
* **Creación de un usuario administrador inicial**.
* **Generación de un conjunto de tareas asociadas al usuario administrador**, útiles para pruebas y validación del funcionamiento.

## Usuario administrador inicial

El sistema crea automáticamente:

```
Email:    admin@task.com
Password: admin
```

La contraseña se almacena de forma hasheada.

## Payload de ejemplo para autenticación

```
POST /auth/login
```

```json
{
  "email": "admin@task.com",
  "password": "admin"
}
```

## Datos adicionales creados

* El usuario administrador recibe 30 tareas iniciales con distintos estados.
* Son útiles para validar el funcionamiento de los endpoints sin crear datos manuales.

## Proceso de creación

1. Alembic crea la estructura inicial.
2. El script de seed:

   * Verifica si el usuario ya existe
   * Crea el usuario administrador si no existe
   * Hashea la contraseña
   * Inserta las tareas asociadas

## Nota de seguridad

Estas credenciales son únicamente para desarrollo y pruebas.

---

# Autenticación (Auth)

La API utiliza JWT (Bearer Token) para proteger los endpoints de tareas.

---

# Registrar usuario

**POST** `/auth/register`

## Payload

```
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

El email debe ser único y la contraseña se almacena hasheada.

---

# Login

**POST** `/auth/login`

## Payload

```
{
  "email": "admin@task.com",
  "password": "admin"
}
```

## Respuesta de ejemplo

```
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

## Uso del Token

Todos los endpoints protegidos requieren:

```
Authorization: Bearer <access_token>
```

---

# Tasks API

Todos los endpoints de tareas requieren autenticación.

---

# Crear tarea

**POST** `/tasks/`

## Payload

```
{
  "title": "Nueva tarea",
  "description": "Descripción de la tarea"
}
```

La tarea se asocia automáticamente al usuario autenticado.

---

# Listar tareas (con paginación)

**GET** `/tasks/`

Este endpoint devuelve las tareas del usuario autenticado aplicando paginación mediante `page` y `page_size`.

## Autenticación requerida

```
Authorization: Bearer <token>
```

## Parámetros de consulta

| Parámetro | Tipo | Por defecto | Descripción                                |
| --------- | ---- | ----------- | ------------------------------------------ |
| page      | int  | 1           | Número de página solicitada. Debe ser ≥ 1. |
| page_size | int  | 10          | Cantidad de registros por página (1-100).  |

## Descripción

* `page` indica la página actual.
* `page_size` define cuántos elementos se devuelven por página.
* El backend convierte internamente los parámetros en `offset` y `limit`.
* La respuesta incluye:

  * total
  * total_pages
  * next_page
  * prev_page
  * items

## Ejemplo de solicitud

```
GET http://127.0.0.1:8000/tasks/?page=1&page_size=5
```

## Ejemplo de respuesta

```
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

# Obtener tarea por ID

**GET** `/tasks/{task_id}`

* Devuelve la tarea si pertenece al usuario autenticado.
* Si no existe o no pertenece al usuario, devuelve `404`.

---

# Actualizar tarea

**PUT** `/tasks/{task_id}`

## Payload

```
{
  "title": "Tarea actualizada",
  "description": "Descripción actualizada",
  "status": 0
}
```

Actualiza únicamente tareas pertenecientes al usuario autenticado.

---

# Eliminar tarea

**DELETE** `/tasks/{task_id}`

Elimina la tarea si pertenece al usuario autenticado.

---

# Flujo típico de uso

```
1. Login
2. Obtener JWT
3. Incluir Authorization: Bearer <token> en cada request
4. Consumir endpoints de Tasks
```

---

# Notas técnicas

* El email es el identificador único del usuario.
* Los JWT son configurables mediante variables de entorno.
* Las contraseñas se almacenan hasheadas.
* El acceso a tareas está restringido por usuario.
* El proyecto está preparado para múltiples entornos.
* La configuración está centralizada en `app/core/config.py`.
* La paginación está implementada a nivel de consulta para manejar grandes volúmenes de datos de forma eficiente.

---

# Autor

Luis Pereira
Backend / QA Engineer

---
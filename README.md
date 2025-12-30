---

# FastAPI Technical Test – Task API

Backend desarrollado con FastAPI, utilizando PostgreSQL en Docker, Alembic para migraciones y variables de entorno centralizadas.
El entorno está preparado para levantarse fácilmente en desarrollo local.

---

# Requisitos previos

* Python 3.10–3.11.8
* Docker y Docker Compose
* Git
* Virtualenv

---

# Ejecución rápida en Windows

El proyecto incluye un script que automatiza toda la inicialización:

```
inicializar.bat
```

El script realiza:

1. Inicio de contenedores Docker
2. Espera a que la base de datos esté disponible
3. Aplicación de migraciones
4. Ejecución del seed
5. Inicio del servidor FastAPI

---

# Estructura del proyecto

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

El proyecto utiliza un archivo `.env` como fuente única de configuración tanto para FastAPI como para Docker Compose.

## Crear archivo `.env`

Ubicado en la raíz del proyecto.

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

Notas:

* `DB_HOST=postgres` corresponde al nombre del servicio en docker-compose.
* El archivo `.env` no debe incluirse en el repositorio.

---

# Base de Datos (Docker)

La base de datos PostgreSQL se levanta mediante Docker Compose.

## Iniciar la base de datos

```
docker-compose up -d
```

Esto crea:

* Contenedor PostgreSQL
* Volumen persistente

La base de datos estará disponible en:

```
localhost:5433
```

---

# Entorno virtual de Python

## Crear entorno

```
python -m venv env
```

## Activar entorno

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

# Migraciones (Alembic)

## Aplicar migraciones

```
alembic upgrade head
```

---

# Ejecutar el servidor FastAPI

```
uvicorn app.main:app --reload
```

Accesos:

* API: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# Flujo de ejecución general

```
Docker → PostgreSQL → Alembic → FastAPI
```

Todo el proyecto utiliza el mismo archivo `.env` para garantizar coherencia.

---

# Datos iniciales (Seed)

El proyecto ejecuta un script de seed para dejar el sistema listo para uso inmediato.

El script:

* Aplica migraciones
* Crea un usuario administrador
* Inserta tareas iniciales asociadas a dicho usuario

## Usuario administrador inicial

```
Email:    admin@task.com
Password: admin
```

La contraseña se almacena hasheada.

### Payload de ejemplo para autenticación

```
POST /auth/login
```

```json
{
  "email": "admin@task.com",
  "password": "admin"
}
```

## Datos generados automáticamente

* 30 tareas iniciales asociadas al administrador
* Útiles para validar endpoints sin crear datos manuales

## Proceso del seed

1. Alembic crea la estructura
2. El seed:

   * Verifica si el usuario existe
   * Crea el usuario administrador si no existe
   * Hashea la contraseña
   * Inserta tareas de ejemplo

Nota: Estas credenciales son solo para desarrollo y pruebas.

---

# Autenticación (JWT)

La API utiliza JWT (Bearer Token) para proteger los endpoints de tareas.

---

# Registrar usuario

**POST** `/auth/register`

### Payload

```
{
  "email": "user@example.com",
  "password": "strong-password"
}
```

---

# Login

**POST** `/auth/login`

### Payload

```
{
  "email": "admin@task.com",
  "password": "admin"
}
```

### Respuesta

```
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

Para endpoints protegidos:

```
Authorization: Bearer <access_token>
```

---

# Tasks API

Todos los endpoints requieren autenticación.

---

## Crear tarea

**POST** `/tasks/`

### Payload

```
{
  "title": "Nueva tarea",
  "description": "Descripción de la tarea"
}
```

La tarea se asocia automáticamente al usuario autenticado.

---

## Listar tareas (paginación)

**GET** `/tasks/?page=1&page_size=10`

### Parámetros

| Parámetro | Tipo | Por defecto | Descripción              |
| --------- | ---- | ----------- | ------------------------ |
| page      | int  | 1           | Número de página         |
| page_size | int  | 10          | Tamaño de página (1–100) |

### Respuesta

Incluye: total, total_pages, next_page, prev_page, items.

Ejemplo:

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

## Obtener tarea por ID

**GET** `/tasks/{task_id}`

Devuelve la tarea si pertenece al usuario autenticado.
Si no existe o no pertenece, responde 404.

---

## Actualizar tarea

**PUT** `/tasks/{task_id}`

### Payload

```
{
  "title": "Tarea actualizada",
  "description": "Descripción actualizada",
  "status": 0
}
```

---

## Eliminar tarea

**DELETE** `/tasks/{task_id}`

Elimina la tarea si pertenece al usuario autenticado.

---

# Flujo típico de uso

```
1. Login
2. Obtener JWT
3. Enviar Authorization: Bearer <token>
4. Consumir endpoints de Tasks
```

---

# Notas técnicas

* El email es único por usuario.
* JWT configurable por variables de entorno.
* Contraseñas almacenadas con hashing seguro.
* Acceso a tareas restringido por usuario.
* Proyecto preparado para múltiples entornos.
* Configuración centralizada en `app/core/config.py`.
* Paginación implementada a nivel de consulta para eficiencia.

---

# Autor

Luis Pereira
Backend / QA Engineer

---

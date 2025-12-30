---

## 🧠 DECISIONES TÉCNICAS Y TRADE-OFFS

En esta sección se explican las principales decisiones técnicas tomadas durante el desarrollo del proyecto, junto con los **trade-offs** asociados.

---

### Identificación del usuario por email

**Decisión:**
El usuario se identifica de forma única por su **email**.

**Ventajas:**

* Evita ambigüedad de usernames
* Es estándar en APIs modernas
* Simplifica el flujo de autenticación

**Trade-off:**

* Cambiar el email implica actualizar la identidad del usuario
* No permite múltiples cuentas con el mismo correo

---

### Autenticación con JWT

**Decisión:**
Se implementó autenticación basada en **JWT (Bearer Token)**.

**Ventajas:**

* Stateless (no depende de sesión en servidor)
* Escalable y fácil de integrar con frontend
* Compatible con FastAPI de forma nativa

**Trade-off:**

* El token no puede invalidarse fácilmente antes de expirar
* Requiere manejo adecuado del `SECRET_KEY`

---

### Usuario y datos iniciales mediante Seed

**Decisión:**
El usuario administrador y las tareas iniciales se crean mediante un **script de seed**.

**Ventajas:**

* Permite probar la API sin configuración manual
* Garantiza consistencia entre entornos
* Facilita la evaluación técnica

**Trade-off:**

* Los datos no son dinámicos
* Debe evitarse en entornos productivos

---

### Migraciones con Alembic

**Decisión:**
Se utilizó **Alembic** para versionar el esquema de base de datos.

**Ventajas:**

* Control de versiones del esquema
* Compatible con SQLAlchemy
* Permite evolución controlada del modelo

**Trade-off:**

* Requiere disciplina para manejar migraciones
* Puede generar conflictos si se autogeneran sin revisión

---

### Uso de Docker solo para la base de datos

**Decisión:**
Docker se utiliza únicamente para PostgreSQL, mientras que FastAPI corre localmente.

**Ventajas:**

* Reduce complejidad
* Facilita debugging en desarrollo
* Menor tiempo de setup

**Trade-off:**

* No replica exactamente un entorno productivo
* Requiere coordinación entre host y contenedor

---

### Variables de entorno centralizadas

**Decisión:**
Toda la configuración se centralizó en un archivo `.env`, cargado desde `core`.

**Ventajas:**

* Evita hardcodear secretos
* Facilita cambio de entorno
* Configuración única para Docker y FastAPI

**Trade-off:**

* Requiere manejo cuidadoso del `.env`
* Dependencia de variables externas

---
### Paginación con `page` y `page_size`

**Decisión:**
La paginación del listado de tareas se implementa utilizando los parámetros `page` y `page_size`.

**Ventajas:**

* Es un enfoque intuitivo para el cliente, basado en navegación por páginas.
* Facilita generar enlaces como `next_page` y `prev_page`.
* Permite controlar fácilmente cuántos elementos se devuelven por solicitud.
* Compatible con SQLAlchemy mediante la conversión interna a `offset` y `limit`.

**Trade-off:**

* Internamente se deben calcular los valores `skip` y `limit`.
* Si los datos cambian entre solicitudes, el contenido de cada página puede variar.
* No es tan eficiente ni estable como la paginación basada en cursores para datasets muy grandes.
---

### Separación por capas (Core, DB, Routes)

**Decisión:**
El proyecto se estructuró por capas funcionales.

**Ventajas:**

* Código más mantenible
* Separación clara de responsabilidades
* Facilita testing y escalabilidad

**Trade-off:**

* Más archivos y estructura inicial
* Mayor curva de aprendizaje para proyectos pequeños

---

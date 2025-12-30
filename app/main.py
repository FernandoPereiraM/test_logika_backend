from fastapi import FastAPI
from app.api import auth, tasks

app = FastAPI(
    title="Technical Test API: TASK CRUD",
    description="""
API REST desarrollada con FastAPI.

Funcionalidades:
- Autenticación de usuarios (login)
- CRUD completo de tareas
- Persistencia con PostgreSQL
- Migraciones con Alembic

La documentación interactiva está disponible automáticamente.
""",
    version="1.0.0",
)

# Rutas
app.include_router(auth.router, tags=["Auth"])
app.include_router(tasks.router, tags=["Tasks"])


@app.on_event("startup")
async def startup_event():
    print("🚀 API iniciada correctamente")
    print("📘 Swagger UI → http://localhost:8000/docs")

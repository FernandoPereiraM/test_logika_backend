from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

revision = "847036d72cca"
down_revision = "0e9bca78f8fe"

def upgrade():
    tasks_table = table(
        "tasks",
        column("title", sa.String),
        column("description", sa.Text),
        column("status", sa.Integer),
        column("user_id", sa.Integer),
    )

    # Admin tiene ID 1 por ser el primer usuario insertado
    op.bulk_insert(
        tasks_table,
        [
            {"title": "Tarea 1", "description": "Preparar informe mensual", "status": 0, "user_id": 1},
            {"title": "Tarea 2", "description": "Revisar correo pendiente", "status": 1, "user_id": 1},
            {"title": "Tarea 3", "description": "Actualización del sistema", "status": 2, "user_id": 1},
            {"title": "Tarea 4", "description": "Planificar reunión semanal", "status": 0, "user_id": 1},
            {"title": "Tarea 5", "description": "Organizar documentos", "status": 1, "user_id": 1},
            {"title": "Tarea 6", "description": "Realizar respaldo de datos", "status": 2, "user_id": 1},
            {"title": "Tarea 7", "description": "Actualizar inventario", "status": 0, "user_id": 1},
            {"title": "Tarea 8", "description": "Documentar proceso de trabajo", "status": 1, "user_id": 1},
            {"title": "Tarea 9", "description": "Revisión de métricas semanales", "status": 2, "user_id": 1},
            {"title": "Tarea 10", "description": "Preparar presentación", "status": 0, "user_id": 1},
            {"title": "Tarea 11", "description": "Optimizar base de datos", "status": 1, "user_id": 1},
            {"title": "Tarea 12", "description": "Atender solicitudes internas", "status": 2, "user_id": 1},
            {"title": "Tarea 13", "description": "Configurar nuevo servidor", "status": 0, "user_id": 1},
            {"title": "Tarea 14", "description": "Limpiar archivos temporales", "status": 1, "user_id": 1},
            {"title": "Tarea 15", "description": "Actualizar dependencias del proyecto", "status": 2, "user_id": 1},
            {"title": "Tarea 16", "description": "Verificar logs del sistema", "status": 0, "user_id": 1},
            {"title": "Tarea 17", "description": "Crear scripts de automatización", "status": 1, "user_id": 1},
            {"title": "Tarea 18", "description": "Revisar niveles de seguridad", "status": 2, "user_id": 1},
            {"title": "Tarea 19", "description": "Modificar configuración de red", "status": 0, "user_id": 1},
            {"title": "Tarea 20", "description": "Evaluar rendimiento del servidor", "status": 1, "user_id": 1},
            {"title": "Tarea 21", "description": "Crear manual de usuario", "status": 2, "user_id": 1},
            {"title": "Tarea 22", "description": "Revisión de endpoints API", "status": 0, "user_id": 1},
            {"title": "Tarea 23", "description": "Depurar errores del sistema", "status": 1, "user_id": 1},
            {"title": "Tarea 24", "description": "Configurar entorno de pruebas", "status": 2, "user_id": 1},
            {"title": "Tarea 25", "description": "Evaluar nuevas herramientas", "status": 0, "user_id": 1},
            {"title": "Tarea 26", "description": "Migrar base de datos", "status": 1, "user_id": 1},
            {"title": "Tarea 27", "description": "Crear dashboards analíticos", "status": 2, "user_id": 1},
            {"title": "Tarea 28", "description": "Reorganizar estructura del proyecto", "status": 0, "user_id": 1},
            {"title": "Tarea 29", "description": "Revisar accesos de usuarios", "status": 1, "user_id": 1},
            {"title": "Tarea 30", "description": "Implementar mejoras de rendimiento", "status": 2, "user_id": 1},
        ]
    )

def downgrade():
    op.execute("DELETE FROM tasks WHERE user_id = 1")

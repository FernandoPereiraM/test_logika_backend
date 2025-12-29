from app.db.session import SessionLocal
from app.services.user_service import create_user  # Tus funciones actuales
from app.models.task import Task
from app.models.user import User

def seed_data():
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == "admin@task.com").first()
        if not existing_user:
            user = create_user(db, email="admin@task.com", password="admin")
            print(f"Usuario creado: {user.email}")
        else:
            user = existing_user

        #Añadir tareas masivas
        new_tasks = [
            Task(title="Lectura del Proyecto", description="Ninguna", user_id=user.id),
            Task(title="Migrar BD", description="Ejecutar alembic upgrade", user_id=user.id),
            Task(title="Crud Completo", description="Instalar dependencias", user_id=user.id),
            Task(title="Tests", description="Ejecutar tests", user_id=user.id),
            Task(title="Configurar proyecto", description="Instalar dependencias", user_id=user.id),
            Task(title="Feedback", description="En Espera", user_id=user.id),
        ]
        db.add_all(new_tasks)
        db.commit()
        print("Tareas añadidas exitosamente.")
        
    except Exception as e:
        print(f"Error en el seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
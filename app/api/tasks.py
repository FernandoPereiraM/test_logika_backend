from fastapi import APIRouter, Depends, HTTPException, status, Query,  Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.session import get_db
from app.models.user import User
from app.core.config import settings
from app.schemas.task import TaskCreate, TaskPaginationOut, TaskUpdate, TaskOut
from app.services import task_service

# En Swagger aparecerán bajo la sección "Tasks"
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# tokenUrl apunta al endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# OBTENER USUARIO AUTENTICADO
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        # Decodifica el token JWT usando la clave secreta
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


#CREATE
@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Crea la tarea asociada al usuario autenticado
    return task_service.create_task(
        db,
        task_in,
        current_user.id,
    )

# LIST TASKS (PAGINADO)
@router.get("/", response_model=TaskPaginationOut)
def list_tasks(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    # Obtiene las tareas paginadas desde el service
    data = task_service.get_tasks(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )

    # Función auxiliar para construir URLs
    def build_url(page_number: int | None):
        if page_number is None:
            return None
        return str(
            request.url.include_query_params(
                page=page_number,
                page_size=page_size,
            )
        )

    # Se agregan las URLs de navegación
    data["next_page_url"] = build_url(data["next_page"])
    data["prev_page_url"] = build_url(data["prev_page"])

    return data



# GET BY ID
@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Busca la tarea asegurando que pertenezca al usuario
    task = task_service.get_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# UPDATE
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Busca la tarea del usuario
    task = task_service.get_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_service.update_task(
        db=db,
        task=task,
        task_in=task_in,
    )


# DELETE
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_service.delete_task(db=db, task=task)

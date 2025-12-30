from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_in: TaskCreate, user_id: int) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        user_id=user_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, user_id: int, page: int, page_size: int):

    #page/page_size
    skip = (page - 1) * page_size
    limit = page_size

    query = db.query(Task).filter(Task.user_id == user_id)

    total = query.count()

    items = (
        query.order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Calcular total de páginas
    total_pages = (total + page_size - 1) // page_size

    # Calcular next/prev page
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "next_page": next_page,
        "prev_page": prev_page,
        "items": items,
    }



def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()


def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    if task_in.title is not None:
        task.title = task_in.title

    if task_in.description is not None:
        task.description = task_in.description

    if task_in.status is not None:
        task.status = task_in.status

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()

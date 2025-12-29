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

def get_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
):
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

def update_task(
    db: Session,
    task: Task,
    task_in: TaskUpdate,
) -> Task:
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

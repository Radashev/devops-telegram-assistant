from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_db
from app.repositories.postgres.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.user import UserCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_telegram_id(x_telegram_id: int = Header(...)) -> int:
    return x_telegram_id


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Depends(get_telegram_id),
):
    user_repo = UserRepository(db)
    task_repo = TaskRepository()

    user = await user_repo.get_or_create(
        UserCreate(
            telegram_id=telegram_id,
            username=None,
            first_name=None,
            last_name=None,
            email=None,
        )
    )

    data = task.model_dump()
    data["user_id"] = user.id

    return await task_repo.create(db, data)


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Depends(get_telegram_id),
):
    user_repo = UserRepository(db)
    task_repo = TaskRepository()

    user = await user_repo.get_by_telegram_id(telegram_id)
    if not user:
        return []

    return await task_repo.get_all(db, user.id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Depends(get_telegram_id),
):
    user_repo = UserRepository(db)
    task_repo = TaskRepository()

    user = await user_repo.get_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = await task_repo.update(
        db=db,
        task_id=task_id,
        user_id=user.id,
        data=task.model_dump(exclude_unset=True),
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    telegram_id: int = Depends(get_telegram_id),
):
    user_repo = UserRepository(db)
    task_repo = TaskRepository()

    user = await user_repo.get_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = await task_repo.delete(
        db=db,
        task_id=task_id,
        user_id=user.id,
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"status": "deleted"}
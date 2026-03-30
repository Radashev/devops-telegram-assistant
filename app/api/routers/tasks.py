from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskCreate, TaskResponse
from app.repositories.task_repository import TaskRepository
from app.db.postgres import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await TaskRepository.create(
        db,
        {
            "title": task.title,
            "description": task.description,
            "user_id": 1,
            "is_done": False
        }
    )


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await TaskRepository.get_all(db)

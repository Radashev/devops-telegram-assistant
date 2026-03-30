from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    @staticmethod
    async def create(db: AsyncSession, task_data: dict) -> Task:
        task = Task(**task_data)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Task]:
        result = await db.execute(select(Task).order_by(Task.id))
        return list(result.scalars().all())
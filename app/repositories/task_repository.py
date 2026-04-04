from sqlalchemy import delete, select, update
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
    async def get_all(db: AsyncSession, user_id: int) -> list[Task]:
        result = await db.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, task_id: int) -> Task | None:
        result = await db.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        task_id: int,
        user_id: int,
        data: dict,
    ) -> Task | None:
        stmt = (
            update(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
            .values(**data)
            .returning(Task)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(
        db: AsyncSession,
        task_id: int,
        user_id: int,
    ) -> bool:
        stmt = (
            delete(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0
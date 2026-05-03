from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reminder import Reminder


class ReminderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        title: str,
        day_of_month: int | None,
        is_last_day: bool,
    ) -> Reminder:
        reminder = Reminder(
            user_id=user_id,
            title=title,
            day_of_month=day_of_month,
            is_last_day=is_last_day,
            is_active=True,
        )
        self.session.add(reminder)
        await self.session.commit()
        await self.session.refresh(reminder)
        return reminder

    async def get_all_by_user_id(self, user_id: int) -> list[Reminder]:
        result = await self.session.execute(
            select(Reminder)
            .where(Reminder.user_id == user_id)
            .order_by(Reminder.id.asc())
        )
        return list(result.scalars().all())

    async def get_by_id_and_user_id(
        self,
        reminder_id: int,
        user_id: int,
    ) -> Reminder | None:
        result = await self.session.execute(
            select(Reminder).where(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def delete_by_id_and_user_id(
        self,
        reminder_id: int,
        user_id: int,
    ) -> bool:
        reminder = await self.get_by_id_and_user_id(reminder_id, user_id)
        if reminder is None:
            return False

        await self.session.delete(reminder)
        await self.session.commit()
        return True

    async def get_active(self) -> list[Reminder]:
        result = await self.session.execute(
            select(Reminder)
            .where(Reminder.is_active.is_(True))
            .order_by(Reminder.id.asc())
        )
        return list(result.scalars().all())

    async def mark_triggered(self, reminder_id: int, triggered_at: datetime) -> None:
        reminder = await self.session.get(Reminder, reminder_id)

        if reminder is None:
            return

        reminder.last_triggered_at = triggered_at
        await self.session.commit()
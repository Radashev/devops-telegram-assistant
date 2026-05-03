import calendar
from datetime import date, datetime

from app.repositories.reminder_repository import ReminderRepository


class ReminderService:
    def __init__(self, reminder_repository: ReminderRepository):
        self.reminder_repository = reminder_repository

    def parse_day_of_month(self, raw_day: str) -> tuple[int | None, bool]:
        raw_day = raw_day.strip().lower()

        if raw_day == "last":
            return None, True

        if not raw_day.isdigit():
            raise ValueError("Day must be a number from 1 to 31 or 'last'.")

        day = int(raw_day)

        if day < 1 or day > 31:
            raise ValueError("Day must be between 1 and 31.")

        return day, False

    def is_due_today(self, reminder, today: date) -> bool:
        if reminder.is_last_day:
            last_day = calendar.monthrange(today.year, today.month)[1]
            return today.day == last_day

        return reminder.day_of_month == today.day

    def was_triggered_today(self, reminder, today: date) -> bool:
        if reminder.last_triggered_at is None:
            return False

        return reminder.last_triggered_at.date() == today

    async def get_due_reminders(self, today: date):
        reminders = await self.reminder_repository.get_active()

        due = []

        for reminder in reminders:
            if not self.is_due_today(reminder, today):
                continue

            if self.was_triggered_today(reminder, today):
                continue

            due.append(reminder)

        return due

    async def mark_triggered(self, reminder_id: int, triggered_at: datetime) -> None:
        await self.reminder_repository.mark_triggered(
            reminder_id=reminder_id,
            triggered_at=triggered_at,
        )

    async def create_monthly_reminder(
        self,
        user_id: int,
        raw_day: str,
        title: str,
    ):
        if not title.strip():
            raise ValueError("Reminder title cannot be empty.")

        day_of_month, is_last_day = self.parse_day_of_month(raw_day)

        return await self.reminder_repository.create(
            user_id=user_id,
            title=title.strip(),
            day_of_month=day_of_month,
            is_last_day=is_last_day,
        )

    async def get_user_reminders(self, user_id: int):
        return await self.reminder_repository.get_all_by_user_id(user_id)

    async def delete_reminder(self, reminder_id: int, user_id: int) -> bool:
        return await self.reminder_repository.delete_by_id_and_user_id(
            reminder_id=reminder_id,
            user_id=user_id,
        )

import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Bot

from app.db.postgres import AsyncSessionLocal
from app.repositories.reminder_repository import ReminderRepository
from app.repositories.postgres.user_repository import UserRepository
from app.services.reminder_service import ReminderService


TIMEZONE = ZoneInfo("Europe/Warsaw")


async def run_reminder_scheduler(bot: Bot) -> None:
    print("✅ Reminder scheduler started", flush=True)
    while True:
        try:
            now = datetime.now(TIMEZONE)
            today = now.date()

            async with AsyncSessionLocal() as session:
                reminder_repository = ReminderRepository(session)
                user_repository = UserRepository(session)
                reminder_service = ReminderService(reminder_repository)

                due_reminders = await reminder_service.get_due_reminders(today)
                print(f"⏰ Scheduler tick: now={now}, today={today}", flush=True)
                print(f"📌 Due reminders found: {len(due_reminders)}", flush=True)

                for reminder in due_reminders:
                    user = await user_repository.get_by_id(reminder.user_id)

                    if user is None:
                        continue

                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"🔔 Нагадування:\n\n{reminder.title}",
                    )

                    await reminder_service.mark_triggered(
                        reminder_id=reminder.id,
                        triggered_at=now,
                    )


        except Exception:

            import traceback

            traceback.print_exc()

        await asyncio.sleep(30)
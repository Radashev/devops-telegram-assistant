from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.postgres import AsyncSessionLocal
from app.repositories.reminder_repository import ReminderRepository
from app.repositories.postgres.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.reminder_service import ReminderService

router = Router()


async def get_or_create_db_user_id(telegram_user, session) -> int:
    user_repo = UserRepository(session)

    payload = UserCreate(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
    )

    user = await user_repo.get_or_create(payload)
    return user.id


@router.message(Command("remind_monthly"))
async def remind_monthly_handler(message: Message) -> None:
    if not message.text:
        await message.answer("❌ Порожня команда.")
        return

    parts = message.text.strip().split(maxsplit=2)

    if len(parts) < 3:
        await message.answer(
            "Формат:\n"
            "/remind_monthly 9 Заплатити за житло\n"
            "/remind_monthly last Передати показники лічильників"
        )
        return

    _, raw_day, title = parts

    async with AsyncSessionLocal() as session:
        try:
            user_id = await get_or_create_db_user_id(message.from_user, session)

            reminder_repo = ReminderRepository(session)
            reminder_service = ReminderService(reminder_repo)

            reminder = await reminder_service.create_monthly_reminder(
                user_id=user_id,
                raw_day=raw_day,
                title=title,
            )

            day_text = "last" if reminder.is_last_day else str(reminder.day_of_month)

            await message.answer(
                f"✅ Нагадування створено\n"
                f"ID: {reminder.id}\n"
                f"Day: {day_text}\n"
                f"Text: {reminder.title}"
            )

        except ValueError as e:
            await message.answer(f"❌ {e}")
        except Exception:
            await message.answer("❌ Помилка при створенні нагадування.")
            raise


@router.message(Command("reminders"))
async def list_reminders_handler(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user_id = await get_or_create_db_user_id(message.from_user, session)

        reminder_repo = ReminderRepository(session)
        reminder_service = ReminderService(reminder_repo)

        reminders = await reminder_service.get_user_reminders(user_id)

        if not reminders:
            await message.answer("У тебе ще немає нагадувань.")
            return

        lines = ["📌 Твої щомісячні нагадування:\n"]

        for reminder in reminders:
            day_text = "last" if reminder.is_last_day else str(reminder.day_of_month)
            status = "active" if reminder.is_active else "inactive"

            lines.append(
                f"ID: {reminder.id} | day: {day_text} | {status}\n"
                f"— {reminder.title}"
            )

        await message.answer("\n\n".join(lines))


@router.message(Command("delete_reminder"))
async def delete_reminder_handler(message: Message) -> None:
    if not message.text:
        await message.answer("❌ Порожня команда.")
        return

    parts = message.text.strip().split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Формат:\n/delete_reminder 2")
        return

    raw_id = parts[1].strip()

    if not raw_id.isdigit():
        await message.answer("❌ ID має бути числом.")
        return

    reminder_id = int(raw_id)

    async with AsyncSessionLocal() as session:
        user_id = await get_or_create_db_user_id(message.from_user, session)

        reminder_repo = ReminderRepository(session)
        reminder_service = ReminderService(reminder_repo)

        deleted = await reminder_service.delete_reminder(
            reminder_id=reminder_id,
            user_id=user_id,
        )

        if not deleted:
            await message.answer("❌ Нагадування не знайдено.")
            return

        await message.answer(f"✅ Нагадування {reminder_id} видалено.")
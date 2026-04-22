import aiohttp
from aiogram import Router, types
from aiogram.filters import Command

from app.core.config import settings
from app.services.email_cache import email_cache

router = Router()

API_URL = f"{settings.bot_api_base_url}/tasks/"


def build_headers(message: types.Message) -> dict:
    return {
        "x-telegram-id": str(message.from_user.id),
    }


@router.message(Command("emails_to_tasks"))
async def emails_to_tasks_handler(message: types.Message):
    cached = email_cache.get()

    if not cached:
        await message.answer("❌ Немає даних. Спочатку виконай /triage_batch")
        return

    headers = build_headers(message)
    created = 0

    async with aiohttp.ClientSession() as session:
        for email, result in cached:
            if result.priority not in ["urgent", "important"]:
                continue

            payload = {
                "title": result.summary,
                "description": f"{email.subject} | {email.from_email}",
            }

            async with session.post(API_URL, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    created += 1

    await message.answer(f"✅ Створено задач: {created}")

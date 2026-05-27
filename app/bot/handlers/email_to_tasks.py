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


def should_create_task(summary: str, subject: str, sender: str) -> bool:
    text = f"{summary} {subject} {sender}".lower()

    positive_keywords = [
        "interview",
        "job offer",
        "vacancy",
        "recruiter",
        "application",
        "apply",
        "position",
        "engineer role",
        "devops engineer",
        "platform engineer",
        "backend python",
        "action required",
        "deadline",
    ]

    negative_keywords = [
        "weekly summary",
        "weekly job offers",
        "newsletter",
        "discount",
        "promotion",
        "free trial",
        "transaction",
        "top-up",
        "order confirmation",
        "payment",
        "profile views",
        "job alert",
    ]

    if any(word in text for word in negative_keywords):
        return False

    if any(word in text for word in positive_keywords):
        return True

    return False


def build_task_title(summary: str) -> str:
    return f"Review: {summary}".strip()


@router.message(Command("emails_to_tasks"))
async def emails_to_tasks_handler(message: types.Message):
    cached = email_cache.get()

    if not cached:
        await message.answer(
            "❌ Немає даних. Спочатку виконай /check_emails або /triage_batch"
        )
        return

    headers = build_headers(message)
    created = 0
    skipped = 0

    async with aiohttp.ClientSession() as session:
        for email, result in cached:
            if result.priority not in ["urgent", "important"]:
                skipped += 1
                continue

            summary = result.summary or ""
            subject = email.subject or ""
            sender = email.from_email or ""

            if not should_create_task(summary, subject, sender):
                skipped += 1
                continue

            payload = {
                "title": build_task_title(summary),
                "description": f"Subject: {subject}\nFrom: {sender}",
            }

            async with session.post(API_URL, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    created += 1
                else:
                    text = await resp.text()
                    await message.answer(f"❌ Error while creating task: {text}")

    await message.answer(
        f"✅ Створено задач: {created}\n"
        f"⏭ Пропущено email: {skipped}"
    )

from aiogram import Router, types
from aiogram.filters import Command
from html import escape

from app.services.email_cache import email_cache
from app.services.gmail_service import GmailService

router = Router()


@router.message(Command("archive_preview"))
async def archive_preview_handler(message: types.Message):
    cached = email_cache.get()

    if not cached:
        await message.answer(
            "❌ Немає даних. Спочатку виконай /check_emails або /triage_batch"
        )
        return

    ignore_items = [
        (email, result)
        for email, result in cached
        if result.priority == "ignore"
    ]

    if not ignore_items:
        await message.answer("✅ Немає email для архівації.")
        return

    lines = ["📦 <b>Emails suggested for archive</b>\n"]

    for index, (email, result) in enumerate(ignore_items, start=1):
        summary = escape(result.summary or "")
        from_email = escape(email.from_email or "")
        subject = escape(email.subject or "")

        lines.append(
            f"{index}. {summary}\n"
            f"   From: {from_email}\n"
            f"   Subject: {subject}"
        )

    lines.append("")
    lines.append("👉 Якщо все ок, наступним кроком зробимо /archive_confirm")

    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("archive_confirm"))
async def archive_confirm_handler(message: types.Message):
    cached = email_cache.get()

    if not cached:
        await message.answer(
            "❌ Немає даних. Спочатку виконай /check_emails або /triage_batch"
        )
        return

    ignore_items = [
        (email, result)
        for email, result in cached
        if result.priority == "ignore"
    ]

    if not ignore_items:
        await message.answer("✅ Немає email для архівації.")
        return

    gmail = GmailService()
    archived_count = 0

    for email, result in ignore_items:
        if not email.id:
            continue

        gmail.archive_message(email.id)
        archived_count += 1

    await message.answer(f"✅ Архівовано email: {archived_count}")
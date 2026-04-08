import html
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command

from app.services.google_calendar_service import GoogleCalendarService

router = Router()


@router.message(Command("gcal"))
async def create_calendar_event(message: types.Message):
    try:
        _, date_str, time_str, *event_text = (message.text or "").split()
        summary = " ".join(event_text).strip()
        start_dt = datetime.strptime(
            f"{date_str} {time_str}",
            "%Y-%m-%d %H:%M",
        )

        if not summary:
            raise ValueError("empty summary")
    except Exception:
        await message.answer(
            "❗ Формат неправильний\n"
            "Приклад:\n"
            "<code>/gcal 2026-02-01 20:30 Зустріч</code>",
            parse_mode="HTML",
        )
        return

    service = GoogleCalendarService()

    try:
        event = await service.create_event(
            start_dt=start_dt,
            summary=summary,
        )
    except Exception as e:
        await message.answer(
            f"⚠️ Помилка Google Calendar:\n<code>{html.escape(str(e))}</code>",
            parse_mode="HTML",
        )
        return

    await message.answer(
        "📅 Подію додано в Google Calendar!\n\n"
        f"📝 <b>{html.escape(event.summary)}</b>\n"
        f"⏰ {html.escape(event.start_time)}\n\n"
        f"🔗 <a href='{html.escape(event.html_link)}'>Відкрити в календарі</a>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
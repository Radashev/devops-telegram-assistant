from aiogram import Router, types
from aiogram.filters import Command

from app.services.gmail_service import GmailService
from app.schemas.email_triage import EmailInput
from app.services.email_agent_service import EmailTriageAgentService
from app.services.email_cache import email_cache

router = Router()


@router.message(Command("check_emails"))
async def check_emails_handler(message: types.Message):
    gmail = GmailService()
    agent = EmailTriageAgentService()

    raw_emails = gmail.fetch_messages(max_results=20)

    emails = [
        EmailInput(
            id=e["id"],
            from_email=e["from"],
            subject=e["subject"],
            snippet=e["snippet"],
        )
        for e in raw_emails
    ]

    results = await agent.triage_batch(emails)
    email_cache.set(results)

    urgent = []
    important = []
    ignore = []

    for email, result in results:
        if result.priority == "urgent":
            urgent.append(result.summary)
        elif result.priority == "important":
            important.append(result.summary)
        else:
            ignore.append(result.summary)

    text = "📩 <b>Email summary</b>\n\n"

    if urgent:
        text += "🔴 URGENT:\n" + "\n".join(f"• {x}" for x in urgent) + "\n\n"

    if important:
        text += "🟡 IMPORTANT:\n" + "\n".join(f"• {x}" for x in important) + "\n\n"

    if ignore:
        text += "⚪ IGNORE:\n" + "\n".join(f"• {x}" for x in ignore)

    await message.answer(text, parse_mode="HTML")

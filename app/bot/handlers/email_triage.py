from aiogram import Router, types
from aiogram.filters import Command

from collections import defaultdict
from app.schemas.email_triage import EmailInput
from app.services.email_agent_service import EmailTriageAgentService
from app.services.email_cache import email_cache

router = Router()


@router.message(Command("triage_email"))
async def triage_email_handler(message: types.Message):
    if not message.text:
        await message.answer(
            "Формат:\n"
            "/triage_email from@example.com | Subject | Snippet"
        )
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await message.answer(
            "Формат:\n"
            "/triage_email from@example.com | Subject | Snippet"
        )
        return

    payload = parts[1].strip()
    segments = [segment.strip() for segment in payload.split("|")]

    if len(segments) < 3:
        await message.answer(
            "Формат:\n"
            "/triage_email from@example.com | Subject | Snippet"
        )
        return

    from_email, subject, snippet = segments[0], segments[1], segments[2]

    email_input = EmailInput(
        from_email=from_email,
        subject=subject,
        snippet=snippet,
    )

    service = EmailTriageAgentService()

    try:
        result = await service.triage_email(email_input)

        priority_map = {
            "urgent": "🔴 URGENT",
            "important": "🟡 IMPORTANT",
            "can_wait": "🔵 CAN WAIT",
            "ignore": "⚪ IGNORE",
        }

        priority_text = priority_map.get(result.priority, result.priority)

        text = (
            "📩 <b>Email triage result</b>\n\n"
            f"Priority: <b>{priority_text}</b>\n"
            f"Reply required: <b>{'yes' if result.reply_required else 'no'}</b>\n"
            f"Summary: {result.summary}\n"
            f"Reason: {result.reason}"
        )

        await message.answer(text, parse_mode="HTML")

    except ValueError as e:
        await message.answer(f"❌ {e}")
    except Exception:
        await message.answer("❌ Помилка під час аналізу email.")
        raise


@router.message(Command("triage_batch"))
async def triage_batch_handler(message: types.Message):
    """
    Формат:
    /triage_batch
    from1@example.com | Subject 1 | Snippet 1
    ---
    from2@example.com | Subject 2 | Snippet 2
    ---
    from3@example.com | Subject 3 | Snippet 3
    """
    if not message.text:
        await message.answer(
            "Формат:\n"
            "/triage_batch\n"
            "from1@example.com | Subject 1 | Snippet 1\n"
            "---\n"
            "from2@example.com | Subject 2 | Snippet 2"
        )
        return

    parts = message.text.split("\n", maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await message.answer(
            "Формат:\n"
            "/triage_batch\n"
            "from1@example.com | Subject 1 | Snippet 1\n"
            "---\n"
            "from2@example.com | Subject 2 | Snippet 2"
        )
        return

    raw_batch = parts[1].strip()
    raw_items = [item.strip() for item in raw_batch.split("---") if item.strip()]

    emails: list[EmailInput] = []

    for item in raw_items:
        segments = [segment.strip() for segment in item.split("|")]

        if len(segments) < 3:
            await message.answer(
                "❌ Один із email блоків має неправильний формат.\n\n"
                "Правильно:\n"
                "from@example.com | Subject | Snippet"
            )
            return

        from_email, subject, snippet = segments[0], segments[1], segments[2]

        emails.append(
            EmailInput(
                from_email=from_email,
                subject=subject,
                snippet=snippet,
            )
        )

    if not emails:
        await message.answer("❌ Немає email для аналізу.")
        return

    service = EmailTriageAgentService()

    try:
        batch_results = await service.triage_batch(emails)

        grouped: dict[str, list[tuple[EmailInput, str, bool]]] = defaultdict(list)

        for email, result in batch_results:
            grouped[result.priority].append(
                (email, result.summary, result.reply_required)
            )
        email_cache.set(batch_results)

        priority_order = ["urgent", "important", "can_wait", "ignore"]
        priority_titles = {
            "urgent": "🔴 URGENT",
            "important": "🟡 IMPORTANT",
            "can_wait": "🔵 CAN WAIT",
            "ignore": "⚪ IGNORE",
        }

        lines = ["📩 <b>Email batch triage</b>\n"]

        for priority in priority_order:
            items = grouped.get(priority, [])
            if not items:
                continue

            lines.append(f"{priority_titles[priority]} ({len(items)})")

            for email, summary, reply_required in items:
                reply_mark = " [reply]" if reply_required else ""
                lines.append(f"• {summary}{reply_mark}")

            lines.append("")

        lines.append("👉 Suggested actions only. No emails will be deleted without your confirmation.")

        await message.answer("\n".join(lines), parse_mode="HTML")

    except ValueError as e:
        await message.answer(f"❌ {e}")
    except Exception:
        await message.answer("❌ Помилка під час batch-аналізу email.")
        raise
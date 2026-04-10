from aiogram import Router, types
from aiogram.filters import Command

router = Router()


HELP_UA = """
ℹ️ <b>DevOps Telegram Assistant</b>

👋 <b>/start</b>
Запуск бота

📋 <b>/list</b>
Показати задачі

➕ <b>/add текст</b>
Додати задачу

✅ <b>/done номер</b>
Позначити як виконану

🗑 <b>/delete номер</b>
Видалити задачу

📅 <b>/gcal YYYY-MM-DD HH:MM текст</b>
Додати подію в Google Calendar


🌐 English version: /help_en
"""


HELP_EN = """
ℹ️ <b>DevOps Telegram Assistant</b>

👋 <b>/start</b>
Start the bot

📋 <b>/list</b>
Show your tasks

➕ <b>/add text</b>
Add a new task

✅ <b>/done number</b>
Mark task as done

🗑 <b>/delete number</b>
Delete a task

📅 <b>/gcal YYYY-MM-DD HH:MM text</b>
Create Google Calendar event


🌐 Українська: /help
"""


@router.message(Command("help"))
async def help_ua(message: types.Message):
    await message.answer(
        HELP_UA,
        parse_mode="HTML",
    )


@router.message(Command("help_en"))
async def help_en(message: types.Message):
    await message.answer(
        HELP_EN,
        parse_mode="HTML",
    )
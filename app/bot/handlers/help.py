from aiogram import Router, types
from aiogram.filters import Command

router = Router()


HELP_UA = """
ℹ️ <b>DevOps Telegram Assistant</b>

👋 <b>/start</b>
Запуск бота

<b>📋 Tasks</b>

📋 <b>/list</b>
Показати задачі

➕ <b>/add текст</b>
Додати задачу

✅ <b>/done номер</b>
Позначити задачу як виконану

🗑 <b>/delete номер</b>
Видалити задачу

<b>🔁 Monthly reminders</b>

🔁 <b>/remind_monthly 9 текст</b>
Створити щомісячне нагадування на 9 число

🔁 <b>/remind_monthly last текст</b>
Створити нагадування на останній день місяця

📌 <b>/reminders</b>
Показати всі щомісячні нагадування

🗑 <b>/delete_reminder ID</b>
Видалити нагадування за ID

<b>📅 Google Calendar</b>

📅 <b>/gcal YYYY-MM-DD HH:MM текст</b>
Додати подію в Google Calendar

🌐 English version: <b>/help_en</b>
"""


HELP_EN = """
ℹ️ <b>DevOps Telegram Assistant</b>

👋 <b>/start</b>
Start the bot

<b>📋 Tasks</b>

📋 <b>/list</b>
Show your tasks

➕ <b>/add text</b>
Add a new task

✅ <b>/done number</b>
Mark task as done

🗑 <b>/delete number</b>
Delete a task

<b>🔁 Monthly reminders</b>

🔁 <b>/remind_monthly 9 text</b>
Create a monthly reminder for the 9th day

🔁 <b>/remind_monthly last text</b>
Create a reminder for the last day of the month

📌 <b>/reminders</b>
Show all monthly reminders

🗑 <b>/delete_reminder ID</b>
Delete a reminder by ID

<b>📅 Google Calendar</b>

📅 <b>/gcal YYYY-MM-DD HH:MM text</b>
Create a Google Calendar event

🌐 Українська: <b>/help</b>
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
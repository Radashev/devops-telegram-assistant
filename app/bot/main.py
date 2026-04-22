import os
import asyncio
import app.models
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.bot.handlers.tasks import router as tasks_router
from app.bot.handlers.calendar import router as calendar_router
from app.bot.handlers.help import router as help_router
from app.bot.handlers.reminders import router as reminders_router
from app.bot.handlers.task_planner import router as task_planner_router
from app.bot.handlers.email_triage import router as email_triage_router
from app.bot.handlers.email_to_tasks import router as email_to_tasks_router
from app.bot.handlers.email_fetch import router as email_fetch_router
from app.bot.handlers.email_archive import router as email_archive_router


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(tasks_router)
dp.include_router(calendar_router)
dp.include_router(help_router)
dp.include_router(reminders_router)
dp.include_router(task_planner_router)
dp.include_router(email_triage_router)
dp.include_router(email_to_tasks_router)
dp.include_router(email_fetch_router)
dp.include_router(email_archive_router)


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Bot is running 🚀")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

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


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Bot is running 🚀")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

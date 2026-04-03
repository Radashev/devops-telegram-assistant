import aiohttp
from aiogram import Router, types

router = Router()

API_URL = "http://api:8000/tasks/"


@router.message(lambda m: m.text.startswith("/add"))
async def add_task(message: types.Message):
    parts = message.text.split(" ", 1)

    if len(parts) < 2:
        await message.answer("Формат: /add task text")
        return

    title = parts[1]

    payload = {
        "title": title,
        "description": None
    }

    headers = {
        "x-telegram-id": str(message.from_user.id)
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload, headers=headers) as resp:
            if resp.status == 200:
                await message.answer("Task created ✅")
            else:
                text = await resp.text()
                await message.answer(f"Error: {text}")


@router.message(lambda m: m.text and m.text.startswith("/list"))
async def list_tasks(message: types.Message):
    headers = {
        "x-telegram-id": str(message.from_user.id),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as resp:
            if resp.status != 200:
                await message.answer("Error fetching tasks")
                return

            tasks = await resp.json()

            if not tasks:
                await message.answer("No tasks yet")
                return

            text = "\n".join(
                [f"{t['id']}. {t['title']}" for t in tasks]
            )

            await message.answer(text)
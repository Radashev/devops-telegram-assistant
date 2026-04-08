import aiohttp
from aiogram import Router, types
from app.core.config import settings

router = Router()

API_URL = f"{settings.bot_api_base_url}/tasks/"


def build_headers(message: types.Message) -> dict:
    return {
        "x-telegram-id": str(message.from_user.id),
    }


async def fetch_tasks(message: types.Message) -> list[dict] | None:
    headers = build_headers(message)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as resp:
            if resp.status != 200:
                await message.answer("Error fetching tasks")
                return None

            return await resp.json()


def resolve_task_by_number(tasks: list[dict], number_str: str) -> dict | None:
    if not number_str.isdigit():
        return None

    number = int(number_str)

    if number < 1 or number > len(tasks):
        return None

    return tasks[number - 1]


@router.message(lambda m: m.text and m.text.startswith("/add"))
async def add_task(message: types.Message):
    parts = message.text.split(" ", 1)

    if len(parts) < 2:
        await message.answer("Формат: /add task text")
        return

    title = parts[1].strip()

    if not title:
        await message.answer("Формат: /add task text")
        return

    payload = {
        "title": title,
        "description": None,
    }

    headers = build_headers(message)

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload, headers=headers) as resp:
            if resp.status == 200:
                await message.answer("Task created ✅")
            else:
                text = await resp.text()
                await message.answer(f"Error: {text}")


@router.message(lambda m: m.text and m.text.startswith("/list"))
async def list_tasks(message: types.Message):
    tasks = await fetch_tasks(message)

    if tasks is None:
        return

    if not tasks:
        await message.answer("No tasks yet")
        return

    text = "\n".join(
        [
            f"{index}. {'✅' if task['is_done'] else '❌'} {task['title']}"
            for index, task in enumerate(tasks, start=1)
        ]
    )

    await message.answer(text)


@router.message(lambda m: m.text and m.text.startswith("/done"))
async def done_task(message: types.Message):
    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("Формат: /done <number>")
        return

    tasks = await fetch_tasks(message)
    if tasks is None:
        return

    if not tasks:
        await message.answer("No tasks yet")
        return

    selected_task = resolve_task_by_number(tasks, parts[1])

    if not selected_task:
        await message.answer("Task number not found")
        return

    real_task_id = selected_task["id"]

    headers = build_headers(message)
    payload = {"is_done": True}
    url = f"{API_URL}{real_task_id}"

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                await message.answer("Task done ✅")
            else:
                text = await resp.text()
                await message.answer(f"Error: {text}")


@router.message(lambda m: m.text and m.text.startswith("/delete"))
async def delete_task(message: types.Message):
    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("Формат: /delete <number>")
        return

    tasks = await fetch_tasks(message)
    if tasks is None:
        return

    if not tasks:
        await message.answer("No tasks yet")
        return

    selected_task = resolve_task_by_number(tasks, parts[1])

    if not selected_task:
        await message.answer("Task number not found")
        return

    real_task_id = selected_task["id"]

    headers = build_headers(message)
    url = f"{API_URL}{real_task_id}"

    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as resp:
            if resp.status == 200:
                await message.answer("Task deleted 🗑️")
            else:
                text = await resp.text()
                await message.answer(f"Error: {text}")
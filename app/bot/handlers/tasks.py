import aiohttp
from aiogram import Router, types
from aiogram.filters import Command

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


@router.message(Command("add"))
async def add_task(message: types.Message):
    if not message.text:
        await message.answer("Формат: /add task text")
        return

    parts = message.text.split(maxsplit=1)

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


def parse_task_numbers(raw_args: str) -> list[int]:
    numbers: set[int] = set()

    parts = raw_args.split()

    for part in parts:
        if "-" in part:
            start_str, end_str = part.split("-", 1)

            if not start_str.isdigit() or not end_str.isdigit():
                continue

            start = int(start_str)
            end = int(end_str)

            if start > end:
                continue

            numbers.update(range(start, end + 1))
        else:
            if part.isdigit():
                numbers.add(int(part))

    return sorted(numbers)


@router.message(Command("list"))
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


@router.message(Command("done"))
async def done_task(message: types.Message):
    if not message.text:
        await message.answer("Формат: /done <number>")
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Формат: /done <number>")
        return

    task_number = parts[1].strip()

    tasks = await fetch_tasks(message)
    if tasks is None:
        return

    if not tasks:
        await message.answer("No tasks yet")
        return

    selected_task = resolve_task_by_number(tasks, task_number)

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


@router.message(Command("delete"))
async def delete_task(message: types.Message):
    if not message.text:
        await message.answer("Формат: /delete <number> або /delete 1 2 3 або /delete 1-5")
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Формат: /delete <number> або /delete 1 2 3 або /delete 1-5")
        return

    task_numbers = parse_task_numbers(parts[1])

    if not task_numbers:
        await message.answer("Task number not found")
        return

    tasks = await fetch_tasks(message)
    if tasks is None:
        return

    if not tasks:
        await message.answer("No tasks yet")
        return

    selected_tasks = []

    for number in task_numbers:
        selected_task = resolve_task_by_number(tasks, str(number))
        if selected_task:
            selected_tasks.append(selected_task)

    if not selected_tasks:
        await message.answer("Task number not found")
        return

    headers = build_headers(message)

    deleted = 0
    failed = 0

    async with aiohttp.ClientSession() as session:
        for task in selected_tasks:
            real_task_id = task["id"]
            url = f"{API_URL}{real_task_id}"

            async with session.delete(url, headers=headers) as resp:
                if resp.status == 200:
                    deleted += 1
                else:
                    failed += 1

    await message.answer(
        f"🗑 Видалено задач: {deleted}\n"
        f"❌ Помилок: {failed}"
    )


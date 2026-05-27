from aiogram import Router, types
from aiogram.filters import Command

from app.services.agent_service import TaskPlanningAgentService

router = Router()


@router.message(Command("plan_tasks"))
async def plan_tasks_handler(message: types.Message):
    if not message.text:
        await message.answer("Формат: /plan_tasks <goal>")
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[1].strip():
        await message.answer("Формат: /plan_tasks <goal>")
        return

    goal = parts[1].strip()
    agent_service = TaskPlanningAgentService()

    try:
        tasks = await agent_service.plan_tasks(goal)

        if not tasks:
            await message.answer("❌ AI не зміг згенерувати план задач.")
            return

        formatted = "\n".join(
            [f"{index}. {task}" for index, task in enumerate(tasks, start=1)]
        )

        await message.answer(
            f"🧠 <b>AI Task Plan</b>\n\n{formatted}",
            parse_mode="HTML",
        )

        await message.answer(
            "👉 Хочеш створити ці задачі в системі? Поки що вручну через /add."
        )

    except ValueError as e:
        await message.answer(f"❌ {e}")
    except Exception:
        await message.answer("❌ Помилка під час генерації плану задач.")
        raise
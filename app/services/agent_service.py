import re

from app.bot.llm import call_llm


class TaskPlanningAgentService:
    async def plan_tasks(self, goal: str) -> list[str]:
        goal = goal.strip()

        if not goal:
            raise ValueError("Goal cannot be empty.")

        prompt = self._build_prompt(goal)
        raw_response = await call_llm(prompt)
        tasks = self._parse_tasks(raw_response)

        if not tasks:
            raise ValueError("The agent could not generate tasks.")

        return tasks

    def _build_prompt(self, goal: str) -> str:
        return f"""
You are a Task Planning Agent for a DevOps Telegram Assistant.

Your job is to convert a user's goal into a short list of practical, actionable implementation tasks.

Context:
- The project uses FastAPI, aiogram, PostgreSQL, SQLAlchemy async, Alembic, Docker
- The project follows a clean structure with handlers, services, repositories, models
- The result should fit a backend/Telegram bot development workflow

Rules:
- Return 5 to 7 tasks maximum
- Each task must be short, concrete, and implementation-focused
- Prefer tasks like: create model, add migration, implement service, add handler, test flow
- Do not suggest frontend or UI unless the goal explicitly asks for it
- Do not explain anything
- Do not add intro text
- Do not add conclusion
- Return only the task list
- One task per line

Goal: {goal}
""".strip()

    def _parse_tasks(self, raw_response: str) -> list[str]:
        lines = raw_response.splitlines()
        cleaned_tasks: list[str] = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Прибираємо нумерацію або маркери:
            # "1. ", "2) ", "- ", "* "
            line = re.sub(r"^(\d+[\.\)]\s*|[-*]\s*)", "", line).strip()

            if line:
                cleaned_tasks.append(line)

        # Захист від занадто довгого списку
        return cleaned_tasks[:7]
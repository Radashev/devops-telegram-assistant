from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, payload: UserCreate) -> User:
        user = User(**payload.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_or_create(self, payload: UserCreate) -> User:
        existing = await self.get_by_telegram_id(payload.telegram_id)
        if existing:
            return existing
        return await self.create(payload)

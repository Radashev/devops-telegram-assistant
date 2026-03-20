from app.models.user import User
from app.repositories.postgres.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_telegram_user(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        payload = UserCreate(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        return await self.user_repository.get_or_create(payload)

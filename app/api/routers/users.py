from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_db
from app.repositories.postgres.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.usecases.user_usecase import UserUseCase

router = APIRouter(prefix="/users", tags=["users"])


def get_user_usecase(session: AsyncSession = Depends(get_db)) -> UserUseCase:
    repository = UserRepository(session)
    return UserUseCase(repository)


@router.post("/", response_model=UserRead)
async def create_user(
    payload: UserCreate,
    user_usecase: UserUseCase = Depends(get_user_usecase),
):
    return await user_usecase.register_telegram_user(
        telegram_id=payload.telegram_id,
        username=payload.username,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )


@router.get("/", response_model=list[UserRead])
async def get_users(
    user_usecase: UserUseCase = Depends(get_user_usecase),
):
    return await user_usecase.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    user_usecase: UserUseCase = Depends(get_user_usecase),
):
    user = await user_usecase.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
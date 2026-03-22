from fastapi import FastAPI

from app.api.routers.users import router as users_router

app = FastAPI(title="DevOps Telegram Assistant")


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users_router)

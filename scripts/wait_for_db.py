import asyncio
import os
import asyncpg


async def main():
    database_url = os.environ["DATABASE_URL"]

    # 🔥 FIX: asyncpg не розуміє "+asyncpg"
    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    for attempt in range(30):
        try:
            conn = await asyncpg.connect(database_url)
            await conn.execute("SELECT 1")
            await conn.close()
            print("✅ Database is ready")
            return
        except Exception as e:
            print(f"⏳ Waiting for DB... {attempt + 1}/30: {e}")
            await asyncio.sleep(2)

    raise RuntimeError("❌ DB not ready after waiting")


asyncio.run(main())
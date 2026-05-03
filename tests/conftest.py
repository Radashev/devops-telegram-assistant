import os
import sys
from pathlib import Path


# 👉 FIX imports
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# 👉 FIX env variables для Settings
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/test_db",
)

os.environ.setdefault("BOT_TOKEN", "test_bot_token")
os.environ.setdefault("OPENAI_API_KEY", "test_openai_key")

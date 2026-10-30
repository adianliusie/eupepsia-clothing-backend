import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Local dev loads .env from the repo root. In Lambda, env vars come from the SAM template.
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Settings(BaseSettings):
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "")
    DB_NAME: str = os.environ.get("DB_NAME", "eupepsia-dev")


settings = Settings()

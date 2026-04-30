from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "industrial-rca-agent")
    app_env: str = os.getenv("APP_ENV", "dev")
    auto_reset_max_retry: int = int(os.getenv("AUTO_RESET_MAX_RETRY", "1"))


settings = Settings()

from typing import Literal, Optional

import dotenv
import typer
from pydantic import BaseSettings

app_dir = typer.get_app_dir("y42")


class Settings(BaseSettings):
    class Config:
        validate_all = True
        validate_assignment = True

    Y42_API_KEY: Optional[str] = None
    Y42_ENVIRONMENT: Literal["dev"] | Literal["prod"] = "prod"
    Y42_ROOT_DIR: str = app_dir

    @property
    def Y42_BASE_URL(self) -> str:
        return f"https://api.{self.Y42_ENVIRONMENT}.y42.dev"

    # Set this variable if you plan on setting up a Space with BigQuery
    Y42_GOOGLE_CLOUD_SECRET: Optional[str]


res = dotenv.load_dotenv()
cli_settings = Settings()

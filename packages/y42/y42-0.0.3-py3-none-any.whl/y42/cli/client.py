import httpx

from y42.cli.settings import cli_settings
from y42.clients.y42 import Y42

y42_client = Y42(
    client=httpx.AsyncClient(),
    base_url=cli_settings.Y42_BASE_URL,
    y42_root_dir=cli_settings.Y42_ROOT_DIR,
    api_key=cli_settings.Y42_API_KEY,
)


def reinit_client():
    y42_client.base_url = cli_settings.Y42_BASE_URL
    y42_client.y42_root_dir = cli_settings.Y42_ROOT_DIR
    y42_client.api_key = cli_settings.Y42_API_KEY

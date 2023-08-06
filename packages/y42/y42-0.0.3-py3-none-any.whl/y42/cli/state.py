import json
import os

from pydantic import BaseModel

from y42.cli.settings import cli_settings
from y42.models.company import Company
from y42.models.space import Space

STATE_DIR = os.path.join(cli_settings.Y42_ROOT_DIR, ".y42_state")


class _AppState(BaseModel):
    class Config:
        validate_assignment = True

    known_companies: dict[str, Company] = {}  # company slug -> Company
    known_spaces: dict[str, dict[str, Space]] = {}  # co_slug -> space name -> Space
    active_company: str | None = None  # slug
    space_dirs: dict[str, str] = {}  # space ID -> absolute path

    @classmethod
    def load(cls) -> "_AppState":
        if not os.path.exists(cli_settings.Y42_ROOT_DIR):
            os.makedirs(cli_settings.Y42_ROOT_DIR)
            print(f"Created Y42 root directory {cli_settings.Y42_ROOT_DIR}")

        if not os.path.exists(STATE_DIR):
            res = _AppState()
            res.reset()
            print(f"Initialized app state in {STATE_DIR}.")
            return res

        with open(STATE_DIR, "r") as inf:
            try:
                res = _AppState(**json.load(inf))
            except Exception as e:
                choice = input(
                    f"State could not be loaded from {STATE_DIR}. Reset state? [Y, n]"
                )
                if not choice.strip() or choice.strip().lower() == "y":
                    res = _AppState()
                    res.reset()
                else:
                    raise e

            return res

    def reset(self):
        self.known_companies: dict[str, Company] = {}  # company slug -> Company
        self.known_spaces: dict[
            str, dict[str, Space]
        ] = {}  # co_slug -> space name -> Space
        self.active_company: str | None = None  # slug
        self.space_dirs: dict[str, str] = {}  # space ID -> absolute path
        self.persist()
        print(f"(Re-)initialized Y42 state in {STATE_DIR}")

    def persist(self):
        with open(STATE_DIR, "w") as outf:
            outf.write(self.json(indent=4, by_alias=True))


_state = None


def get_state():
    global _state
    if _state is None:
        _state = _AppState.load()
    return _state

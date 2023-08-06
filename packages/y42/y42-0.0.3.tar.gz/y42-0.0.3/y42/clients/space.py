import json
import logging
import os
import uuid

from y42.api import APIClient
from y42.models.space import Space, SpaceUpdate
from y42.models.util import GoogleCloudSecret

log = logging.getLogger(__name__)

GIT_COMMANDS = {
    "clone",
    "init",
    "add",
    "mv",
    "restore",
    "rm",
    "bisect",
    "diff",
    "grep",
    "log",
    "show",
    "status",
    "branch",
    "commit",
    "merge",
    "rebase",
    "reset",
    "switch",
    "tag",
    "fetch",
    "pull",
    "push",
}


def is_clone(git_cmd) -> bool:
    for word in git_cmd:
        if word == "clone":
            return True
        if word.startswith("-"):
            continue
        elif word in GIT_COMMANDS:
            break
    return False


class SpaceClient(APIClient):
    def __init__(
        self,
        company_id: str,
        space_id: uuid.UUID,
        optional_repo_dir: str | None = None,
        **kwargs,
    ):
        super(SpaceClient, self).__init__(**kwargs)
        self.company_id = company_id
        self.space_id = space_id
        self.repo_dir = optional_repo_dir or str(space_id)

    @property
    def git_url(self) -> str:
        return f"{self.base_url}/gateway/companies/{self.company_id}/spaces/{self.space_id}/git"

    @property
    def git_path_options(self):
        return f"--git-dir={os.path.join(self.repo_dir, '.git')} --work-tree={self.repo_dir}"

    @property
    def git_authorization_options(self):
        return f'-c http.extraHeader="Authorization: Bearer {self.api_key}"'

    @property
    def git_clone_cmd(self):
        return (
            f"git {self.git_authorization_options} clone {self.git_url} {self.repo_dir}"
        )

    @property
    def git_cmd_in_repo_path_str(self):
        return f"git {self.git_path_options} {self.git_authorization_options}"

    @property
    def git_cmd_str(self):
        return f"git {self.git_authorization_options}"

    @property
    def is_cloned(self):
        return os.path.exists(os.path.join(self.repo_dir, ".git"))

    async def get_details(self) -> Space:
        space_res = await self.client.get(
            f"/gateway/companies/{self.company_id}/spaces/{self.space_id}"
        )
        space_res.raise_for_status()
        space = Space(**space_res.json()["space_details"])
        return space

    async def update(self, space_update: SpaceUpdate) -> bool:
        res = await self.client.post(
            f"/gateway/companies/{self.company_id}/spaces/{self.space_id}",
            json=space_update.json(),
        )
        res.raise_for_status()
        return True

    async def delete(self) -> bool:
        res = await self.client.delete(
            f"/gateway/companies/{self.company_id}/spaces/{self.space_id}"
        )
        res.raise_for_status()
        return True

    async def setup_bigquery(
        self,
        bucket_name: str,
        dataset_name: str,
        location: str,
        secret: GoogleCloudSecret | str,
        update_secret: bool = False,
    ) -> Space | None:
        if isinstance(secret, str):
            secret = GoogleCloudSecret(**json.loads(secret))
        res = await self.client.post(
            f"/gateway/companies/{self.company_id}/spaces/{self.space_id}/setup/bigquery",
            params={"update": update_secret},
            json={
                "bucket_name": bucket_name,
                "dataset_name": dataset_name,
                "location": location,
                "secret": secret.dict(by_alias=True),
            },
        )
        res.raise_for_status()
        return (
            await self.get_details()
        )  # TODO not sure if this extra request is worth it

    async def clone(self) -> tuple[bytes, bytes]:
        if not os.path.exists(self.repo_dir):
            log.info(f"Creating directory {self.repo_dir} for space {self.space_id}")
            os.makedirs(self.repo_dir)

        if self.is_cloned:
            log.info(
                f"Repository at {self.repo_dir} appears to be cloned already, doing nothing."
            )
            return b"", b""

        stdout, stderr = await self.run_shell(self.git_clone_cmd)
        log.info(f"Cloned repository for space {self.space_id} to {self.repo_dir}")
        return stdout, stderr

    async def git_cmd(
        self, args: list[str], run_in_repo_path: bool = False
    ) -> tuple[bytes, bytes]:
        # run_in_repo_path can be used to safely run git commands in different spaces simultaneously without cd-ing
        if is_clone(args):
            raise ValueError(
                f"clone operations should be done via the {self.__class__.__name__}.clone(...) method"
            )

        if run_in_repo_path:
            use_git_cmd = self.git_cmd_in_repo_path_str
        else:
            use_git_cmd = self.git_cmd_str

        stdout, stderr = await self.run_shell(" ".join([use_git_cmd, *args]))
        return stdout, stderr

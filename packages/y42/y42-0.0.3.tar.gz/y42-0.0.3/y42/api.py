import asyncio
import logging
import uuid

import httpx

log = logging.getLogger(__name__)


class APIClient(object):
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        y42_root_dir: str | None = None,
        init_from: "APIClient | None" = None,
        **kwargs_for_httpx_client,
    ):
        self.api_key = api_key
        self._base_url = base_url
        self.y42_root_dir = y42_root_dir

        if client is not None and not isinstance(client, httpx.AsyncClient):
            raise ValueError("client must be httpx.AsyncClient")

        self._client = client
        if self._client is not None and self.base_url is not None:
            self._client.base_url = httpx.URL(self.base_url)
        self._kwargs_for_httpx_client = kwargs_for_httpx_client or {}
        if init_from:
            self._init_from(other_client=init_from)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

        if self._client is not None and self.base_url is not None:
            self._client.base_url = httpx.URL(self.base_url)

    def _init_from(self, other_client: "APIClient") -> None:
        self.api_key = other_client.api_key
        self.base_url = other_client.base_url
        self._client = other_client._client
        self.y42_root_dir = other_client.y42_root_dir

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise ValueError(
                "No HTTP client is set. "
                "Either supply an httpx.AsyncClient instance in the constructor, "
                f"or use this {self.__class__.__name__} object as an async contextmanager."
            )
        self._client.headers.update(
            self.make_headers()  # set default headers, more will be added by different methods
        )
        return self._client

    def make_headers(
        self, space_id: uuid.UUID | None = None, branch: str | None = None
    ) -> dict:
        headers = {}
        if self.api_key is not None:
            headers["authorization"] = f"Bearer {self.api_key}"
        if space_id is not None:
            headers["x-storage-id"] = str(space_id)
        if branch is not None:
            headers["x-storage-branch"] = branch
        return headers

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url, **self._kwargs_for_httpx_client
        )
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.__aexit__()
        self._client = None

    async def run_shell(self, cmd) -> tuple[bytes, bytes]:
        cleaned = (
            cmd
            if self.api_key not in cmd
            else cmd.replace(self.api_key, "**************")
        )
        log.debug(f"$ {cleaned}")
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        log.debug(stdout)
        log.debug(stderr)
        if proc.returncode != 0:
            raise RuntimeError(
                f"Shell command `{cleaned}` finished with code {proc.returncode}. "
                f"stderr output:\n\n{stderr.decode('utf-8')}\n"
                f"stdout output:\n\n{stdout.decode('utf-8')}"
            )
        return stdout, stderr

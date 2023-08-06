import logging

from y42.api import APIClient
from y42.models.company import Company

log = logging.getLogger(__name__)


class Y42(APIClient):
    async def get_companies(self) -> list[Company]:
        res = await self.client.get("/gateway/companies")
        res.raise_for_status()
        return [Company(**company_dict) for company_dict in res.json()["data"]]

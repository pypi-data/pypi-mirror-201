import uuid

from y42.api import APIClient
from y42.models.space import Space


class CompanyClient(APIClient):
    def __init__(self, company_id: str, **kwargs):
        super(CompanyClient, self).__init__(**kwargs)
        self.company_id = company_id

    async def get_spaces(self) -> list[Space]:
        res = await self.client.get(f"/gateway/companies/{self.company_id}/spaces/")
        res.raise_for_status()
        return [Space(**space_dict) for space_dict in res.json()["spaces"]]

    async def create_space(self, space_name: str) -> Space:
        # Create the actual space, unfortunately this does not return the details
        created = await self.client.post(
            f"/gateway/companies/{self.company_id}/spaces/new",
            json={"space_name": space_name},
        )
        created.raise_for_status()
        space_id = uuid.UUID(created.json()["space_id"])
        # Grab the space details separately, so that we can return an actual Space object
        space_res = await self.client.get(
            f"/gateway/companies/{self.company_id}/spaces/{str(space_id)}"
        )
        space_res.raise_for_status()
        return Space(**space_res.json()["space_details"])

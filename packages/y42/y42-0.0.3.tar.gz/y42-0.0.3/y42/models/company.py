import datetime

from pydantic import BaseModel, Field


class Company(BaseModel):
    company_id: str = Field(alias="id")
    slug: str
    name: str
    created_at: datetime.datetime
    requires_2fa_since: bool | None = Field(alias="2fa_required_since")
    email_structure: str | None
    is_trial: bool
    force_sso: bool

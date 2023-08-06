import datetime
import uuid
from typing import Literal

from pydantic import BaseModel, Field

from y42.clients.y42 import APIClient


class Bucket(BaseModel):
    name: str
    project_id: str
    type_: Literal["google_cloud_storage"] | Literal["amazon_s3"] | Literal[
        "azure_blob_storage"
    ] = Field(alias="type")


class Database(BaseModel):
    name: str
    project_id: str
    type_: Literal["bigquery"] | Literal["snowflake"] = Field(alias="type")


class DataWarehouse(BaseModel):
    bucket: Bucket | dict
    database: Database | dict


class Space(BaseModel, APIClient):
    space_id: uuid.UUID = Field(alias="id")
    name: str = Field(alias="space_name")
    repo_name: str
    repo_full_name: str
    company_id: str
    secret_id: uuid.UUID | None
    data_warehouse: DataWarehouse | None
    public_schema_name: str | None
    is_default: bool
    job_retention_time_minutes: int
    created_at: datetime.date | None = None
    updated_at: datetime.date | None = None


class SpaceUpdate(BaseModel):
    is_default: bool | None = None
    name: str | None = None
    job_retention_time_minutes: int | None = None

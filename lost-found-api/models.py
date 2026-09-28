from enum import Enum

from sqlmodel import SQLModel, Field
from pydantic import field_validator


class ItemStatus(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus

    @field_validator(
        "title",
        "description",
        "category",
        "location",
        "reported_by"
    )
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Field must not be empty")

        if len(value.strip()) < 3:
            raise ValueError("Field must contain meaningful text")

        return value.strip()
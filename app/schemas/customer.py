from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerBaseSchema(BaseModel):
    customer_number: str = Field(min_length=3, max_length=30)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    phone: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = None
    address: str | None = None
    notes: str | None = None

    @field_validator("customer_number", "first_name", "last_name", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        if not value or not str(value).strip():
            raise ValueError("Pflichtfeld darf nicht leer sein.")
        return str(value).strip()


class CustomerCreateSchema(CustomerBaseSchema):
    pass


class CustomerUpdateSchema(CustomerBaseSchema):
    pass


class CustomerReadSchema(CustomerBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

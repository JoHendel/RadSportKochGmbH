from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.enums import ProductCategory


class ProductBaseSchema(BaseModel):
    article_number: str = Field(min_length=3, max_length=30)
    name: str = Field(min_length=2, max_length=150)
    category: ProductCategory
    description: str | None = None
    purchase_price: Decimal = Field(gt=Decimal("0"))
    sale_price: Decimal = Field(gt=Decimal("0"))
    stock_quantity: int = Field(ge=0)
    minimum_stock: int = Field(ge=0)
    is_active: bool = True

    @field_validator("article_number", "name", mode="before")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        if not value or not str(value).strip():
            raise ValueError("Pflichtfeld darf nicht leer sein.")
        return str(value).strip()

    @model_validator(mode="after")
    def validate_prices(self) -> "ProductBaseSchema":
        # Der Verkaufspreis darf unter dem Einkaufspreis liegen, wenn bewusst
        # rabattiert wird. Extremwerte werden trotzdem früh abgefangen.
        if self.purchase_price > Decimal("999999") or self.sale_price > Decimal("999999"):
            raise ValueError("Preis liegt außerhalb des zulässigen Bereichs.")
        return self


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductUpdateSchema(ProductBaseSchema):
    pass


class ProductReadSchema(ProductBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

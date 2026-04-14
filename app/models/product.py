from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, Enum, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ProductCategory
from app.database.base import Base
from app.models.mixins import TimestampMixin


class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_number: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    category: Mapped[ProductCategory] = mapped_column(Enum(ProductCategory), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    minimum_stock: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    order_items = relationship("OrderItem", back_populates="product")

    @property
    def is_low_stock(self) -> bool:
        return self.stock_quantity <= self.minimum_stock

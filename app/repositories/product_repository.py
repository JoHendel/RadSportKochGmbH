from __future__ import annotations

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.core.enums import ProductCategory
from app.models.product import Product


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, search: str = "", category: ProductCategory | None = None, active_only: bool | None = None) -> list[Product]:
        statement = select(Product).order_by(Product.name.asc())

        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(
                    Product.article_number.ilike(pattern),
                    Product.name.ilike(pattern),
                    Product.description.ilike(pattern),
                )
            )
        if category is not None:
            filters.append(Product.category == category)
        if active_only is not None:
            filters.append(Product.is_active == active_only)

        if filters:
            statement = statement.where(and_(*filters))
        return list(self.session.scalars(statement).all())

    def low_stock(self) -> list[Product]:
        statement = select(Product).where(Product.stock_quantity <= Product.minimum_stock).order_by(Product.stock_quantity.asc())
        return list(self.session.scalars(statement).all())

    def get(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.flush()
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)

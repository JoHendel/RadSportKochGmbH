from __future__ import annotations

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.enums import ProductCategory
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema
from app.services.exceptions import EntityNotFoundError, ValidationServiceError


class ProductService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = ProductRepository(session)

    def list_products(
        self,
        search: str = "",
        category: ProductCategory | None = None,
        active_only: bool | None = None,
    ) -> list[Product]:
        return self.repository.list(search=search, category=category, active_only=active_only)

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get(product_id)
        if not product:
            raise EntityNotFoundError("Artikel wurde nicht gefunden.")
        return product

    def low_stock_products(self) -> list[Product]:
        return self.repository.low_stock()

    def create_product(self, data: dict) -> Product:
        try:
            payload = ProductCreateSchema(**data)
        except ValidationError as exc:
            raise ValidationServiceError("\n".join(error["msg"] for error in exc.errors())) from exc

        product = Product(**payload.model_dump())
        try:
            return self.repository.add(product)
        except IntegrityError as exc:
            raise ValidationServiceError("Artikelnummer ist bereits vorhanden.") from exc

    def update_product(self, product_id: int, data: dict) -> Product:
        product = self.get_product(product_id)
        try:
            payload = ProductUpdateSchema(**data)
        except ValidationError as exc:
            raise ValidationServiceError("\n".join(error["msg"] for error in exc.errors())) from exc

        for field_name, value in payload.model_dump().items():
            setattr(product, field_name, value)
        try:
            self.session.flush()
        except IntegrityError as exc:
            raise ValidationServiceError("Artikelnummer ist bereits vorhanden.") from exc
        return product

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.repository.delete(product)

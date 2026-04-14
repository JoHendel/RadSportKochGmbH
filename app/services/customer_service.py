from __future__ import annotations

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreateSchema, CustomerUpdateSchema
from app.services.exceptions import EntityNotFoundError, ValidationServiceError


class CustomerService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = CustomerRepository(session)

    def list_customers(self, search: str = "") -> list[Customer]:
        return self.repository.list(search=search)

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repository.get(customer_id)
        if not customer:
            raise EntityNotFoundError("Kunde wurde nicht gefunden.")
        return customer

    def get_next_customer_number(self) -> str:
        # Die nächste Kundennummer wird aus vorhandenen Nummern ermittelt,
        # damit das Formular sofort mit einem sinnvollen Vorschlag startet.
        max_number = 1000
        for customer_number in self.repository.list_customer_numbers():
            if not customer_number:
                continue
            if customer_number.startswith("C-"):
                numeric_part = customer_number.removeprefix("C-")
                if numeric_part.isdigit():
                    max_number = max(max_number, int(numeric_part))
        return f"C-{max_number + 1:04d}"

    def create_customer(self, data: dict) -> Customer:
        try:
            payload = CustomerCreateSchema(**data)
        except ValidationError as exc:
            raise ValidationServiceError("\n".join(error["msg"] for error in exc.errors())) from exc

        customer = Customer(**payload.model_dump())
        try:
            return self.repository.add(customer)
        except IntegrityError as exc:
            raise ValidationServiceError("Kundennummer oder E-Mail ist bereits vorhanden.") from exc

    def update_customer(self, customer_id: int, data: dict) -> Customer:
        customer = self.get_customer(customer_id)
        try:
            payload = CustomerUpdateSchema(**data)
        except ValidationError as exc:
            raise ValidationServiceError("\n".join(error["msg"] for error in exc.errors())) from exc

        for field_name, value in payload.model_dump().items():
            setattr(customer, field_name, value)
        try:
            self.session.flush()
        except IntegrityError as exc:
            raise ValidationServiceError("Kundennummer oder E-Mail ist bereits vorhanden.") from exc
        return customer

    def delete_customer(self, customer_id: int) -> None:
        customer = self.get_customer(customer_id)
        self.repository.delete(customer)

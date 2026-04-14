from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, search: str = "") -> list[Customer]:
        statement = (
            select(Customer)
            .options(selectinload(Customer.orders))
            .order_by(Customer.last_name.asc(), Customer.first_name.asc())
        )
        if search:
            pattern = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    Customer.customer_number.ilike(pattern),
                    Customer.first_name.ilike(pattern),
                    Customer.last_name.ilike(pattern),
                    Customer.email.ilike(pattern),
                    Customer.phone.ilike(pattern),
                )
            )
        return list(self.session.scalars(statement).all())

    def get(self, customer_id: int) -> Customer | None:
        statement = select(Customer).options(selectinload(Customer.orders)).where(Customer.id == customer_id)
        return self.session.scalars(statement).first()

    def list_customer_numbers(self) -> list[str]:
        statement = select(Customer.customer_number)
        return list(self.session.scalars(statement).all())

    def add(self, customer: Customer) -> Customer:
        self.session.add(customer)
        self.session.flush()
        return customer

    def delete(self, customer: Customer) -> None:
        self.session.delete(customer)

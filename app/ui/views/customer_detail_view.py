from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from app.models.customer import Customer
from app.ui.widgets.detail_card import DetailCard
from app.utils.formatters import format_date


class CustomerDetailView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.card = DetailCard("Kundendetails")
        layout = QVBoxLayout(self)
        layout.addWidget(self.card)

    def set_customer(self, customer: Customer | None) -> None:
        if not customer:
            self.card.set_rows([("Status", "Kein Kunde ausgewählt")])
            return
        self.card.set_rows(
            [
                ("Kundennummer", customer.customer_number),
                ("Vorname", customer.first_name),
                ("Nachname", customer.last_name),
                ("Telefon", customer.phone or "-"),
                ("E-Mail", customer.email or "-"),
                ("Adresse", customer.address or "-"),
                ("Notizen", customer.notes or "-"),
                ("Erstellt am", format_date(customer.created_at)),
                ("Anzahl Bestellungen", str(len(customer.orders))),
            ]
        )

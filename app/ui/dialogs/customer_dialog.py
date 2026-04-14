from __future__ import annotations

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QTextEdit, QVBoxLayout

from app.models.customer import Customer


class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer: Customer | None = None, suggested_customer_number: str | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Kunde bearbeiten" if customer else "Kunde anlegen")
        self.resize(520, 420)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.customer_number_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QTextEdit()
        self.notes_input = QTextEdit()

        form.addRow("Kundennummer", self.customer_number_input)
        form.addRow("Vorname", self.first_name_input)
        form.addRow("Nachname", self.last_name_input)
        form.addRow("Telefon", self.phone_input)
        form.addRow("E-Mail", self.email_input)
        form.addRow("Adresse", self.address_input)
        form.addRow("Notizen", self.notes_input)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if customer:
            self.customer_number_input.setText(customer.customer_number)
            self.first_name_input.setText(customer.first_name)
            self.last_name_input.setText(customer.last_name)
            self.phone_input.setText(customer.phone or "")
            self.email_input.setText(customer.email or "")
            self.address_input.setPlainText(customer.address or "")
            self.notes_input.setPlainText(customer.notes or "")
        elif suggested_customer_number:
            self.customer_number_input.setText(suggested_customer_number)
            self.customer_number_input.selectAll()

    def get_data(self) -> dict:
        return {
            "customer_number": self.customer_number_input.text(),
            "first_name": self.first_name_input.text(),
            "last_name": self.last_name_input.text(),
            "phone": self.phone_input.text() or None,
            "email": self.email_input.text() or None,
            "address": self.address_input.toPlainText() or None,
            "notes": self.notes_input.toPlainText() or None,
        }

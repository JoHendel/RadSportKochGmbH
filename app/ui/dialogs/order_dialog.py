from __future__ import annotations

from datetime import date
from decimal import Decimal

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.enums import OrderStatus, PaymentStatus
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.utils.formatters import format_currency
from app.utils.status_helpers import order_status_label, payment_status_label


class OrderDialog(QDialog):
    def __init__(self, customers: list[Customer], products: list[Product], parent=None, order: Order | None = None) -> None:
        super().__init__(parent)
        self.customers = customers
        self.products = products
        self.setWindowTitle("Bestellung bearbeiten" if order else "Bestellung anlegen")
        self.resize(840, 620)

        root_layout = QVBoxLayout(self)
        form = QFormLayout()

        self.order_number_input = QLineEdit()
        self.customer_input = QComboBox()
        for customer in customers:
            self.customer_input.addItem(f"{customer.customer_number} - {customer.full_name}", customer.id)
        self.order_date_input = QDateEdit()
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDate(QDate.currentDate())
        self.status_input = QComboBox()
        for status in OrderStatus:
            self.status_input.addItem(order_status_label(status), status)
        self.payment_status_input = QComboBox()
        for status in PaymentStatus:
            self.payment_status_input.addItem(payment_status_label(status), status)
        self.notes_input = QTextEdit()

        form.addRow("Bestellnummer", self.order_number_input)
        form.addRow("Kunde", self.customer_input)
        form.addRow("Bestelldatum", self.order_date_input)
        form.addRow("Status", self.status_input)
        form.addRow("Zahlstatus", self.payment_status_input)
        form.addRow("Notizen", self.notes_input)
        root_layout.addLayout(form)

        items_header = QHBoxLayout()
        items_label = QLabel("Bestellpositionen")
        items_label.setStyleSheet("font-size: 16px; font-weight: 700;")
        add_item_button = QPushButton("Position hinzufügen")
        add_item_button.clicked.connect(self.add_item_row)
        items_header.addWidget(items_label)
        items_header.addStretch()
        items_header.addWidget(add_item_button)
        root_layout.addLayout(items_header)

        self.items_table = QTableWidget(0, 5)
        self.items_table.setHorizontalHeaderLabels(["Artikel", "Menge", "Einzelpreis", "Gesamtpreis", "Aktion"])
        root_layout.addWidget(self.items_table, 1)

        self.total_label = QLabel("Gesamtsumme: 0,00 EUR")
        self.total_label.setAlignment(Qt.AlignRight)
        self.total_label.setStyleSheet("font-size: 18px; font-weight: 700;")
        root_layout.addWidget(self.total_label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root_layout.addWidget(buttons)

        if order:
            self.order_number_input.setText(order.order_number)
            self.customer_input.setCurrentIndex(self.customer_input.findData(order.customer_id))
            self.order_date_input.setDate(QDate(order.order_date.year, order.order_date.month, order.order_date.day))
            self.status_input.setCurrentIndex(self.status_input.findData(order.status))
            self.payment_status_input.setCurrentIndex(self.payment_status_input.findData(order.payment_status))
            self.notes_input.setPlainText(order.notes or "")
            for item in order.items:
                self.add_item_row(product_id=item.product_id, quantity=item.quantity, unit_price=float(item.unit_price))
        else:
            self.add_item_row()

    def add_item_row(self, product_id: int | None = None, quantity: int = 1, unit_price: float | None = None) -> None:
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)

        product_combo = QComboBox()
        for product in self.products:
            product_combo.addItem(f"{product.article_number} - {product.name}", product.id)
        if product_id is not None:
            product_combo.setCurrentIndex(product_combo.findData(product_id))
        product_combo.currentIndexChanged.connect(self._update_row_price)

        quantity_input = QSpinBox()
        quantity_input.setMinimum(1)
        quantity_input.setMaximum(1000)
        quantity_input.setValue(quantity)
        quantity_input.valueChanged.connect(self.update_totals)

        price_input = QLineEdit()
        if unit_price is not None:
            price_input.setText(f"{unit_price:.2f}")
        else:
            product = self._find_product(product_combo.currentData())
            price_input.setText(f"{float(product.sale_price):.2f}" if product else "0.00")
        price_input.textChanged.connect(self.update_totals)

        total_item = QTableWidgetItem("0,00 EUR")
        remove_button = QPushButton("Entfernen")
        remove_button.clicked.connect(self._remove_item_row_from_sender)

        self.items_table.setCellWidget(row, 0, product_combo)
        self.items_table.setCellWidget(row, 1, quantity_input)
        self.items_table.setCellWidget(row, 2, price_input)
        self.items_table.setItem(row, 3, total_item)
        self.items_table.setCellWidget(row, 4, remove_button)

        self.update_totals()

    def _remove_item_row_from_sender(self) -> None:
        button = self.sender()
        if button is None:
            return
        for row in range(self.items_table.rowCount()):
            if self.items_table.cellWidget(row, 4) is button:
                self.items_table.removeRow(row)
                break
        self.update_totals()

    def _find_product(self, product_id: int | None) -> Product | None:
        return next((product for product in self.products if product.id == product_id), None)

    def _update_row_price(self) -> None:
        for row in range(self.items_table.rowCount()):
            combo = self.items_table.cellWidget(row, 0)
            price_input = self.items_table.cellWidget(row, 2)
            if combo and price_input and not price_input.text():
                product = self._find_product(combo.currentData())
                if product:
                    price_input.setText(f"{float(product.sale_price):.2f}")
        self.update_totals()

    def update_totals(self) -> None:
        total = Decimal("0.00")
        for row in range(self.items_table.rowCount()):
            quantity_input = self.items_table.cellWidget(row, 1)
            price_input = self.items_table.cellWidget(row, 2)
            if not quantity_input or not price_input:
                continue
            try:
                row_total = Decimal(quantity_input.value()) * Decimal(price_input.text().replace(",", "."))
            except Exception:
                row_total = Decimal("0.00")
            total += row_total
            self.items_table.item(row, 3).setText(format_currency(row_total))
        self.total_label.setText(f"Gesamtsumme: {format_currency(total)}")

    def get_data(self) -> dict:
        items: list[dict] = []
        for row in range(self.items_table.rowCount()):
            product_combo = self.items_table.cellWidget(row, 0)
            quantity_input = self.items_table.cellWidget(row, 1)
            price_input = self.items_table.cellWidget(row, 2)
            items.append(
                {
                    "product_id": product_combo.currentData(),
                    "quantity": quantity_input.value(),
                    "unit_price": price_input.text().replace(",", "."),
                }
            )

        return {
            "order_number": self.order_number_input.text(),
            "customer_id": self.customer_input.currentData(),
            "order_date": self.order_date_input.date().toPython(),
            "status": self.status_input.currentData(),
            "payment_status": self.payment_status_input.currentData(),
            "notes": self.notes_input.toPlainText() or None,
            "items": items,
        }

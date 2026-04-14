from __future__ import annotations

from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QTableWidgetItem, QVBoxLayout, QWidget

from app.models.order import Order
from app.ui.widgets.detail_card import DetailCard
from app.ui.widgets.table_widget import DataTableWidget
from app.utils.formatters import format_currency, format_date
from app.utils.status_helpers import order_status_label, payment_status_label


class OrderDetailView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.card = DetailCard("Bestelldetails")
        self.items_table = DataTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels(["Artikel", "Menge", "Einzelpreis", "Gesamtpreis"])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.card)
        layout.addWidget(self.items_table)

    def set_order(self, order: Order | None) -> None:
        if not order:
            self.card.set_rows([("Status", "Keine Bestellung ausgewählt")])
            self.items_table.setRowCount(0)
            return

        self.card.set_rows(
            [
                ("Bestellnummer", order.order_number),
                ("Kunde", order.customer.full_name),
                ("Datum", format_date(order.order_date)),
                ("Status", order_status_label(order.status)),
                ("Zahlstatus", payment_status_label(order.payment_status)),
                ("Gesamtsumme", format_currency(order.total_amount)),
                ("Notizen", order.notes or "-"),
            ]
        )

        self.items_table.setRowCount(len(order.items))
        for row, item in enumerate(order.items):
            product_item = QTableWidgetItem(item.product.name)
            product_item.setToolTip(item.product.name)
            self.items_table.setItem(row, 0, product_item)
            self.items_table.setItem(row, 1, QTableWidgetItem(str(item.quantity)))
            self.items_table.setItem(row, 2, QTableWidgetItem(format_currency(item.unit_price)))
            self.items_table.setItem(row, 3, QTableWidgetItem(format_currency(item.total_price)))
        self.items_table.resizeRowsToContents()

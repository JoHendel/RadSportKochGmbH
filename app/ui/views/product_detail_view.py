from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from app.models.product import Product
from app.ui.widgets.detail_card import DetailCard
from app.utils.formatters import format_currency, format_date


class ProductDetailView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.card = DetailCard("Artikeldetails")
        layout = QVBoxLayout(self)
        layout.addWidget(self.card)

    def set_product(self, product: Product | None) -> None:
        if not product:
            self.card.set_rows([("Status", "Kein Artikel ausgewählt")])
            return
        self.card.set_rows(
            [
                ("Artikelnummer", product.article_number),
                ("Bezeichnung", product.name),
                ("Kategorie", product.category.value),
                ("Einkaufspreis", format_currency(product.purchase_price)),
                ("Verkaufspreis", format_currency(product.sale_price)),
                ("Lagerbestand", str(product.stock_quantity)),
                ("Mindestbestand", str(product.minimum_stock)),
                ("Aktiv", "Ja" if product.is_active else "Nein"),
                ("Erstellt am", format_date(product.created_at)),
                ("Beschreibung", product.description or "-"),
            ]
        )

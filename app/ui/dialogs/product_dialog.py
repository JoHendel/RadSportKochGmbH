from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from app.core.enums import ProductCategory
from app.models.product import Product


class ProductDialog(QDialog):
    def __init__(self, parent=None, product: Product | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Artikel bearbeiten" if product else "Artikel anlegen")
        self.resize(560, 460)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.article_number_input = QLineEdit()
        self.name_input = QLineEdit()
        self.category_input = QComboBox()
        for category in ProductCategory:
            self.category_input.addItem(category.value, category)
        self.description_input = QTextEdit()
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setMaximum(999999.99)
        self.purchase_price_input.setDecimals(2)
        self.sale_price_input = QDoubleSpinBox()
        self.sale_price_input.setMaximum(999999.99)
        self.sale_price_input.setDecimals(2)
        self.stock_quantity_input = QSpinBox()
        self.stock_quantity_input.setMaximum(100000)
        self.minimum_stock_input = QSpinBox()
        self.minimum_stock_input.setMaximum(100000)
        self.active_input = QCheckBox("Artikel ist aktiv")
        self.active_input.setChecked(True)

        form.addRow("Artikelnummer", self.article_number_input)
        form.addRow("Bezeichnung", self.name_input)
        form.addRow("Kategorie", self.category_input)
        form.addRow("Beschreibung", self.description_input)
        form.addRow("Einkaufspreis", self.purchase_price_input)
        form.addRow("Verkaufspreis", self.sale_price_input)
        form.addRow("Lagerbestand", self.stock_quantity_input)
        form.addRow("Mindestbestand", self.minimum_stock_input)
        form.addRow("", self.active_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if product:
            self.article_number_input.setText(product.article_number)
            self.name_input.setText(product.name)
            self.category_input.setCurrentIndex(self.category_input.findData(product.category))
            self.description_input.setPlainText(product.description or "")
            self.purchase_price_input.setValue(float(product.purchase_price))
            self.sale_price_input.setValue(float(product.sale_price))
            self.stock_quantity_input.setValue(product.stock_quantity)
            self.minimum_stock_input.setValue(product.minimum_stock)
            self.active_input.setChecked(product.is_active)

    def get_data(self) -> dict:
        return {
            "article_number": self.article_number_input.text(),
            "name": self.name_input.text(),
            "category": self.category_input.currentData(),
            "description": self.description_input.toPlainText() or None,
            "purchase_price": str(self.purchase_price_input.value()),
            "sale_price": str(self.sale_price_input.value()),
            "stock_quantity": self.stock_quantity_input.value(),
            "minimum_stock": self.minimum_stock_input.value(),
            "is_active": self.active_input.isChecked(),
        }

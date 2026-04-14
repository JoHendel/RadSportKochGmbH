from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.enums import OrderStatus, PaymentStatus, ProductCategory
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


class SeedService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def seed(self) -> None:
        customers = self._create_customers()
        products = self._create_products()
        self._create_orders(customers, products)
        self.session.flush()

    def _create_customers(self) -> list[Customer]:
        customers = [
            Customer(
                customer_number="C-1001",
                first_name="Martin",
                last_name="Becker",
                phone="+49 171 2203344",
                email="martin.becker@example.com",
                address="Sonnenstraße 18\n80331 München",
                notes="Kauft regelmäßig Zubehör für Rennrad-Touren.",
            ),
            Customer(
                customer_number="C-1002",
                first_name="Sarah",
                last_name="Lenz",
                phone="+49 172 3344556",
                email="sarah.lenz@example.com",
                address="Am Markt 4\n50667 Köln",
                notes="Interessiert an hochwertigen Gravel-Bikes.",
            ),
            Customer(
                customer_number="C-1003",
                first_name="Jonas",
                last_name="Hartmann",
                phone="+49 160 9988776",
                email="jonas.hartmann@example.com",
                address="Elbchaussee 72\n22765 Hamburg",
                notes="Werkstattkunde und Pendler mit E-Bike.",
            ),
            Customer(
                customer_number="C-1004",
                first_name="Nina",
                last_name="Schubert",
                phone="+49 151 4567890",
                email="nina.schubert@example.com",
                address="Bergstraße 11\n70173 Stuttgart",
                notes="Bestellt häufig Bekleidung und Helme.",
            ),
        ]
        self.session.add_all(customers)
        self.session.flush()
        return customers

    def _create_products(self) -> list[Product]:
        products = [
            Product(
                article_number="P-2001",
                name="RoadMaster Carbon 8",
                category=ProductCategory.BICYCLE,
                description="Leichtes Carbon-Rennrad mit Shimano 105 Di2.",
                purchase_price=Decimal("1899.00"),
                sale_price=Decimal("2599.00"),
                stock_quantity=4,
                minimum_stock=1,
                is_active=True,
            ),
            Product(
                article_number="P-2002",
                name="Gravel Explorer Pro",
                category=ProductCategory.BICYCLE,
                description="Vielseitiges Gravel-Bike mit hydraulischen Scheibenbremsen.",
                purchase_price=Decimal("1499.00"),
                sale_price=Decimal("2199.00"),
                stock_quantity=2,
                minimum_stock=1,
                is_active=True,
            ),
            Product(
                article_number="P-3001",
                name="Shimano Ultegra Kassette 11-30",
                category=ProductCategory.SPARE_PART,
                description="11-fach Kassette für sportive Einsätze.",
                purchase_price=Decimal("69.00"),
                sale_price=Decimal("99.90"),
                stock_quantity=8,
                minimum_stock=3,
                is_active=True,
            ),
            Product(
                article_number="P-3002",
                name="Continental Grand Prix 5000",
                category=ProductCategory.SPARE_PART,
                description="Performance-Rennradreifen 700x25C.",
                purchase_price=Decimal("34.00"),
                sale_price=Decimal("54.90"),
                stock_quantity=12,
                minimum_stock=4,
                is_active=True,
            ),
            Product(
                article_number="P-4001",
                name="Fahrradhelm AeroShield",
                category=ProductCategory.ACCESSORY,
                description="Leichter Helm mit MIPS-Schutzsystem.",
                purchase_price=Decimal("52.00"),
                sale_price=Decimal("89.90"),
                stock_quantity=5,
                minimum_stock=2,
                is_active=True,
            ),
            Product(
                article_number="P-4002",
                name="Trinkflasche Team 750 ml",
                category=ProductCategory.ACCESSORY,
                description="BPA-freie Trinkflasche im Vereinsdesign.",
                purchase_price=Decimal("4.20"),
                sale_price=Decimal("9.90"),
                stock_quantity=20,
                minimum_stock=6,
                is_active=True,
            ),
            Product(
                article_number="P-5001",
                name="Winter Jacket Pro",
                category=ProductCategory.CLOTHING,
                description="Wasserabweisende Softshell-Jacke für kalte Touren.",
                purchase_price=Decimal("65.00"),
                sale_price=Decimal("129.00"),
                stock_quantity=3,
                minimum_stock=3,
                is_active=True,
            ),
        ]
        self.session.add_all(products)
        self.session.flush()
        return products

    def _create_orders(self, customers: list[Customer], products: list[Product]) -> None:
        order_specs = [
            {
                "order_number": "O-5001",
                "customer": customers[0],
                "order_date": date.today() - timedelta(days=2),
                "status": OrderStatus.COMPLETED,
                "payment_status": PaymentStatus.PAID,
                "notes": "Abholung im Laden.",
                "items": [(products[4], 1), (products[5], 2)],
            },
            {
                "order_number": "O-5002",
                "customer": customers[1],
                "order_date": date.today() - timedelta(days=1),
                "status": OrderStatus.PROCESSING,
                "payment_status": PaymentStatus.PARTIALLY_PAID,
                "notes": "Rahmengröße vor Versand prüfen.",
                "items": [(products[1], 1), (products[2], 1)],
            },
            {
                "order_number": "O-5003",
                "customer": customers[2],
                "order_date": date.today(),
                "status": OrderStatus.OPEN,
                "payment_status": PaymentStatus.PENDING,
                "notes": "Pendlerpaket mit schneller Verfügbarkeit.",
                "items": [(products[3], 2), (products[4], 1), (products[6], 1)],
            },
        ]

        for spec in order_specs:
            order = Order(
                order_number=spec["order_number"],
                customer_id=spec["customer"].id,
                order_date=spec["order_date"],
                status=spec["status"],
                payment_status=spec["payment_status"],
                notes=spec["notes"],
                total_amount=Decimal("0.00"),
            )
            self.session.add(order)
            self.session.flush()

            for product, quantity in spec["items"]:
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.sale_price,
                    total_price=Decimal("0.00"),
                )
                item.recalculate_total()
                product.stock_quantity -= quantity
                order.items.append(item)

            order.recalculate_total()

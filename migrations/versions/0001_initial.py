"""Initial schema for RadSportKochGmbH."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


order_status = sa.Enum("DRAFT", "OPEN", "PROCESSING", "COMPLETED", "CANCELLED", name="orderstatus")
payment_status = sa.Enum("PENDING", "PARTIALLY_PAID", "PAID", "REFUNDED", name="paymentstatus")
product_category = sa.Enum("BICYCLE", "SPARE_PART", "ACCESSORY", "CLOTHING", name="productcategory")


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_number", sa.String(length=30), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_customer_number"), "customers", ["customer_number"], unique=True)
    op.create_index(op.f("ix_customers_email"), "customers", ["email"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("article_number", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("category", product_category, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("purchase_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("sale_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), nullable=False),
        sa.Column("minimum_stock", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_article_number"), "products", ["article_number"], unique=True)
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_number", sa.String(length=30), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("status", order_status, nullable=False),
        sa.Column("payment_status", payment_status, nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_customer_id"), "orders", ["customer_id"], unique=False)
    op.create_index(op.f("ix_orders_order_number"), "orders", ["order_number"], unique=True)

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_index(op.f("ix_orders_order_number"), table_name="orders")
    op.drop_index(op.f("ix_orders_customer_id"), table_name="orders")
    op.drop_table("orders")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_index(op.f("ix_products_article_number"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_customers_email"), table_name="customers")
    op.drop_index(op.f("ix_customers_customer_number"), table_name="customers")
    op.drop_table("customers")

    product_category.drop(op.get_bind(), checkfirst=False)
    payment_status.drop(op.get_bind(), checkfirst=False)
    order_status.drop(op.get_bind(), checkfirst=False)

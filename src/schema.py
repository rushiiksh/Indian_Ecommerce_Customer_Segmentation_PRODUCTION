from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("order_id", name="uq_orders_order_id"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    customer_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str | None] = mapped_column(String(100))

class OrderDetail(Base):
    __tablename__ = "order_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.order_id"), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    profit: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    sub_category: Mapped[str | None] = mapped_column(String(100))

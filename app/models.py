from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    generic_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    barcode: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    minimum_stock: Mapped[int] = mapped_column(Integer, default=5)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    batches: Mapped[list["StockBatch"]] = relationship(
        back_populates="medicine", cascade="all, delete-orphan"
    )


class StockBatch(Base):
    __tablename__ = "stock_batches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"), index=True)
    batch_number: Mapped[str] = mapped_column(String(80), index=True)
    expiry_date: Mapped[date] = mapped_column(Date)
    purchase_price: Mapped[float] = mapped_column(Numeric(12, 2))
    sale_price: Mapped[float] = mapped_column(Numeric(12, 2))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    medicine: Mapped[Medicine] = relationship(back_populates="batches")

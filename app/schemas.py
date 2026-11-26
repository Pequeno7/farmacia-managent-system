from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MedicineCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=2, max_length=160)
    generic_name: str | None = Field(default=None, max_length=160)
    category: str | None = Field(default=None, max_length=100)
    barcode: str | None = Field(default=None, max_length=80)
    minimum_stock: int = Field(default=5, ge=0)


class MedicineRead(MedicineCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    active: bool
    created_at: datetime


class BatchCreate(BaseModel):
    batch_number: str = Field(min_length=1, max_length=80)
    expiry_date: date
    purchase_price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    sale_price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    quantity: int = Field(default=0, ge=0)


class BatchRead(BatchCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    medicine_id: int
    created_at: datetime


class StockSummary(BaseModel):
    medicine_count: int
    batch_count: int
    units_in_stock: int
    low_stock_count: int
    expired_batch_count: int

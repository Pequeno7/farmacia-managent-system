from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Medicine, StockBatch
from app.schemas import StockSummary

router = APIRouter(prefix="/dashboard", tags=["Painel"])


@router.get("/stock", response_model=StockSummary)
def stock_summary(db: Session = Depends(get_db)):
    medicine_count = db.scalar(
        select(func.count(Medicine.id)).where(Medicine.active.is_(True))
    ) or 0
    batch_count = db.scalar(select(func.count(StockBatch.id))) or 0
    units_in_stock = db.scalar(select(func.coalesce(func.sum(StockBatch.quantity), 0))) or 0

    stock_by_medicine = db.execute(
        select(Medicine.id, Medicine.minimum_stock, func.coalesce(func.sum(StockBatch.quantity), 0))
        .outerjoin(StockBatch)
        .where(Medicine.active.is_(True))
        .group_by(Medicine.id, Medicine.minimum_stock)
    ).all()
    low_stock_count = sum(
        1 for _, minimum, quantity in stock_by_medicine if quantity <= minimum
    )
    expired_batch_count = db.scalar(
        select(func.count(StockBatch.id)).where(StockBatch.expiry_date < date.today())
    ) or 0

    return StockSummary(
        medicine_count=medicine_count,
        batch_count=batch_count,
        units_in_stock=units_in_stock,
        low_stock_count=low_stock_count,
        expired_batch_count=expired_batch_count,
    )

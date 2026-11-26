from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Medicine, StockBatch
from app.schemas import BatchCreate, BatchRead

router = APIRouter(tags=["Stock"])


@router.post(
    "/medicines/{medicine_id}/batches",
    response_model=BatchRead,
    status_code=status.HTTP_201_CREATED,
)
def create_batch(
    medicine_id: int, payload: BatchCreate, db: Session = Depends(get_db)
):
    medicine = db.get(Medicine, medicine_id)
    if medicine is None or not medicine.active:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    batch = StockBatch(medicine_id=medicine_id, **payload.model_dump())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


@router.get("/medicines/{medicine_id}/batches", response_model=list[BatchRead])
def list_batches(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.get(Medicine, medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    return db.scalars(
        select(StockBatch)
        .where(StockBatch.medicine_id == medicine_id)
        .order_by(StockBatch.expiry_date)
    ).all()

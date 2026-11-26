from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Medicine
from app.schemas import MedicineCreate, MedicineRead

router = APIRouter(prefix="/medicines", tags=["Medicamentos"])


@router.post("/", response_model=MedicineRead, status_code=status.HTTP_201_CREATED)
def create_medicine(payload: MedicineCreate, db: Session = Depends(get_db)):
    medicine = Medicine(**payload.model_dump())
    db.add(medicine)
    try:
        db.commit()
        db.refresh(medicine)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um medicamento com este SKU ou código de barras.",
        )
    return medicine


@router.get("/", response_model=list[MedicineRead])
def list_medicines(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    limit = min(max(limit, 1), 200)
    return db.scalars(
        select(Medicine).where(Medicine.active.is_(True))
        .order_by(Medicine.name).offset(skip).limit(limit)
    ).all()


@router.get("/{medicine_id}", response_model=MedicineRead)
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.get(Medicine, medicine_id)
    if medicine is None or not medicine.active:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado.")
    return medicine

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models  # noqa: F401
from app.routers import batches, dashboard, medicines


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Pharmacy Management System API",
    description="API inicial para gestão de medicamentos e stock de farmácia.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(medicines.router, prefix="/api/v1")
app.include_router(batches.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")


@app.get("/", tags=["Sistema"])
def root():
    return {"name": "Pharmacy Management System", "version": "0.1.0"}


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/lgus", tags=["local-governments"])


@router.get("/", response_model=List[schemas.LocalGovernment])
def get_lgus(
    skip: int = 0,
    limit: int = 100,
    province: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.LocalGovernment)
    if province:
        query = query.filter(models.LocalGovernment.province == province)
    lgus = query.offset(skip).limit(limit).all()
    return lgus


@router.get("/provinces", response_model=List[str])
def get_provinces(db: Session = Depends(get_db)):
    provinces = db.query(models.LocalGovernment.province).distinct().filter(
        models.LocalGovernment.province.isnot(None)
    ).all()
    return [p[0] for p in provinces if p[0]]


@router.get("/{lgu_id}", response_model=schemas.LGUDetailResponse)
def get_lgu_detail(lgu_id: int, db: Session = Depends(get_db)):
    lgu = db.query(models.LocalGovernment).filter(models.LocalGovernment.id == lgu_id).first()
    if lgu is None:
        raise HTTPException(status_code=404, detail="LGU not found")

    transactions = db.query(models.UnliquidatedTransaction).filter(
        models.UnliquidatedTransaction.lgu_id == lgu_id
    ).all()

    reports = db.query(models.AuditReport).filter(
        models.AuditReport.lgu_id == lgu_id
    ).all()

    total_unliquidated = sum(t.amount for t in transactions)
    years_with_data = sorted(list(set(t.year for t in transactions)))

    return schemas.LGUDetailResponse(
        lgu=lgu,
        total_unliquidated=total_unliquidated,
        years_with_data=years_with_data,
        transactions=transactions,
        reports=reports
    )


@router.get("/search/by-name")
def search_lgus_by_name(
    name: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    lgus = db.query(models.LocalGovernment).filter(
        models.LocalGovernment.name.ilike(f"%{name}%")
    ).limit(50).all()
    return lgus

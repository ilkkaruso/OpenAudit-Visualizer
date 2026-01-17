from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=List[schemas.UnliquidatedTransactionWithLGU])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    year: Optional[int] = None,
    province: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.UnliquidatedTransaction).join(models.LocalGovernment)

    if year:
        query = query.filter(models.UnliquidatedTransaction.year == year)
    if province:
        query = query.filter(models.LocalGovernment.province == province)
    if min_amount is not None:
        query = query.filter(models.UnliquidatedTransaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.UnliquidatedTransaction.amount <= max_amount)

    transactions = query.offset(skip).limit(limit).all()
    return transactions


@router.get("/years", response_model=List[int])
def get_available_years(db: Session = Depends(get_db)):
    years = db.query(models.UnliquidatedTransaction.year).distinct().order_by(
        models.UnliquidatedTransaction.year
    ).all()
    return [y[0] for y in years]


@router.get("/aggregate/by-year")
def aggregate_by_year(db: Session = Depends(get_db)):
    results = db.query(
        models.UnliquidatedTransaction.year,
        func.sum(models.UnliquidatedTransaction.amount).label("total_amount"),
        func.count(models.UnliquidatedTransaction.id).label("count")
    ).group_by(models.UnliquidatedTransaction.year).order_by(
        models.UnliquidatedTransaction.year
    ).all()

    return [
        {
            "year": r.year,
            "total_amount": float(r.total_amount),
            "count": r.count
        }
        for r in results
    ]


@router.get("/aggregate/by-province")
def aggregate_by_province(
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.LocalGovernment.province,
        func.sum(models.UnliquidatedTransaction.amount).label("total_amount"),
        func.count(models.UnliquidatedTransaction.id).label("count")
    ).join(models.UnliquidatedTransaction)

    if year:
        query = query.filter(models.UnliquidatedTransaction.year == year)

    results = query.group_by(models.LocalGovernment.province).order_by(
        func.sum(models.UnliquidatedTransaction.amount).desc()
    ).all()

    return [
        {
            "province": r.province,
            "total_amount": float(r.total_amount),
            "count": r.count
        }
        for r in results
    ]


@router.get("/top-lgus")
def get_top_lgus_by_amount(
    limit: int = Query(default=20, le=100),
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.LocalGovernment.id,
        models.LocalGovernment.name,
        models.LocalGovernment.province,
        func.sum(models.UnliquidatedTransaction.amount).label("total_amount"),
        func.count(models.UnliquidatedTransaction.id).label("transaction_count")
    ).join(models.UnliquidatedTransaction)

    if year:
        query = query.filter(models.UnliquidatedTransaction.year == year)

    results = query.group_by(
        models.LocalGovernment.id,
        models.LocalGovernment.name,
        models.LocalGovernment.province
    ).order_by(
        func.sum(models.UnliquidatedTransaction.amount).desc()
    ).limit(limit).all()

    return [
        {
            "lgu_id": r.id,
            "lgu_name": r.name,
            "province": r.province,
            "total_amount": float(r.total_amount),
            "transaction_count": r.transaction_count
        }
        for r in results
    ]

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/stats", response_model=schemas.StatsResponse)
def get_overall_stats(db: Session = Depends(get_db)):
    total_lgus = db.query(func.count(models.LocalGovernment.id)).scalar()
    total_reports = db.query(func.count(models.AuditReport.id)).scalar()

    total_unliquidated = db.query(
        func.sum(models.UnliquidatedTransaction.amount)
    ).scalar() or 0

    years = db.query(models.UnliquidatedTransaction.year).distinct().all()
    years_covered = sorted([y[0] for y in years])

    provinces_count = db.query(
        func.count(func.distinct(models.LocalGovernment.province))
    ).scalar()

    return schemas.StatsResponse(
        total_lgus=total_lgus,
        total_reports=total_reports,
        total_unliquidated_amount=total_unliquidated,
        years_covered=years_covered,
        provinces_count=provinces_count
    )


@router.get("/trends/yearly")
def get_yearly_trends(db: Session = Depends(get_db)):
    results = db.query(
        models.UnliquidatedTransaction.year,
        func.sum(models.UnliquidatedTransaction.amount).label("total_amount"),
        func.avg(models.UnliquidatedTransaction.amount).label("avg_amount"),
        func.count(models.UnliquidatedTransaction.id).label("count"),
        func.count(func.distinct(models.UnliquidatedTransaction.lgu_id)).label("lgus_count")
    ).group_by(
        models.UnliquidatedTransaction.year
    ).order_by(
        models.UnliquidatedTransaction.year
    ).all()

    return [
        {
            "year": r.year,
            "total_amount": float(r.total_amount),
            "avg_amount": float(r.avg_amount),
            "transaction_count": r.count,
            "lgus_count": r.lgus_count
        }
        for r in results
    ]


@router.get("/distribution/amount-ranges")
def get_amount_distribution(db: Session = Depends(get_db)):
    ranges = [
        (0, 100000, "0-100K"),
        (100000, 500000, "100K-500K"),
        (500000, 1000000, "500K-1M"),
        (1000000, 5000000, "1M-5M"),
        (5000000, 10000000, "5M-10M"),
        (10000000, float('inf'), "10M+")
    ]

    results = []
    for min_val, max_val, label in ranges:
        query = db.query(func.count(models.UnliquidatedTransaction.id)).filter(
            models.UnliquidatedTransaction.amount >= min_val
        )
        if max_val != float('inf'):
            query = query.filter(models.UnliquidatedTransaction.amount < max_val)

        count = query.scalar()
        results.append({
            "range": label,
            "min": min_val,
            "max": max_val if max_val != float('inf') else None,
            "count": count
        })

    return results


@router.get("/heatmap/province-year")
def get_province_year_heatmap(db: Session = Depends(get_db)):
    results = db.query(
        models.LocalGovernment.province,
        models.UnliquidatedTransaction.year,
        func.sum(models.UnliquidatedTransaction.amount).label("total_amount")
    ).join(
        models.UnliquidatedTransaction
    ).group_by(
        models.LocalGovernment.province,
        models.UnliquidatedTransaction.year
    ).all()

    return [
        {
            "province": r.province,
            "year": r.year,
            "total_amount": float(r.total_amount)
        }
        for r in results
    ]

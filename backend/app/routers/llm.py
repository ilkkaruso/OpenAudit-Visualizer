from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from .. import models, schemas
from ..database import get_db
from ..config import settings

router = APIRouter(prefix="/llm", tags=["llm-integration"])


class LLMRequest(BaseModel):
    report_id: Optional[int] = None
    lgu_id: Optional[int] = None
    analysis_type: str
    custom_prompt: Optional[str] = None
    model: str = "claude-sonnet-4"


@router.post("/analyze", response_model=schemas.LLMAnalysis)
async def analyze_with_llm(request: LLMRequest, db: Session = Depends(get_db)):
    if not request.report_id and not request.lgu_id:
        raise HTTPException(
            status_code=400,
            detail="Either report_id or lgu_id must be provided"
        )

    if not settings.anthropic_api_key and not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="LLM API keys not configured"
        )

    context_text = ""

    if request.report_id:
        report = db.query(models.AuditReport).filter(
            models.AuditReport.id == request.report_id
        ).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        context_text = report.findings_text or report.raw_text or ""

    elif request.lgu_id:
        lgu = db.query(models.LocalGovernment).filter(
            models.LocalGovernment.id == request.lgu_id
        ).first()
        if not lgu:
            raise HTTPException(status_code=404, detail="LGU not found")

        transactions = db.query(models.UnliquidatedTransaction).filter(
            models.UnliquidatedTransaction.lgu_id == request.lgu_id
        ).all()

        context_text = f"LGU: {lgu.name}, Province: {lgu.province}\n\n"
        context_text += f"Total unliquidated transactions: {len(transactions)}\n"
        context_text += f"Total amount: {sum(t.amount for t in transactions)}\n\n"

    prompt = request.custom_prompt or f"Analyze the following audit data for {request.analysis_type}:\n\n{context_text}"

    response_text = f"[LLM Analysis Placeholder - Integration ready for {request.model}]\n\n"
    response_text += f"Analysis Type: {request.analysis_type}\n"
    response_text += f"Context length: {len(context_text)} characters\n\n"
    response_text += "To enable actual LLM analysis, configure API keys in .env file."

    analysis = models.LLMAnalysis(
        report_id=request.report_id,
        lgu_id=request.lgu_id,
        analysis_type=request.analysis_type,
        prompt=prompt,
        response=response_text,
        model_name=request.model
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@router.get("/analyses", response_model=List[schemas.LLMAnalysis])
def get_llm_analyses(
    lgu_id: Optional[int] = None,
    report_id: Optional[int] = None,
    analysis_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.LLMAnalysis)

    if lgu_id:
        query = query.filter(models.LLMAnalysis.lgu_id == lgu_id)
    if report_id:
        query = query.filter(models.LLMAnalysis.report_id == report_id)
    if analysis_type:
        query = query.filter(models.LLMAnalysis.analysis_type == analysis_type)

    analyses = query.order_by(
        models.LLMAnalysis.created_at.desc()
    ).offset(skip).limit(limit).all()

    return analyses


@router.get("/analyses/{analysis_id}", response_model=schemas.LLMAnalysis)
def get_llm_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(models.LLMAnalysis).filter(
        models.LLMAnalysis.id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return analysis

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/", response_model=List[schemas.AuditTopic])
def get_all_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    topics = db.query(models.AuditTopic).offset(skip).limit(limit).all()
    return topics


@router.get("/{topic_id}", response_model=schemas.AuditTopic)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.AuditTopic).filter(models.AuditTopic.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.get("/{topic_id}/analysis", response_model=schemas.TopicAnalysisResponse)
def get_topic_analysis(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(models.AuditTopic).filter(models.AuditTopic.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    report_topics = db.query(models.ReportTopic).filter(
        models.ReportTopic.topic_id == topic_id
    ).all()

    report_count = len(report_topics)
    avg_proportion = None
    if report_count > 0:
        total_proportion = sum(rt.topic_proportion or 0 for rt in report_topics)
        avg_proportion = total_proportion / report_count

    return schemas.TopicAnalysisResponse(
        topic=topic,
        report_count=report_count,
        avg_proportion=avg_proportion
    )

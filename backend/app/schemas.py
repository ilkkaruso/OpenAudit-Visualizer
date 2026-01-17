from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class AuditTopicBase(BaseModel):
    topic_number: int
    description: str
    terms: Optional[str] = None
    prevalence: Optional[Decimal] = None


class AuditTopicCreate(AuditTopicBase):
    pass


class AuditTopic(AuditTopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LocalGovernmentBase(BaseModel):
    name: str
    province: Optional[str] = None
    region: Optional[str] = None
    lgu_type: Optional[str] = None


class LocalGovernmentCreate(LocalGovernmentBase):
    pass


class LocalGovernment(LocalGovernmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UnliquidatedTransactionBase(BaseModel):
    year: int
    amount: Decimal
    context_pre: Optional[str] = None
    context_post: Optional[str] = None


class UnliquidatedTransactionCreate(UnliquidatedTransactionBase):
    lgu_id: int
    report_id: Optional[int] = None


class UnliquidatedTransaction(UnliquidatedTransactionBase):
    id: int
    lgu_id: int
    report_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UnliquidatedTransactionWithLGU(UnliquidatedTransaction):
    lgu: Optional[LocalGovernment] = None

    model_config = ConfigDict(from_attributes=True)


class AuditReportBase(BaseModel):
    year: int
    report_type: str = "executive_summary"
    file_path: Optional[str] = None
    raw_text: Optional[str] = None
    findings_text: Optional[str] = None


class AuditReportCreate(AuditReportBase):
    lgu_id: int


class AuditReport(AuditReportBase):
    id: int
    lgu_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportTopicBase(BaseModel):
    topic_proportion: Optional[Decimal] = None


class ReportTopicCreate(ReportTopicBase):
    report_id: int
    topic_id: int


class ReportTopic(ReportTopicBase):
    id: int
    report_id: int
    topic_id: int
    created_at: datetime
    topic: Optional[AuditTopic] = None

    model_config = ConfigDict(from_attributes=True)


class LLMAnalysisBase(BaseModel):
    analysis_type: str
    prompt: Optional[str] = None
    response: str
    model_name: Optional[str] = None


class LLMAnalysisCreate(LLMAnalysisBase):
    report_id: Optional[int] = None
    lgu_id: Optional[int] = None


class LLMAnalysis(LLMAnalysisBase):
    id: int
    report_id: Optional[int] = None
    lgu_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatsResponse(BaseModel):
    total_lgus: int
    total_reports: int
    total_unliquidated_amount: Decimal
    years_covered: List[int]
    provinces_count: int


class LGUDetailResponse(BaseModel):
    lgu: LocalGovernment
    total_unliquidated: Decimal
    years_with_data: List[int]
    transactions: List[UnliquidatedTransaction]
    reports: List[AuditReport]


class TopicAnalysisResponse(BaseModel):
    topic: AuditTopic
    report_count: int
    avg_proportion: Optional[Decimal] = None

from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class AuditTopic(Base):
    __tablename__ = "audit_topics"

    id = Column(Integer, primary_key=True, index=True)
    topic_number = Column(Integer, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    terms = Column(Text)
    prevalence = Column(DECIMAL(5, 4))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    report_topics = relationship("ReportTopic", back_populates="topic")


class LocalGovernment(Base):
    __tablename__ = "local_governments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    province = Column(String(255))
    region = Column(String(100))
    lgu_type = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('name', 'province', name='_name_province_uc'),)

    audit_reports = relationship("AuditReport", back_populates="lgu")
    unliquidated_transactions = relationship("UnliquidatedTransaction", back_populates="lgu")
    llm_analyses = relationship("LLMAnalysis", back_populates="lgu")


class AuditReport(Base):
    __tablename__ = "audit_reports"

    id = Column(Integer, primary_key=True, index=True)
    lgu_id = Column(Integer, ForeignKey("local_governments.id", ondelete="CASCADE"))
    year = Column(Integer, nullable=False)
    report_type = Column(String(100), default="executive_summary")
    file_path = Column(Text)
    raw_text = Column(Text)
    findings_text = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('lgu_id', 'year', 'report_type', name='_lgu_year_type_uc'),)

    lgu = relationship("LocalGovernment", back_populates="audit_reports")
    unliquidated_transactions = relationship("UnliquidatedTransaction", back_populates="report")
    report_topics = relationship("ReportTopic", back_populates="report")
    llm_analyses = relationship("LLMAnalysis", back_populates="report")


class UnliquidatedTransaction(Base):
    __tablename__ = "unliquidated_transactions"

    id = Column(Integer, primary_key=True, index=True)
    lgu_id = Column(Integer, ForeignKey("local_governments.id", ondelete="CASCADE"), index=True)
    report_id = Column(Integer, ForeignKey("audit_reports.id", ondelete="CASCADE"))
    year = Column(Integer, nullable=False, index=True)
    amount = Column(DECIMAL(15, 2), nullable=False)
    context_pre = Column(Text)
    context_post = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    lgu = relationship("LocalGovernment", back_populates="unliquidated_transactions")
    report = relationship("AuditReport", back_populates="unliquidated_transactions")


class ReportTopic(Base):
    __tablename__ = "report_topics"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("audit_reports.id", ondelete="CASCADE"), index=True)
    topic_id = Column(Integer, ForeignKey("audit_topics.id", ondelete="CASCADE"), index=True)
    topic_proportion = Column(DECIMAL(5, 4))
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (UniqueConstraint('report_id', 'topic_id', name='_report_topic_uc'),)

    report = relationship("AuditReport", back_populates="report_topics")
    topic = relationship("AuditTopic", back_populates="report_topics")


class LLMAnalysis(Base):
    __tablename__ = "llm_analysis"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("audit_reports.id", ondelete="CASCADE"), index=True)
    lgu_id = Column(Integer, ForeignKey("local_governments.id", ondelete="CASCADE"), index=True)
    analysis_type = Column(String(100), nullable=False)
    prompt = Column(Text)
    response = Column(Text, nullable=False)
    model_name = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    report = relationship("AuditReport", back_populates="llm_analyses")
    lgu = relationship("LocalGovernment", back_populates="llm_analyses")

-- OpenAudit Database Schema
-- PostgreSQL database for audit reports and findings

-- Table for audit topic themes (from LDA topic modeling)
CREATE TABLE IF NOT EXISTS audit_topics (
    id SERIAL PRIMARY KEY,
    topic_number INTEGER UNIQUE NOT NULL,
    description TEXT NOT NULL,
    terms TEXT,
    prevalence DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for local government units
CREATE TABLE IF NOT EXISTS local_governments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    province VARCHAR(255),
    region VARCHAR(100),
    lgu_type VARCHAR(50), -- municipality, city, province
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, province)
);

-- Table for audit reports
CREATE TABLE IF NOT EXISTS audit_reports (
    id SERIAL PRIMARY KEY,
    lgu_id INTEGER REFERENCES local_governments(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    report_type VARCHAR(100) DEFAULT 'executive_summary',
    file_path TEXT,
    raw_text TEXT,
    findings_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(lgu_id, year, report_type)
);

-- Table for unliquidated transactions (extracted from reports)
CREATE TABLE IF NOT EXISTS unliquidated_transactions (
    id SERIAL PRIMARY KEY,
    lgu_id INTEGER REFERENCES local_governments(id) ON DELETE CASCADE,
    report_id INTEGER REFERENCES audit_reports(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    context_pre TEXT,
    context_post TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for topic-report associations (from topic modeling)
CREATE TABLE IF NOT EXISTS report_topics (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES audit_reports(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES audit_topics(id) ON DELETE CASCADE,
    topic_proportion DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_id, topic_id)
);

-- Table for LLM-generated analysis and insights
CREATE TABLE IF NOT EXISTS llm_analysis (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES audit_reports(id) ON DELETE CASCADE,
    lgu_id INTEGER REFERENCES local_governments(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL, -- summary, risk_assessment, recommendations, etc.
    prompt TEXT,
    response TEXT NOT NULL,
    model_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_unliquidated_lgu ON unliquidated_transactions(lgu_id);
CREATE INDEX IF NOT EXISTS idx_unliquidated_year ON unliquidated_transactions(year);
CREATE INDEX IF NOT EXISTS idx_audit_reports_lgu ON audit_reports(lgu_id);
CREATE INDEX IF NOT EXISTS idx_audit_reports_year ON audit_reports(year);
CREATE INDEX IF NOT EXISTS idx_report_topics_report ON report_topics(report_id);
CREATE INDEX IF NOT EXISTS idx_report_topics_topic ON report_topics(topic_id);
CREATE INDEX IF NOT EXISTS idx_llm_analysis_report ON llm_analysis(report_id);
CREATE INDEX IF NOT EXISTS idx_llm_analysis_lgu ON llm_analysis(lgu_id);

-- Insert the 25 audit topics from Topicmodel1.R
INSERT INTO audit_topics (topic_number, description) VALUES
(1, 'Citation of COA Circulars'),
(2, 'Financial accounting and bookkeeping'),
(3, 'Employee/Personnel Payment Protocols'),
(4, 'Need for timely submission of documents'),
(5, 'City Audit Recommendations'),
(6, 'Municipal Audit Recommendations'),
(7, 'Fuel, Inventory, and Supplies Anomalies'),
(8, 'Implementation of Audit Recommendations for Past Year'),
(9, 'COA Circular Violations'),
(10, 'Remittance of Withheld Income Taxes'),
(11, 'Completion of Construction Projects/Contracts'),
(12, 'Public land and property management'),
(13, 'Utilization of Disaster Management Fund (LDRRMF)'),
(14, 'Solid Waste Management Issues'),
(15, 'Unliquidated Cash Advances Issues'),
(16, 'Reporting of Local Financial Statements'),
(17, 'General Recommendations and Observations'),
(18, 'Management of Local Development Fund (LDF)'),
(19, 'Procurement and Bidding Issues'),
(20, 'Balance of Disallowances, Suspensions, and Charges'),
(21, 'Real Property Tax Management'),
(22, 'Property, Plant, and Equipment Records and Reporting Issues'),
(23, 'Recommendations for Municipal Treasurer and Accountant'),
(24, 'Gender and Development Budgeting and Project Issues'),
(25, 'Municipal Financial Accounting and Management Issues')
ON CONFLICT (topic_number) DO NOTHING;

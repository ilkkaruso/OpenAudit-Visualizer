export interface AuditTopic {
  id: number;
  topic_number: number;
  description: string;
  terms?: string;
  prevalence?: number;
  created_at: string;
  updated_at: string;
}

export interface LocalGovernment {
  id: number;
  name: string;
  province?: string;
  region?: string;
  lgu_type?: string;
  created_at: string;
  updated_at: string;
}

export interface UnliquidatedTransaction {
  id: number;
  lgu_id: number;
  report_id?: number;
  year: number;
  amount: number;
  context_pre?: string;
  context_post?: string;
  created_at: string;
  updated_at: string;
  lgu?: LocalGovernment;
}

export interface AuditReport {
  id: number;
  lgu_id: number;
  year: number;
  report_type: string;
  file_path?: string;
  raw_text?: string;
  findings_text?: string;
  created_at: string;
  updated_at: string;
}

export interface StatsResponse {
  total_lgus: number;
  total_reports: number;
  total_unliquidated_amount: number;
  years_covered: number[];
  provinces_count: number;
}

export interface LGUDetailResponse {
  lgu: LocalGovernment;
  total_unliquidated: number;
  years_with_data: number[];
  transactions: UnliquidatedTransaction[];
  reports: AuditReport[];
}

export interface YearlyAggregate {
  year: number;
  total_amount: number;
  count: number;
}

export interface ProvinceAggregate {
  province: string;
  total_amount: number;
  count: number;
}

export interface TopLGU {
  lgu_id: number;
  lgu_name: string;
  province: string;
  total_amount: number;
  transaction_count: number;
}

export interface YearlyTrend {
  year: number;
  total_amount: number;
  avg_amount: number;
  transaction_count: number;
  lgus_count: number;
}

export interface LLMAnalysis {
  id: number;
  report_id?: number;
  lgu_id?: number;
  analysis_type: string;
  prompt?: string;
  response: string;
  model_name?: string;
  created_at: string;
  updated_at: string;
}

export interface LLMRequest {
  report_id?: number;
  lgu_id?: number;
  analysis_type: string;
  custom_prompt?: string;
  model?: string;
}

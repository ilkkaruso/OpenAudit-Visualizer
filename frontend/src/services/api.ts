import axios from 'axios';
import type {
  AuditTopic,
  LocalGovernment,
  UnliquidatedTransaction,
  StatsResponse,
  LGUDetailResponse,
  YearlyAggregate,
  ProvinceAggregate,
  TopLGU,
  YearlyTrend,
  LLMAnalysis,
  LLMRequest
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const topicsAPI = {
  getAll: () => api.get<AuditTopic[]>('/topics'),
  getById: (id: number) => api.get<AuditTopic>(`/topics/${id}`),
  getAnalysis: (id: number) => api.get(`/topics/${id}/analysis`),
};

export const lgusAPI = {
  getAll: (params?: { skip?: number; limit?: number; province?: string }) =>
    api.get<LocalGovernment[]>('/lgus', { params }),
  getProvinces: () => api.get<string[]>('/lgus/provinces'),
  getById: (id: number) => api.get<LGUDetailResponse>(`/lgus/${id}`),
  searchByName: (name: string) => api.get<LocalGovernment[]>(`/lgus/search/by-name`, {
    params: { name },
  }),
};

export const transactionsAPI = {
  getAll: (params?: {
    skip?: number;
    limit?: number;
    year?: number;
    province?: string;
    min_amount?: number;
    max_amount?: number;
  }) => api.get<UnliquidatedTransaction[]>('/transactions', { params }),
  getYears: () => api.get<number[]>('/transactions/years'),
  aggregateByYear: () => api.get<YearlyAggregate[]>('/transactions/aggregate/by-year'),
  aggregateByProvince: (year?: number) =>
    api.get<ProvinceAggregate[]>('/transactions/aggregate/by-province', {
      params: { year },
    }),
  getTopLGUs: (limit: number = 20, year?: number) =>
    api.get<TopLGU[]>('/transactions/top-lgus', {
      params: { limit, year },
    }),
};

export const analyticsAPI = {
  getStats: () => api.get<StatsResponse>('/analytics/stats'),
  getYearlyTrends: () => api.get<YearlyTrend[]>('/analytics/trends/yearly'),
  getAmountDistribution: () => api.get('/analytics/distribution/amount-ranges'),
  getProvinceYearHeatmap: () => api.get('/analytics/heatmap/province-year'),
};

export const llmAPI = {
  analyze: (request: LLMRequest) => api.post<LLMAnalysis>('/llm/analyze', request),
  getAnalyses: (params?: {
    lgu_id?: number;
    report_id?: number;
    analysis_type?: string;
    skip?: number;
    limit?: number;
  }) => api.get<LLMAnalysis[]>('/llm/analyses', { params }),
  getAnalysisById: (id: number) => api.get<LLMAnalysis>(`/llm/analyses/${id}`),
};

export default api;

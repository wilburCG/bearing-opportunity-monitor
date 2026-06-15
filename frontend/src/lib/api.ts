import type { Company, EntityRelationship, IndustryGraph, Opportunity, OpportunityDetail, OpportunityNote, Product } from '@/types/opportunity';

function getApiBaseUrl(): string {
  const configured = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (configured && configured !== 'auto') return configured;
  return '/api/backend';
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API ${response.status}: ${text}`);
  }

  return response.json() as Promise<T>;
}

export function listOpportunities(params: {
  industry?: string;
  province?: string;
  opportunity_type?: string;
  status?: string;
  min_score?: number;
  max_score?: number;
  min_urgency?: number;
  max_urgency?: number;
  min_confidence?: number;
  max_confidence?: number;
  limit?: number;
}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return request<Opportunity[]>(`/opportunities?${query.toString()}`);
}

export function getOpportunity(id: number) {
  return request<OpportunityDetail>(`/opportunities/${id}`);
}

export function updateOpportunityStatus(id: number, status: string) {
  return request<OpportunityDetail>(`/opportunities/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}

export function listOpportunityNotes(id: number) {
  return request<OpportunityNote[]>(`/opportunities/${id}/notes`);
}

export function createOpportunityNote(id: number, note: string, operator = 'Web') {
  return request<OpportunityNote>(`/opportunities/${id}/notes`, {
    method: 'POST',
    body: JSON.stringify({ note, operator }),
  });
}

export function chatWithAgent(message: string) {
  return request<{ answer: string; mode: string }>(`/agent/chat`, {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}

export function listCompanies(params: { q?: string; industry?: string; company_type?: string; province?: string; city?: string; status?: string; min_confidence?: number; max_confidence?: number; limit?: number } = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return request<Company[]>(`/industry/companies?${query.toString()}`);
}

export function createCompany(payload: Partial<Company> & { name: string }) {
  return request<Company>(`/industry/companies`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function listProducts(params: { q?: string; industry?: string; category?: string; company_id?: number; manufacturer_name?: string; status?: string; min_confidence?: number; max_confidence?: number; limit?: number } = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return request<Product[]>(`/industry/products?${query.toString()}`);
}

export function createProduct(payload: Partial<Product> & { name: string }) {
  return request<Product>(`/industry/products`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function listRelationships(params: { entity_type?: string; entity_id?: number; source_type?: string; target_type?: string; relation_type?: string; min_confidence?: number; max_confidence?: number; limit?: number } = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return request<EntityRelationship[]>(`/industry/relationships?${query.toString()}`);
}

export function createRelationship(payload: Omit<EntityRelationship, 'id' | 'created_at' | 'updated_at'>) {
  return request<EntityRelationship>(`/industry/relationships`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getIndustryGraph(params: { entity_type?: string; entity_id?: number; source_type?: string; target_type?: string; relation_type?: string; min_confidence?: number; max_confidence?: number; limit?: number } = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') query.set(key, String(value));
  });
  return request<IndustryGraph>(`/industry/graph?${query.toString()}`);
}

export type OpportunityStatus = 'new' | 'pending_verify' | 'followed' | 'converted' | 'invalid' | string;

export interface Opportunity {
  id: number;
  title: string;
  summary?: string | null;
  opportunity_type?: string | null;
  industry?: string | null;
  company_name?: string | null;
  province?: string | null;
  city?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  volume_score: number;
  urgency_score: number;
  confidence_score: number;
  fit_score: number;
  total_score: number;
  status: OpportunityStatus;
  created_at: string;
  updated_at: string;
}

export interface OpportunityDetail extends Opportunity {
  project_name?: string | null;
  district?: string | null;
  address?: string | null;
  bearing_types?: { items?: string[] } | null;
  bearing_models?: { items?: string[] } | null;
  equipment_types?: { items?: string[] } | null;
  estimated_quantity?: string | null;
  estimated_amount?: string | null;
  deadline_at?: string | null;
  confidence_reason?: string | null;
  recommended_action?: string | null;
}

export interface OpportunityNote {
  id: number;
  opportunity_id: number;
  note: string;
  operator?: string | null;
}

export interface Company {
  id: number;
  name: string;
  alias_names?: { items?: string[] } | null;
  company_type?: string | null;
  industry?: string | null;
  province?: string | null;
  city?: string | null;
  address?: string | null;
  website?: string | null;
  description?: string | null;
  tags?: { items?: string[] } | null;
  source_url?: string | null;
  confidence_score: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  model?: string | null;
  category?: string | null;
  industry?: string | null;
  company_id?: number | null;
  manufacturer_name?: string | null;
  description?: string | null;
  specifications?: Record<string, unknown> | null;
  application_scenarios?: { items?: string[] } | null;
  tags?: { items?: string[] } | null;
  source_url?: string | null;
  confidence_score: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface EntityRelationship {
  id: number;
  source_type: string;
  source_id: number;
  target_type: string;
  target_id: number;
  relation_type: string;
  evidence?: string | null;
  confidence_score: number;
  source_url?: string | null;
  created_at: string;
  updated_at: string;
}

export interface IndustryGraphNode {
  id: string;
  entity_type: string;
  entity_id: number;
  label: string;
  meta?: Record<string, unknown> | null;
}

export interface IndustryGraph {
  nodes: IndustryGraphNode[];
  edges: Array<{
    id: number;
    source: string;
    target: string;
    relation_type: string;
    evidence?: string | null;
    confidence_score: number;
  }>;
}

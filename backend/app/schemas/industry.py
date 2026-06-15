from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CompanyBase(BaseModel):
    name: str
    alias_names: dict | None = None
    company_type: str | None = None
    industry: str | None = None
    province: str | None = None
    city: str | None = None
    address: str | None = None
    website: str | None = None
    description: str | None = None
    tags: dict | None = None
    source_url: str | None = None
    confidence_score: float = 0
    status: str = "active"


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    alias_names: dict | None = None
    company_type: str | None = None
    industry: str | None = None
    province: str | None = None
    city: str | None = None
    address: str | None = None
    website: str | None = None
    description: str | None = None
    tags: dict | None = None
    source_url: str | None = None
    confidence_score: float | None = None
    status: str | None = None


class CompanyOut(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ProductBase(BaseModel):
    name: str
    model: str | None = None
    category: str | None = None
    industry: str | None = None
    company_id: int | None = None
    manufacturer_name: str | None = None
    description: str | None = None
    specifications: dict | None = None
    application_scenarios: dict | None = None
    tags: dict | None = None
    source_url: str | None = None
    confidence_score: float = 0
    status: str = "active"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    model: str | None = None
    category: str | None = None
    industry: str | None = None
    company_id: int | None = None
    manufacturer_name: str | None = None
    description: str | None = None
    specifications: dict | None = None
    application_scenarios: dict | None = None
    tags: dict | None = None
    source_url: str | None = None
    confidence_score: float | None = None
    status: str | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class RelationshipBase(BaseModel):
    source_type: str
    source_id: int
    target_type: str
    target_id: int
    relation_type: str
    evidence: str | None = None
    confidence_score: float = 0
    source_url: str | None = None


class RelationshipCreate(RelationshipBase):
    pass


class RelationshipUpdate(BaseModel):
    relation_type: str | None = None
    evidence: str | None = None
    confidence_score: float | None = None
    source_url: str | None = None


class RelationshipOut(RelationshipBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class GraphNode(BaseModel):
    id: str
    entity_type: str
    entity_id: int
    label: str
    meta: dict | None = None


class GraphEdge(BaseModel):
    id: int
    source: str
    target: str
    relation_type: str
    evidence: str | None = None
    confidence_score: float


class IndustryGraphOut(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]

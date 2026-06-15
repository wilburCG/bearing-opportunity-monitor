from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.company import Company
from app.models.product import Product
from app.models.opportunity import Opportunity
from app.models.entity_relationship import EntityRelationship
from app.schemas.industry import (
    CompanyCreate,
    CompanyOut,
    CompanyUpdate,
    GraphEdge,
    GraphNode,
    IndustryGraphOut,
    ProductCreate,
    ProductOut,
    ProductUpdate,
    RelationshipCreate,
    RelationshipOut,
    RelationshipUpdate,
)

router = APIRouter()

ENTITY_TYPES = {"company", "product", "opportunity"}


def _apply_updates(item, payload):
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(item, key, value)
    return item


def _node_key(entity_type: str, entity_id: int) -> str:
    return f"{entity_type}:{entity_id}"


def _validate_entity_type(entity_type: str) -> None:
    if entity_type not in ENTITY_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported entity type: {entity_type}")


@router.get("/companies", response_model=list[CompanyOut])
def list_companies(
    q: str | None = None,
    industry: str | None = None,
    company_type: str | None = None,
    status: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(Company)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Company.name.like(like), Company.description.like(like), Company.city.like(like)))
    if industry:
        query = query.filter(Company.industry == industry)
    if company_type:
        query = query.filter(Company.company_type == company_type)
    if status:
        query = query.filter(Company.status == status)
    else:
        query = query.filter(Company.status != "deleted")
    return query.order_by(Company.updated_at.desc()).limit(limit).all()


@router.post("/companies", response_model=CompanyOut)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    item = Company(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/companies/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    item = db.get(Company, company_id)
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    return item


@router.patch("/companies/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, payload: CompanyUpdate, db: Session = Depends(get_db)):
    item = db.get(Company, company_id)
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    _apply_updates(item, payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/companies/{company_id}", response_model=CompanyOut)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    item = db.get(Company, company_id)
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    item.status = "deleted"
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/products", response_model=list[ProductOut])
def list_products(
    q: str | None = None,
    industry: str | None = None,
    category: str | None = None,
    company_id: int | None = None,
    status: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Product.name.like(like), Product.model.like(like), Product.description.like(like), Product.manufacturer_name.like(like)))
    if industry:
        query = query.filter(Product.industry == industry)
    if category:
        query = query.filter(Product.category == category)
    if company_id:
        query = query.filter(Product.company_id == company_id)
    if status:
        query = query.filter(Product.status == status)
    else:
        query = query.filter(Product.status != "deleted")
    return query.order_by(Product.updated_at.desc()).limit(limit).all()


@router.post("/products", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    item = Product(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    item = db.get(Product, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return item


@router.patch("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    item = db.get(Product, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    _apply_updates(item, payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/products/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    item = db.get(Product, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    item.status = "deleted"
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/relationships", response_model=list[RelationshipOut])
def list_relationships(
    entity_type: str | None = None,
    entity_id: int | None = None,
    relation_type: str | None = None,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    query = db.query(EntityRelationship)
    if entity_type:
        _validate_entity_type(entity_type)
    if entity_type and entity_id:
        query = query.filter(
            or_(
                (EntityRelationship.source_type == entity_type) & (EntityRelationship.source_id == entity_id),
                (EntityRelationship.target_type == entity_type) & (EntityRelationship.target_id == entity_id),
            )
        )
    elif entity_type:
        query = query.filter(or_(EntityRelationship.source_type == entity_type, EntityRelationship.target_type == entity_type))
    if relation_type:
        query = query.filter(EntityRelationship.relation_type == relation_type)
    return query.order_by(EntityRelationship.updated_at.desc()).limit(limit).all()


@router.post("/relationships", response_model=RelationshipOut)
def create_relationship(payload: RelationshipCreate, db: Session = Depends(get_db)):
    _validate_entity_type(payload.source_type)
    _validate_entity_type(payload.target_type)
    item = EntityRelationship(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/relationships/{relationship_id}", response_model=RelationshipOut)
def update_relationship(relationship_id: int, payload: RelationshipUpdate, db: Session = Depends(get_db)):
    item = db.get(EntityRelationship, relationship_id)
    if not item:
        raise HTTPException(status_code=404, detail="Relationship not found")
    _apply_updates(item, payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/relationships/{relationship_id}")
def delete_relationship(relationship_id: int, db: Session = Depends(get_db)):
    item = db.get(EntityRelationship, relationship_id)
    if not item:
        raise HTTPException(status_code=404, detail="Relationship not found")
    db.delete(item)
    db.commit()
    return {"ok": True}


@router.get("/relationships/graph", response_model=IndustryGraphOut)
@router.get("/graph", response_model=IndustryGraphOut)
def get_graph(
    entity_type: str | None = None,
    entity_id: int | None = None,
    relation_type: str | None = None,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    relationships = list_relationships(entity_type=entity_type, entity_id=entity_id, relation_type=relation_type, limit=limit, db=db)
    node_refs: set[tuple[str, int]] = set()
    for rel in relationships:
        node_refs.add((rel.source_type, rel.source_id))
        node_refs.add((rel.target_type, rel.target_id))

    companies = {item.id: item for item in db.query(Company).filter(Company.id.in_([i for t, i in node_refs if t == "company"])).all()} if any(t == "company" for t, _ in node_refs) else {}
    products = {item.id: item for item in db.query(Product).filter(Product.id.in_([i for t, i in node_refs if t == "product"])).all()} if any(t == "product" for t, _ in node_refs) else {}
    opportunities = {item.id: item for item in db.query(Opportunity).filter(Opportunity.id.in_([i for t, i in node_refs if t == "opportunity"])).all()} if any(t == "opportunity" for t, _ in node_refs) else {}

    nodes: list[GraphNode] = []
    for node_type, node_id in sorted(node_refs):
        label = f"{node_type}:{node_id}"
        meta = None
        if node_type == "company" and node_id in companies:
            item = companies[node_id]
            label = item.name
            meta = {"industry": item.industry, "company_type": item.company_type, "city": item.city}
        elif node_type == "product" and node_id in products:
            item = products[node_id]
            label = item.model or item.name
            meta = {"name": item.name, "category": item.category, "manufacturer_name": item.manufacturer_name}
        elif node_type == "opportunity" and node_id in opportunities:
            item = opportunities[node_id]
            label = item.title
            meta = {"industry": item.industry, "company_name": item.company_name, "total_score": item.total_score}
        nodes.append(GraphNode(id=_node_key(node_type, node_id), entity_type=node_type, entity_id=node_id, label=label, meta=meta))

    edges = [
        GraphEdge(
            id=rel.id,
            source=_node_key(rel.source_type, rel.source_id),
            target=_node_key(rel.target_type, rel.target_id),
            relation_type=rel.relation_type,
            evidence=rel.evidence,
            confidence_score=rel.confidence_score,
        )
        for rel in relationships
    ]
    return IndustryGraphOut(nodes=nodes, edges=edges)

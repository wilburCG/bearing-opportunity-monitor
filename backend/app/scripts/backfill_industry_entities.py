"""Backfill companies and relationships from existing opportunities.

Usage:
  python -m app.scripts.backfill_industry_entities
"""
from app.db.session import SessionLocal
from app.models.company import Company
from app.models.entity_relationship import EntityRelationship
from app.models.opportunity import Opportunity


def main() -> None:
    db = SessionLocal()
    created_companies = 0
    created_relationships = 0
    try:
        opportunities = db.query(Opportunity).filter(Opportunity.company_name.isnot(None)).all()
        for opp in opportunities:
            name = (opp.company_name or "").strip()
            if not name or name in {"-", "未知", "不详"}:
                continue
            company = db.query(Company).filter(Company.name == name).one_or_none()
            if not company:
                company = Company(
                    name=name,
                    company_type="buyer",
                    industry=opp.industry,
                    province=opp.province,
                    city=opp.city,
                    description=f"由商机沉淀的企业：{opp.title}",
                    tags={"items": ["from_opportunity"]},
                    confidence_score=max(opp.confidence_score or 0, 50),
                    status="active",
                )
                db.add(company)
                db.flush()
                created_companies += 1
            rel = db.query(EntityRelationship).filter(
                EntityRelationship.source_type == "company",
                EntityRelationship.source_id == company.id,
                EntityRelationship.target_type == "opportunity",
                EntityRelationship.target_id == opp.id,
                EntityRelationship.relation_type == "has_opportunity",
            ).one_or_none()
            if not rel:
                db.add(EntityRelationship(
                    source_type="company",
                    source_id=company.id,
                    target_type="opportunity",
                    target_id=opp.id,
                    relation_type="has_opportunity",
                    evidence=opp.title,
                    confidence_score=opp.confidence_score or 0,
                ))
                created_relationships += 1
        db.commit()
        print({"created_companies": created_companies, "created_relationships": created_relationships})
    finally:
        db.close()


if __name__ == "__main__":
    main()

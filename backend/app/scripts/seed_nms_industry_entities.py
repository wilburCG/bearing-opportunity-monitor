"""Seed Nanchang Mineral Systems / 南矿集团 company and product entities.

This preserves the NMS research result in the new industry intelligence data model.
Usage:
  python -m app.scripts.seed_nms_industry_entities
"""
from app.db.session import SessionLocal
from app.models.company import Company
from app.models.entity_relationship import EntityRelationship
from app.models.product import Product

NMS_PRODUCTS = [
    {
        "name": "旋回破碎机",
        "model": "GC系列",
        "category": "破碎设备",
        "description": "初级破碎设备，用于矿山和石料加工，将爆破物料加工至250毫米以下。",
    },
    {
        "name": "颚式破碎机",
        "model": "JC系列",
        "category": "破碎设备",
        "description": "初级破碎设备，用于矿山和石料加工，将爆破物料加工至350毫米以下。",
    },
    {
        "name": "圆锥破碎机",
        "model": "CC单缸系列",
        "category": "破碎设备",
        "description": "中碎、细碎破碎设备，将初碎物料加工至30-10毫米以下。",
    },
    {
        "name": "圆锥破碎机",
        "model": "MC多缸系列",
        "category": "破碎设备",
        "description": "中碎、细碎破碎设备；2025年MC800多缸圆锥破碎机获评江西省优秀新产品一等奖。",
    },
    {
        "name": "反击式破碎机",
        "model": "HS系列",
        "category": "破碎设备",
        "description": "非金属矿和石料加工设备，适用于中等硬度以下和低磨蚀性岩石。",
    },
    {
        "name": "立轴冲击式破碎机",
        "model": "VS系列",
        "category": "破碎设备",
        "description": "细碎整形设备，用于非金属矿和石料加工。",
    },
    {
        "name": "筛分机",
        "model": "YKR圆振筛",
        "category": "筛分设备",
        "description": "用于矿山和石料加工的预筛和产品干湿筛分作业。",
    },
    {
        "name": "筛分机",
        "model": "ZKR直线筛",
        "category": "筛分设备",
        "description": "用于矿山和石料加工的筛分设备。",
    },
    {
        "name": "筛分机",
        "model": "BS系列香蕉筛",
        "category": "筛分设备",
        "description": "用于金属矿山领域的大处理量矿物筛分作业。",
    },
    {
        "name": "筛分机",
        "model": "HFS/V系列液压高频筛",
        "category": "筛分设备",
        "description": "用于5毫米以下细粒径高效筛分，广泛用于机制砂筛分作业。",
    },
    {
        "name": "给料机",
        "model": "HPF棒条给料机",
        "category": "给料设备",
        "description": "用于矿山和石料加工的给料及预筛作业。",
    },
    {
        "name": "移动破碎筛分站",
        "model": "MT履带系列",
        "category": "大型集成设备",
        "description": "用于小规模、短期的破碎筛分作业。",
    },
    {
        "name": "移动破碎筛分站",
        "model": "MP轮胎系列",
        "category": "大型集成设备",
        "description": "用于小规模、中短期的破碎筛分作业。",
    },
    {
        "name": "制砂楼",
        "model": "MSP系列",
        "category": "大型集成设备",
        "description": "用于建筑机制砂精品砂作业。",
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.name == "南昌矿机集团股份有限公司").one_or_none()
        if not company:
            company = Company(
                name="南昌矿机集团股份有限公司",
                alias_names={"items": ["南矿集团", "南昌矿机", "NMS", "Nanchang Mineral Systems"]},
                company_type="manufacturer",
                industry="破碎筛分",
                province="江西",
                city="南昌",
                website="https://www.nmsindustries.com/",
                description="国内中高端矿机装备供应服务商，主营砂石骨料、金属矿山相关破碎与筛分设备研发、设计、生产、销售及后市场服务。",
                tags={"items": ["上市公司", "破碎筛分", "矿山设备", "砂石骨料"]},
                source_url="http://static.cninfo.com.cn/finalpage/2026-04-24/1225161911.PDF",
                confidence_score=95,
                status="active",
            )
            db.add(company)
            db.flush()

        created_products = 0
        created_relationships = 0
        for item in NMS_PRODUCTS:
            product = db.query(Product).filter(
                Product.company_id == company.id,
                Product.name == item["name"],
                Product.model == item["model"],
            ).one_or_none()
            if not product:
                product = Product(
                    **item,
                    industry="破碎筛分",
                    company_id=company.id,
                    manufacturer_name=company.name,
                    application_scenarios={"items": ["砂石骨料", "金属矿山", "石料加工"]},
                    tags={"items": ["NMS", "年报披露主要整机产品"]},
                    source_url="http://static.cninfo.com.cn/finalpage/2026-04-24/1225161911.PDF",
                    confidence_score=90,
                    status="active",
                )
                db.add(product)
                db.flush()
                created_products += 1

            rel = db.query(EntityRelationship).filter(
                EntityRelationship.source_type == "company",
                EntityRelationship.source_id == company.id,
                EntityRelationship.target_type == "product",
                EntityRelationship.target_id == product.id,
                EntityRelationship.relation_type == "manufactures",
            ).one_or_none()
            if not rel:
                db.add(EntityRelationship(
                    source_type="company",
                    source_id=company.id,
                    target_type="product",
                    target_id=product.id,
                    relation_type="manufactures",
                    evidence="南矿集团2025年年度报告“主要产品及其用途”列示。",
                    confidence_score=90,
                    source_url="http://static.cninfo.com.cn/finalpage/2026-04-24/1225161911.PDF",
                ))
                created_relationships += 1

        db.commit()
        print({"company_id": company.id, "created_products": created_products, "created_relationships": created_relationships})
    finally:
        db.close()


if __name__ == "__main__":
    main()

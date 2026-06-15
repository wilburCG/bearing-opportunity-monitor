"""Refine crusher OEM seed data with better verified URLs/product lines."""
from app.db.session import SessionLocal
from app.models.company import Company
from app.models.product import Product
from app.models.entity_relationship import EntityRelationship

REFINE = {
    "上海山美环保装备股份有限公司": {
        "website": "https://www.sanmecrusher.com/",
        "source_url": "https://www.sanmecrusher.com/products/",
        "confidence_score": 94,
        "description": "破碎筛分装备商，产品中心完整列出 Crusher、Mobile Crusher、Sand Maker & Washer、Feeders & Screens，覆盖圆锥、颚破、反击、立轴、锤破、旋回、移动破碎筛分等。",
        "products": [
            ("圆锥破碎机", "E-SMG系列", "破碎设备", "山美产品中心列示 E-SMG Series Cone Crusher。"),
            ("圆锥破碎机", "E-SMS系列", "破碎设备", "山美产品中心列示 E-SMS Series Cone Crusher。"),
            ("圆锥破碎机", "SMH系列", "破碎设备", "山美产品中心列示 SMH Series Cone Crusher。"),
            ("颚式破碎机", "Jaw Crusher", "破碎设备", "山美产品中心列示 Jaw Crusher。"),
            ("反击式破碎机", "HCP系列", "破碎设备", "山美产品中心列示 Impact Crusher / HCP。"),
            ("立轴冲击式破碎机", "VC7系列", "破碎设备", "山美产品中心列示 VC7 Series Vertical Shaft Impact Crusher。"),
            ("锤式破碎机", "PCX系列", "破碎设备", "山美产品中心列示 PCX Series High Efficient Hammer Fine Crusher。"),
            ("旋回破碎机", "Gyratory Crusher", "破碎设备", "山美产品中心列示 Gyratory Crusher。"),
            ("辊筛破碎机", "SMTR系列", "破碎设备", "山美产品中心列示 SMTR series roller screening crusher。"),
            ("辊式制砂机", "SMPG系列", "破碎设备", "山美产品中心列示 SMPG Series Roller Sand Maker。"),
            ("移动颚式破碎站", "E-MP系列", "大型集成设备", "山美产品中心列示 E-MP Series Mobile Jaw Crusher。"),
            ("移动反击式破碎站", "E-MP系列", "大型集成设备", "山美产品中心列示 E-MP Series Mobile Impact Crusher。"),
            ("移动圆锥破碎站", "E-MP系列", "大型集成设备", "山美产品中心列示 E-MP Series Mobile Cone Crusher。"),
            ("移动筛分站", "E-MP系列", "筛分设备", "山美产品中心列示 E-MP Series Mobile Screen。"),
        ],
    },
    "浙矿重工股份有限公司": {
        "website": "https://www.cnzkzg.com/",
        "source_url": "https://www.cnzkzg.com/",
        "confidence_score": 92,
        "description": "浙矿重工股份有限公司成立于2003年，2020年创业板上市，官网称专注于矿山破碎筛分设备的研发与制造，是国内砂石装备行业上市公司，提供设备供应及 EPC+O 全流程服务。",
        "products": [],
    },
    "广西美斯达工程机械设备有限公司": {
        "website": "https://www.mesdagroup.com/",
        "source_url": "https://www.mesdagroup.com/",
        "confidence_score": 92,
        "description": "美斯达为广西南宁移动破碎筛分设备制造商，官网称提供 crawler mounted mobile crushing and screening equipment，覆盖 mobile jaw/cone/impact/hammer crusher、mobile screener、mobile conveyor 等。",
        "products": [
            ("移动颚式破碎机", "mobile jaw crusher", "大型集成设备", "美斯达官网列示 mobile jaw crusher。"),
            ("移动圆锥破碎机", "mobile cone crusher", "大型集成设备", "美斯达官网列示 mobile cone crusher。"),
            ("移动反击式破碎机", "mobile impact crusher", "大型集成设备", "美斯达官网列示 mobile impact crusher，案例含 MC-350IS。"),
            ("移动锤式破碎机", "mobile hammer crusher", "大型集成设备", "美斯达官网列示 mobile hammer crusher。"),
            ("移动筛分机", "mobile screener", "筛分设备", "美斯达官网列示 mobile screener。"),
            ("移动输送机", "mobile conveyor", "其他设备", "美斯达官网列示 mobile conveyor。"),
        ],
    },
}


def main():
    db = SessionLocal()
    try:
        companies = 0
        products = 0
        rels = 0
        for name, data in REFINE.items():
            company = db.query(Company).filter(Company.name == name).one_or_none()
            if not company:
                continue
            for key in ["website", "source_url", "confidence_score", "description"]:
                setattr(company, key, data[key])
            companies += 1
            for product_data in data["products"]:
                pname, model, category, desc = product_data
                product = db.query(Product).filter(Product.company_id == company.id, Product.name == pname, Product.model == model).one_or_none()
                if not product:
                    product = Product(company_id=company.id, name=pname, model=model)
                    db.add(product)
                    db.flush()
                product.category = category
                product.industry = "破碎筛分"
                product.manufacturer_name = company.name
                product.description = desc
                product.application_scenarios = {"items": ["砂石骨料", "金属矿山", "建筑固废", "石料加工"]}
                product.tags = {"items": ["破碎机", "主机产品", "官网产品中心核验"]}
                product.source_url = data["source_url"]
                product.confidence_score = min(data["confidence_score"], 92)
                product.status = "active"
                products += 1
                rel = db.query(EntityRelationship).filter(
                    EntityRelationship.source_type == "company",
                    EntityRelationship.source_id == company.id,
                    EntityRelationship.target_type == "product",
                    EntityRelationship.target_id == product.id,
                    EntityRelationship.relation_type == "manufactures",
                ).one_or_none()
                if not rel:
                    rel = EntityRelationship(source_type="company", source_id=company.id, target_type="product", target_id=product.id, relation_type="manufactures")
                    db.add(rel)
                rel.evidence = "官网产品中心核验。"
                rel.confidence_score = min(data["confidence_score"], 92)
                rel.source_url = data["source_url"]
                rels += 1
        db.commit()
        print({"companies_refined": companies, "products_upserted": products, "relationships_upserted": rels})
    finally:
        db.close()


if __name__ == "__main__":
    main()

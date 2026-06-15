"""Seed crusher/screening OEM companies and product series.

This script extends the industry intelligence system with domestic crusher/screening
OEMs in the same style as the NMS seed data.

Usage:
  python -m app.scripts.seed_crusher_oem_entities
"""
from app.db.session import SessionLocal
from app.models.company import Company
from app.models.product import Product
from app.models.entity_relationship import EntityRelationship

SOURCE_NOTE = "公开官网/上市公司公告/企业产品中心可核验；部分型号为官网常见产品系列归纳。"

OEM_DATA = [
    {
        "name": "福建南方路面机械股份有限公司",
        "aliases": ["南方路机", "NFLG", "南方路面机械"],
        "province": "福建",
        "city": "泉州",
        "website": "https://www.nflg.com/",
        "description": "工程搅拌、整形制砂、固定/移动破碎筛分、固废资源化和绿色建材整体方案企业。官网列示移动破碎筛分、固定破碎筛分、整形制砂等产品线。",
        "source_url": "https://www.nflg.com/",
        "confidence": 92,
        "products": [
            ("固定破碎筛分设备", "固定破碎筛分", "大型集成设备", "砂石骨料固定式破碎筛分生产线/系统。"),
            ("移动破碎筛分设备", "移动破碎筛分", "大型集成设备", "面向矿山、工程建设和固废资源化的移动破碎筛分设备。"),
            ("机制砂生产设备", "整形制砂", "大型集成设备", "整形制砂/精品机制砂生产线。"),
            ("固废资源化设备", "建筑固废处理线", "大型集成设备", "建筑垃圾、固废资源化处理整体方案。"),
        ],
    },
    {
        "name": "世邦工业科技集团股份有限公司",
        "aliases": ["世邦工业", "SBM", "上海世邦"],
        "province": "上海",
        "city": "上海",
        "website": "https://www.sbmchina.com/",
        "description": "破碎、磨粉、矿山加工设备企业，产品中心列示 Jaw Crusher、Cone Crusher、Gyratory Crusher、Mobile Crusher 等。",
        "source_url": "https://www.sbmchina.com/equipments/",
        "confidence": 90,
        "products": [
            ("颚式破碎机", "C6X系列", "破碎设备", "官网产品中心列示 Jaw Crusher / C6X。"),
            ("圆锥破碎机", "HPT系列", "破碎设备", "官网产品中心列示 Cone Crusher / HPT。"),
            ("旋回破碎机", "HGT系列", "破碎设备", "官网产品中心列示 Gyratory Crusher / HGT。"),
            ("移动破碎站", "LD系列", "大型集成设备", "官网产品中心列示 Mobile Crusher / LD。"),
            ("制砂机", "VSI/VU系列", "破碎设备", "制砂、整形及砂石骨料加工设备。"),
        ],
    },
    {
        "name": "黎明重工科技股份有限公司",
        "aliases": ["黎明重工", "Liming", "河南黎明重工"],
        "province": "河南",
        "city": "郑州",
        "website": "https://www.lmlq.com/",
        "description": "从1987年起专注矿山、建筑、能源等基础设施所需大型装备研发制造，官网列示破碎、制砂、EPC方案和移动破碎站。",
        "source_url": "https://www.lmlq.com/",
        "confidence": 92,
        "products": [
            ("颚式破碎机", "PEW/PE系列", "破碎设备", "矿山和建筑骨料粗碎设备。"),
            ("圆锥破碎机", "HPT/HST/CS系列", "破碎设备", "硬岩中细碎设备。"),
            ("反击式破碎机", "PF/PFW系列", "破碎设备", "中低硬度岩石中细碎和整形。"),
            ("制砂机", "VSI/VU系列", "破碎设备", "机制砂、整形和绿色建材加工。"),
            ("移动破碎站", "K系列/履带式", "大型集成设备", "建筑破碎、矿山破碎、金属矿破碎移动方案。"),
        ],
    },
    {
        "name": "上海山美环保装备股份有限公司",
        "aliases": ["上海山美", "山美环保", "SANME"],
        "province": "上海",
        "city": "上海",
        "website": "https://www.shsmzj.com/",
        "description": "专注矿业、固废及新能源领域工艺及装备，提供矿物加工、尾矿处理、固废循环经济产业园和EPCO绿色建材骨料整体方案。",
        "source_url": "https://www.shsmzj.com/",
        "confidence": 92,
        "products": [
            ("颚式破碎机", "JC/PE系列", "破碎设备", "矿山、骨料和固废处理粗碎设备。"),
            ("圆锥破碎机", "SMH/SMG系列", "破碎设备", "中细碎圆锥破碎设备。"),
            ("反击式破碎机", "HC/HS系列", "破碎设备", "中低硬度物料破碎及建筑垃圾处理。"),
            ("立轴冲击式破碎机", "VC7/VSI系列", "破碎设备", "制砂和骨料整形设备。"),
            ("振动筛", "YK/ZK系列", "筛分设备", "破碎筛分生产线配套筛分设备。"),
            ("移动破碎站", "轮胎/履带系列", "大型集成设备", "矿山、固废、建筑垃圾移动破碎筛分设备。"),
        ],
    },
    {
        "name": "浙矿重工股份有限公司",
        "aliases": ["浙矿股份", "浙矿重工", "Zhekuang Heavy Industry"],
        "province": "浙江",
        "city": "湖州",
        "website": "https://www.zhekuang.com/",
        "description": "上市破碎筛分设备企业，面向砂石骨料、金属矿山和资源回收领域提供破碎、筛分及成套装备。",
        "source_url": "https://www.zhekuang.com/",
        "confidence": 86,
        "products": [
            ("颚式破碎机", "CJ系列", "破碎设备", "粗碎颚式破碎设备。"),
            ("圆锥破碎机", "RC/多缸系列", "破碎设备", "中细碎圆锥破碎设备。"),
            ("反击式破碎机", "PF/CI系列", "破碎设备", "骨料中细碎及整形。"),
            ("振动筛", "YK/ZK系列", "筛分设备", "砂石骨料和矿山筛分设备。"),
            ("给料机", "棒条/振动给料机", "给料设备", "破碎筛分生产线给料设备。"),
        ],
    },
    {
        "name": "广西美斯达工程机械设备有限公司",
        "aliases": ["美斯达", "MESDA"],
        "province": "广西",
        "city": "南宁",
        "website": "https://www.mesdagroup.com/",
        "description": "移动破碎筛分装备企业，重点覆盖履带式移动破碎站、移动筛分站和移动制砂装备。",
        "source_url": "https://www.mesdagroup.com/",
        "confidence": 82,
        "products": [
            ("移动颚式破碎站", "履带式", "大型集成设备", "移动粗碎设备。"),
            ("移动圆锥破碎站", "履带式", "大型集成设备", "移动中细碎设备。"),
            ("移动反击式破碎站", "履带式", "大型集成设备", "建筑垃圾和中低硬度物料移动破碎。"),
            ("移动筛分站", "履带式", "筛分设备", "移动筛分和分级设备。"),
            ("移动制砂站", "履带式", "大型集成设备", "移动制砂和整形设备。"),
        ],
    },
    {
        "name": "成都大宏立机器股份有限公司",
        "aliases": ["大宏立", "大宏立机器"],
        "province": "四川",
        "city": "成都",
        "website": "https://www.dahongli.com/",
        "description": "上市砂石骨料破碎筛分成套设备企业，提供破碎、筛分、输送、环保及成套解决方案。",
        "source_url": "https://www.dahongli.com/",
        "confidence": 84,
        "products": [
            ("颚式破碎机", "PE/PEX系列", "破碎设备", "砂石骨料粗碎设备。"),
            ("圆锥破碎机", "单缸/多缸系列", "破碎设备", "中细碎圆锥破碎设备。"),
            ("反击式破碎机", "PF系列", "破碎设备", "中低硬度骨料破碎设备。"),
            ("制砂机", "立轴冲击式", "破碎设备", "机制砂与整形设备。"),
            ("振动筛", "圆振筛/直线筛", "筛分设备", "骨料分级筛分设备。"),
        ],
    },
    {
        "name": "河南红星矿山机器有限公司",
        "aliases": ["红星机器", "红星矿山", "HXJQ"],
        "province": "河南",
        "city": "郑州",
        "website": "https://www.hxjq.cn/",
        "description": "河南矿山破碎、制砂、磨粉设备企业，产品覆盖颚破、圆锥破、反击破、制砂机、移动破碎站等。",
        "source_url": "https://www.hxjq.cn/",
        "confidence": 80,
        "products": [
            ("颚式破碎机", "PE系列", "破碎设备", "粗碎颚式破碎设备。"),
            ("圆锥破碎机", "单缸/多缸系列", "破碎设备", "硬岩中细碎设备。"),
            ("反击式破碎机", "PF系列", "破碎设备", "中低硬度物料破碎。"),
            ("制砂机", "HX/VSI系列", "破碎设备", "机制砂设备。"),
            ("移动破碎站", "轮胎/履带系列", "大型集成设备", "移动破碎筛分设备。"),
        ],
    },
    {
        "name": "郑州一帆机械设备有限公司",
        "aliases": ["一帆机械", "郑州一帆", "YIFAN"],
        "province": "河南",
        "city": "郑州",
        "website": "https://www.yfcrusher.com/",
        "description": "破碎、筛分、制砂、移动破碎站和建筑垃圾处理设备企业。",
        "source_url": "https://www.yfcrusher.com/",
        "confidence": 78,
        "products": [
            ("颚式破碎机", "PE/JC系列", "破碎设备", "粗碎设备。"),
            ("圆锥破碎机", "SMH/液压系列", "破碎设备", "中细碎设备。"),
            ("反击式破碎机", "PF/HC系列", "破碎设备", "骨料破碎设备。"),
            ("制砂机", "VSI系列", "破碎设备", "制砂整形设备。"),
            ("移动破碎站", "轮胎/履带系列", "大型集成设备", "移动破碎筛分及建筑垃圾处理。"),
        ],
    },
    {
        "name": "河南中誉鼎力智能装备有限公司",
        "aliases": ["中誉鼎力", "河南中誉鼎力", "Dingli"],
        "province": "河南",
        "city": "新乡",
        "website": "https://www.dlksjq.com/",
        "description": "砂石骨料绿色矿山破碎筛分设备与生产线企业，重点覆盖重锤破、颚破、反击破、筛分和成套线。",
        "source_url": "https://www.dlksjq.com/",
        "confidence": 78,
        "products": [
            ("重锤式破碎机", "PCZ/重锤破", "破碎设备", "砂石骨料一次成型破碎设备。"),
            ("颚式破碎机", "PE系列", "破碎设备", "粗碎设备。"),
            ("反击式破碎机", "PF系列", "破碎设备", "中细碎整形设备。"),
            ("振动筛", "圆振筛", "筛分设备", "砂石骨料筛分设备。"),
            ("砂石骨料生产线", "绿色矿山生产线", "大型集成设备", "绿色矿山成套破碎筛分生产线。"),
        ],
    },
    {
        "name": "枣庄鑫金山智能装备有限公司",
        "aliases": ["鑫金山", "枣庄鑫金山"],
        "province": "山东",
        "city": "枣庄",
        "website": "https://www.xjscrusher.com/",
        "description": "砂石骨料破碎筛分及绿色矿山装备企业，重点覆盖锤式破碎、反击破、筛分和成套生产线。",
        "source_url": "https://www.xjscrusher.com/",
        "confidence": 76,
        "products": [
            ("锤式破碎机", "单段锤破/重锤破", "破碎设备", "砂石骨料破碎设备。"),
            ("反击式破碎机", "反击破系列", "破碎设备", "骨料中细碎设备。"),
            ("颚式破碎机", "颚破系列", "破碎设备", "粗碎设备。"),
            ("振动筛", "筛分系列", "筛分设备", "骨料筛分设备。"),
            ("砂石骨料生产线", "绿色矿山成套线", "大型集成设备", "绿色矿山成套设备。"),
        ],
    },
    {
        "name": "韶瑞重工（广东）有限公司",
        "aliases": ["韶瑞重工", "Shaorui Heavy Industries", "SRH"],
        "province": "广东",
        "city": "韶关",
        "website": "https://www.shaoruiheavy.com/",
        "description": "破碎筛分设备企业，产品覆盖颚破、圆锥破、反击破、振动筛、给料机等。",
        "source_url": "https://www.shaoruiheavy.com/",
        "confidence": 78,
        "products": [
            ("颚式破碎机", "SJ系列", "破碎设备", "粗碎设备。"),
            ("圆锥破碎机", "SC/多缸系列", "破碎设备", "中细碎设备。"),
            ("反击式破碎机", "SF系列", "破碎设备", "中低硬度物料破碎。"),
            ("振动筛", "SS系列", "筛分设备", "砂石骨料筛分设备。"),
            ("给料机", "SV系列", "给料设备", "破碎筛分生产线给料设备。"),
        ],
    },
    {
        "name": "中信重工机械股份有限公司",
        "aliases": ["中信重工", "CITIC Heavy Industries"],
        "province": "河南",
        "city": "洛阳",
        "website": "https://www.citichmc.com/",
        "description": "大型矿山重型装备企业，覆盖大型破碎、磨矿、选矿和矿山成套装备。",
        "source_url": "https://www.citichmc.com/",
        "confidence": 84,
        "products": [
            ("旋回破碎机", "大型旋回破", "破碎设备", "大型矿山粗碎设备。"),
            ("圆锥破碎机", "大型圆锥破", "破碎设备", "矿山中细碎设备。"),
            ("半自磨机/球磨机", "磨矿设备", "其他设备", "矿山磨矿装备，非破碎主机但属于矿山主机。"),
        ],
    },
    {
        "name": "北方重工集团有限公司",
        "aliases": ["北方重工", "NHI"],
        "province": "辽宁",
        "city": "沈阳",
        "website": "https://www.nhi.com.cn/",
        "description": "大型矿山、冶金、散料输送和重型装备企业，产品覆盖大型破碎、磨矿及矿山系统装备。",
        "source_url": "https://www.nhi.com.cn/",
        "confidence": 82,
        "products": [
            ("旋回破碎机", "大型旋回破", "破碎设备", "大型矿山粗碎设备。"),
            ("圆锥破碎机", "大型圆锥破", "破碎设备", "矿山中细碎设备。"),
            ("齿辊破碎机", "齿辊破", "破碎设备", "煤炭、矿山及物料破碎设备。"),
            ("磨矿设备", "球磨/自磨系列", "其他设备", "矿山磨矿装备，非破碎主机但与矿山系统配套。"),
        ],
    },
]


def upsert_company(db, item):
    company = db.query(Company).filter(Company.name == item["name"]).one_or_none()
    if not company:
        company = Company(name=item["name"])
        db.add(company)
        db.flush()
    company.alias_names = {"items": item["aliases"]}
    company.company_type = "manufacturer"
    company.industry = "破碎筛分"
    company.province = item["province"]
    company.city = item["city"]
    company.website = item["website"]
    company.description = item["description"]
    company.tags = {"items": ["破碎机主机厂", "破碎筛分", "砂石骨料", "矿山设备"]}
    company.source_url = item["source_url"]
    company.confidence_score = item["confidence"]
    company.status = "active"
    return company


def upsert_product(db, company, item, product_tuple):
    name, model, category, description = product_tuple
    product = db.query(Product).filter(
        Product.company_id == company.id,
        Product.name == name,
        Product.model == model,
    ).one_or_none()
    if not product:
        product = Product(company_id=company.id, name=name, model=model)
        db.add(product)
        db.flush()
    product.category = category
    product.industry = "破碎筛分"
    product.manufacturer_name = company.name
    product.description = description
    product.application_scenarios = {"items": ["砂石骨料", "金属矿山", "建筑固废", "石料加工"]}
    product.tags = {"items": ["破碎机", "主机产品", company.name]}
    product.source_url = item["source_url"]
    product.confidence_score = min(item["confidence"], 90)
    product.status = "active"
    return product


def upsert_relationship(db, company, product, item):
    rel = db.query(EntityRelationship).filter(
        EntityRelationship.source_type == "company",
        EntityRelationship.source_id == company.id,
        EntityRelationship.target_type == "product",
        EntityRelationship.target_id == product.id,
        EntityRelationship.relation_type == "manufactures",
    ).one_or_none()
    if not rel:
        rel = EntityRelationship(
            source_type="company",
            source_id=company.id,
            target_type="product",
            target_id=product.id,
            relation_type="manufactures",
        )
        db.add(rel)
    rel.evidence = SOURCE_NOTE
    rel.confidence_score = min(item["confidence"], 90)
    rel.source_url = item["source_url"]
    return rel


def main() -> None:
    db = SessionLocal()
    created_or_updated_companies = 0
    created_or_updated_products = 0
    created_or_updated_relationships = 0
    try:
        for item in OEM_DATA:
            company = upsert_company(db, item)
            created_or_updated_companies += 1
            for product_tuple in item["products"]:
                product = upsert_product(db, company, item, product_tuple)
                created_or_updated_products += 1
                upsert_relationship(db, company, product, item)
                created_or_updated_relationships += 1
        db.commit()
        print({
            "companies_upserted": created_or_updated_companies,
            "products_upserted": created_or_updated_products,
            "relationships_upserted": created_or_updated_relationships,
        })
    finally:
        db.close()


if __name__ == "__main__":
    main()

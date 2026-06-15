from app.db.session import SessionLocal
from app.models.opportunity import Opportunity
from app.services.scoring import compute_fit_score, compute_total_score

MOCK_ITEMS = [
    {
        "title": "某风电场运维备件轴承采购线索",
        "summary": "公开信息显示华北某风电场近期有运维备件采购需求，涉及主轴/齿轮箱相关轴承。",
        "opportunity_type": "维护服务",
        "industry": "风电",
        "company_name": "华北某新能源公司",
        "project_name": "风电场运维项目",
        "province": "河北省",
        "city": "张家口市",
        "latitude": 40.8244,
        "longitude": 114.8875,
        "bearing_types": {"items": ["主轴轴承", "齿轮箱轴承"]},
        "equipment_types": {"items": ["风电机组", "齿轮箱"]},
        "estimated_amount": "中",
        "volume_score": 75,
        "urgency_score": 70,
        "confidence_score": 65,
        "confidence_reason": "来源为公开运维/备件需求信息，具体型号需销售进一步核实。",
        "recommended_action": "联系区域销售核实项目业主和机型，优先确认齿轮箱备件计划。",
    },
    {
        "title": "钢铁企业轧机检修轴承潜在服务机会",
        "summary": "某钢铁企业发布检修信息，涉及轧线设备维护，可能存在轧机轴承更换或检测需求。",
        "opportunity_type": "项目",
        "industry": "钢铁",
        "company_name": "华东某钢铁集团",
        "project_name": "轧线检修项目",
        "province": "江苏省",
        "city": "南京市",
        "latitude": 32.0603,
        "longitude": 118.7969,
        "bearing_types": {"items": ["轧机轴承", "圆柱滚子轴承"]},
        "equipment_types": {"items": ["轧机", "连轧线"]},
        "estimated_amount": "高",
        "volume_score": 85,
        "urgency_score": 80,
        "confidence_score": 60,
        "confidence_reason": "检修信息可信，但是否明确采购轴承仍需二次验证。",
        "recommended_action": "优先联系售后团队确认检修窗口，准备轧机轴承备件和检测服务方案。",
    },
    {
        "title": "矿山设备维修岗位招聘反映轴承服务需求",
        "summary": "某矿业公司招聘设备维修工程师，岗位描述包含破碎机、输送机、旋转设备维护。",
        "opportunity_type": "招聘信号",
        "industry": "矿山",
        "company_name": "西北某矿业公司",
        "province": "陕西省",
        "city": "榆林市",
        "latitude": 38.2852,
        "longitude": 109.7346,
        "bearing_types": {"items": ["调心滚子轴承", "深沟球轴承"]},
        "equipment_types": {"items": ["破碎机", "输送机", "旋转设备"]},
        "estimated_amount": "中",
        "volume_score": 60,
        "urgency_score": 45,
        "confidence_score": 50,
        "confidence_reason": "招聘信息属于间接信号，说明维护能力或设备负荷增加，但采购需求未直接确认。",
        "recommended_action": "作为中期线索跟踪，结合企业项目和设备采购公告进一步验证。",
    },
]


def main():
    db = SessionLocal()
    try:
        if db.query(Opportunity).count() > 0:
            print("mock data skipped: opportunities already exist")
            return
        for item in MOCK_ITEMS:
            fit = compute_fit_score(item.get("industry"))
            total = compute_total_score(
                item["volume_score"], item["urgency_score"], item["confidence_score"], fit
            )
            db.add(Opportunity(**item, fit_score=fit, total_score=total))
        db.commit()
        print(f"inserted {len(MOCK_ITEMS)} mock opportunities")
    finally:
        db.close()


if __name__ == "__main__":
    main()

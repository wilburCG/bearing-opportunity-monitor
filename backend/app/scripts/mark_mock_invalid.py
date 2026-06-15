from app.db.session import SessionLocal
from app.models.opportunity import Opportunity

MOCK_TITLES = [
    '某风电场运维备件轴承采购线索',
    '钢铁企业轧机检修轴承潜在服务机会',
    '矿山设备维修岗位招聘反映轴承服务需求',
]

def main():
    db = SessionLocal()
    try:
        n = 0
        for title in MOCK_TITLES:
            item = db.query(Opportunity).filter(Opportunity.title == title).first()
            if item:
                item.status = 'invalid'
                n += 1
        db.commit()
        print({'marked_invalid': n})
    finally:
        db.close()

if __name__ == '__main__':
    main()

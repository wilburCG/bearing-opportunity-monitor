from app.db.session import SessionLocal
from app.models.opportunity import Opportunity

UPDATES = {
    'XWLH-26-06-05-001 Bearing Procurement for Refining and Chemical Operations': {
        'company_name': 'Refining and Chemical Buyer (to be verified)',
        'province': None,
        'city': None,
    },
    'XWLH-26-06-05-003 Bearing Procurement for Refining and Chemical Operations': {
        'company_name': 'Refining and Chemical Buyer (to be verified)',
        'province': None,
        'city': None,
    },
    'Hunan Salt Xiangli Salt Chemical SKF Bearing Framework Opportunity': {
        'company_name': 'Hunan Salt Group Co., Ltd.',
        'province': 'Hunan',
        'city': 'Changsha',
    },
    'Zhongfu Shenying Carbon Fiber Xining Bearing Procurement Lead': {
        'company_name': 'Zhongfu Shenying Carbon Fiber Xining Co., Ltd.',
        'province': 'Qinghai',
        'city': 'Xining',
    },
}

def main():
    db = SessionLocal()
    try:
        n=0
        for title, fields in UPDATES.items():
            item=db.query(Opportunity).filter(Opportunity.title==title).first()
            if item:
                for k,v in fields.items(): setattr(item,k,v)
                n+=1
        db.commit()
        print({'updated':n})
    finally:
        db.close()
if __name__=='__main__': main()

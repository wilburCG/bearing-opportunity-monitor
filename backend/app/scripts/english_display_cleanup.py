from app.db.session import SessionLocal
from app.models.opportunity import Opportunity

UPDATES = {
    '福建三钢闽光MRC轴承采购询价公告': {
        'title': 'Fujian Sangang Minguang MRC Bearing RFQ',
        'summary': 'Fujian Minguang Smart Tendering, commissioned by Fujian Sangang Minguang Co., Ltd., issued a public RFQ for MRC bearings. The list includes high-precision bearings and cylindrical roller bearings, with delivery required by 2026-08-15 and quotation deadline 2026-06-09 15:00.',
        'company_name': 'Fujian Sangang Minguang Co., Ltd.',
        'project_name': 'MRC Bearing Procurement',
        'province': 'Fujian',
        'city': 'Sanming',
        'confidence_reason': 'The source is a public RFQ on the Fugreenpine trading platform. It provides the RFQ number, buyer, item list, bearing models, quantities, delivery date, quotation deadline, qualification requirements, and contact information.',
        'recommended_action': 'Treat as the top-priority verified lead. Check MRC contract references, stock and delivery capability for listed models, and prepare platform registration and sealed qualification documents.'
    },
    '鲁西集团FAG轴承询价单20260603': {
        'title': 'Luxi Group FAG Bearing RFQ 20260603',
        'summary': 'Zhiliaobiaoxun shows a Luxi Group FAG bearing RFQ, project number RFQ2606030009. The item is bearing-related, quantity 2 pieces/plates, required by 2026-06-06, with online banking payment and 13% VAT invoice terms.',
        'company_name': 'Luxi Group',
        'project_name': 'FAG Bearing RFQ 20260603',
        'province': 'Beijing',
        'city': 'Beijing',
        'confidence_reason': 'The source is an aggregation page with project name, project number, buyer, release time, deadline, item category, quantity, and payment terms. Specific model and technical requirements require login verification.',
        'recommended_action': 'Verify the original procurement platform for the exact FAG model and technical requirements. If the current RFQ is closed, use it as a recurring-demand signal and monitor Luxi Group SKF/FAG bearing RFQs.'
    },
}

HIDE_TITLES = ['2025年12月铁姆肯轴承采购询价公告']


def main():
    db = SessionLocal()
    try:
        updated = 0
        hidden = 0
        for old_title, fields in UPDATES.items():
            item = db.query(Opportunity).filter(Opportunity.title == old_title).first()
            if item:
                for k, v in fields.items():
                    setattr(item, k, v)
                updated += 1
        for title in HIDE_TITLES:
            item = db.query(Opportunity).filter(Opportunity.title == title).first()
            if item:
                item.status = 'invalid'
                hidden += 1
        db.commit()
        print({'updated_english': updated, 'hidden_non_2026': hidden})
    finally:
        db.close()

if __name__ == '__main__':
    main()

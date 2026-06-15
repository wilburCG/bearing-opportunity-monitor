"""Backfill latitude/longitude for opportunities.

Usage:
  docker compose exec -T backend python -m app.scripts.geocode_opportunities
  docker compose exec -T backend python -m app.scripts.geocode_opportunities --all

Without --all only records missing coordinates are geocoded. With --all, existing
coordinates are refreshed as well.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime

from app.db.session import SessionLocal
from app.models.opportunity import Opportunity
from app.services.geocoding import geocode_opportunity_location


async def main(refresh_all: bool = False):
    db = SessionLocal()
    updated = 0
    skipped = 0
    failed = 0
    items = []
    try:
        query = db.query(Opportunity).filter(Opportunity.status != 'invalid')
        if not refresh_all:
            query = query.filter((Opportunity.latitude.is_(None)) | (Opportunity.longitude.is_(None)))
        rows = query.order_by(Opportunity.id.asc()).all()

        for item in rows:
            result = await geocode_opportunity_location(
                province=item.province,
                city=item.city,
                district=item.district,
                address=item.address,
                company_name=item.company_name,
                title=item.title,
            )
            if not result:
                failed += 1
                items.append({'id': item.id, 'title': item.title, 'status': 'failed'})
                continue

            if item.latitude == result.latitude and item.longitude == result.longitude:
                skipped += 1
                items.append({
                    'id': item.id,
                    'title': item.title,
                    'status': 'unchanged',
                    'source': result.source,
                    'matched_name': result.matched_name,
                    'latitude': result.latitude,
                    'longitude': result.longitude,
                })
                continue

            item.latitude = result.latitude
            item.longitude = result.longitude
            item.updated_at = datetime.utcnow()
            updated += 1
            items.append({
                'id': item.id,
                'title': item.title,
                'status': 'updated',
                'source': result.source,
                'matched_name': result.matched_name,
                'latitude': result.latitude,
                'longitude': result.longitude,
            })

        db.commit()
        print(json.dumps({
            'updated': updated,
            'skipped': skipped,
            'failed': failed,
            'items': items,
        }, ensure_ascii=False, indent=2))
    finally:
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='refresh existing coordinates too')
    args = parser.parse_args()
    asyncio.run(main(refresh_all=args.all))

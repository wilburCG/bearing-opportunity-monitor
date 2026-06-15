'use client';

import { getLocationCoordinates } from '@/lib/geo';
import type { Company, Opportunity } from '@/types/opportunity';
import { Card, Typography } from 'antd';
import dynamic from 'next/dynamic';

export type MapDisplayMode = 'opportunities' | 'companies' | 'all';

interface Props {
  data: Opportunity[];
  companies?: Company[];
  onSelect: (id: number) => void;
  onCompanySelect?: (id: number) => void;
}

const LeafletMap = dynamic(() => import('./OpportunityMapLeaflet'), {
  ssr: false,
  loading: () => <MapFallback data={[]} companies={[]} onSelect={() => {}} loading />,
});

function opportunityHasCoordinates(item: Opportunity) {
  return item.latitude !== null && item.latitude !== undefined && item.longitude !== null && item.longitude !== undefined;
}

function companyHasCoordinates(item: Company) {
  return Boolean(getLocationCoordinates(item.province, item.city));
}

export default function OpportunityMap({ data, companies = [], onSelect, onCompanySelect }: Props) {
  const validOpportunities = data.filter(opportunityHasCoordinates);
  const validCompanies = companies.filter(companyHasCoordinates);

  if (validOpportunities.length > 0 || validCompanies.length > 0) {
    return <LeafletMap data={data} companies={companies} onSelect={onSelect} onCompanySelect={onCompanySelect} />;
  }

  return <MapFallback data={[]} companies={[]} onSelect={onSelect} />;
}

export function MapFallback({ data, companies = [], onSelect, loading = false }: Props & { loading?: boolean }) {
  const opportunityPoints = data
    .filter(opportunityHasCoordinates)
    .map((item) => ({
      id: `opportunity:${item.id}`,
      label: `${item.city || item.province || 'Opportunity'} · ${item.total_score}`,
      latitude: item.latitude as number,
      longitude: item.longitude as number,
      onClick: () => onSelect(item.id),
    }));
  const companyPoints = companies
    .map((item) => {
      const coords = getLocationCoordinates(item.province, item.city);
      if (!coords) return null;
      return {
        id: `company:${item.id}`,
        label: `${item.name} · 企业`,
        latitude: coords.latitude,
        longitude: coords.longitude,
        onClick: () => {},
      };
    })
    .filter((item): item is NonNullable<typeof item> => Boolean(item));
  const valid = [...opportunityPoints, ...companyPoints];
  const minLng = Math.min(...valid.map((item) => item.longitude), 73);
  const maxLng = Math.max(...valid.map((item) => item.longitude), 135);
  const minLat = Math.min(...valid.map((item) => item.latitude), 18);
  const maxLat = Math.max(...valid.map((item) => item.latitude), 54);

  return (
    <Card styles={{ body: { padding: 0 } }}>
      <div className="map-fallback world-map-bg" style={{ height: 645, borderRadius: 16 }}>
        <div className="map-grid" />
        <div className="map-label">Offline map fallback · markers remain interactive</div>
        {loading && <Typography.Text className="map-loading">Loading map...</Typography.Text>}
        {!loading && valid.length === 0 && (
          <Typography.Text className="map-loading">No geocoded opportunities or companies yet.</Typography.Text>
        )}
        {valid.map((item) => {
          const x = ((item.longitude - minLng) / Math.max(maxLng - minLng, 1)) * 78 + 11;
          const y = (1 - ((item.latitude - minLat) / Math.max(maxLat - minLat, 1))) * 68 + 20;
          return (
            <button
              key={item.id}
              className="map-point"
              style={{ left: `${x}%`, top: `${y}%` }}
              onClick={item.onClick}
            >
              {item.label}
            </button>
          );
        })}
      </div>
    </Card>
  );
}

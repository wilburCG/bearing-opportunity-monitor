'use client';

import { getLocationCoordinates } from '@/lib/geo';
import { scoreColor } from '@/lib/format';
import type { Company, Opportunity } from '@/types/opportunity';
import L from 'leaflet';
import { MapContainer, Marker, Popup, TileLayer, useMap } from 'react-leaflet';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { MapFallback } from './OpportunityMap';
import type { MapDisplayMode } from './OpportunityMap';

interface Props {
  data: Opportunity[];
  companies?: Company[];
  onSelect: (id: number) => void;
  onCompanySelect?: (id: number) => void;
}

type MapLevel = 'province' | 'city' | 'company';

type MapPoint = {
  key: string;
  label: string;
  count: number;
  latitude: number;
  longitude: number;
  items: Opportunity[];
};

const PROVINCE_ALIASES: Record<string, string> = {
  北京: '北京市', 北京市: '北京市',
  上海: '上海市', 上海市: '上海市',
  天津: '天津市', 天津市: '天津市',
  重庆: '重庆市', 重庆市: '重庆市',
  全国: '全国',
};

const MUNICIPALITIES = new Set(['北京市', '上海市', '天津市', '重庆市']);

function canonicalProvince(value?: string | null) {
  if (!value) return undefined;
  return PROVINCE_ALIASES[value.trim()] || value.trim();
}

function hasCoordinates(item: Opportunity) {
  return item.latitude !== null && item.latitude !== undefined && item.longitude !== null && item.longitude !== undefined;
}

function getPlottableData(data: Opportunity[]) {
  return data.filter(hasCoordinates);
}

function normalizeProvince(item: Opportunity) {
  return canonicalProvince(item.province) || canonicalProvince(item.city) || 'Unknown Province';
}

function normalizeCity(item: Opportunity) {
  const province = normalizeProvince(item);
  let raw = (item.city || item.province || 'Unknown City').trim();
  if (MUNICIPALITIES.has(province)) return province;
  if (raw.startsWith(province)) raw = raw.slice(province.length) || raw;
  const shortProvince = province.replace(/省|市|壮族自治区|回族自治区|维吾尔自治区|自治区/g, '');
  if (shortProvince && raw.startsWith(shortProvince)) raw = raw.slice(shortProvince.length) || raw;
  if (/^[\u4e00-\u9fa5]{2,6}$/.test(raw) && !/(市|州|地区|盟|县|区)$/.test(raw)) {
    return `${raw}市`;
  }
  return raw;
}

function escapeHtml(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function averagePosition(items: Opportunity[]): [number, number] {
  const valid = getPlottableData(items);
  const lat = valid.reduce((sum, item) => sum + (item.latitude as number), 0) / valid.length;
  const lng = valid.reduce((sum, item) => sum + (item.longitude as number), 0) / valid.length;
  return [lat, lng];
}

function groupItems(items: Opportunity[], getKey: (item: Opportunity) => string, getLabel: (item: Opportunity) => string): MapPoint[] {
  const groups = new Map<string, Opportunity[]>();
  items.forEach((item) => {
    const key = getKey(item);
    const bucket = groups.get(key) || [];
    bucket.push(item);
    groups.set(key, bucket);
  });
  return Array.from(groups.entries())
    .map(([key, bucket]) => {
      const valid = getPlottableData(bucket);
      if (valid.length === 0) return null;
      const [latitude, longitude] = averagePosition(valid);
      return { key, label: getLabel(bucket[0]), count: bucket.length, latitude, longitude, items: bucket };
    })
    .filter((point): point is MapPoint => Boolean(point))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
}

function spreadSamePosition<T>(item: T, index: number, all: T[], getLatLng: (value: T) => [number, number], getId: (value: T) => string | number): [number, number] {
  const [lat, lng] = getLatLng(item);
  const sameLocation = all.filter((other) => {
    const [otherLat, otherLng] = getLatLng(other);
    return otherLat === lat && otherLng === lng;
  });
  const sameIndex = sameLocation.findIndex((other) => getId(other) === getId(item));
  if (sameLocation.length <= 1 || sameIndex < 0) return [lat, lng];
  const angle = (2 * Math.PI * sameIndex) / sameLocation.length;
  const radius = 0.22 + Math.floor(sameIndex / 8) * 0.1;
  return [lat + Math.sin(angle) * radius, lng + Math.cos(angle) * radius];
}

function getDisplayPosition(item: Opportunity, index: number, all: Opportunity[]): [number, number] {
  return spreadSamePosition(item, index, all, (value) => [value.latitude as number, value.longitude as number], (value) => value.id);
}

function getPointDisplayPosition(point: MapPoint, index: number, all: MapPoint[]): [number, number] {
  return spreadSamePosition(point, index, all, (value) => [value.latitude, value.longitude], (value) => value.key);
}

function companyPoints(companies: Company[]) {
  return companies
    .map((c) => {
      const coords = getLocationCoordinates(c.province, c.city);
      if (!coords) return null;
      return { id: c.id, name: c.name, company: c, ...coords };
    })
    .filter((item): item is NonNullable<typeof item> => Boolean(item));
}

function IndustryMapContainer({ data, companies = [], onSelect, onCompanySelect }: Props) {
  const [tileReady, setTileReady] = useState(false);
  const [tileFailed, setTileFailed] = useState(false);
  const [displayMode, setDisplayMode] = useState<MapDisplayMode>('opportunities');
  const center: [number, number] = [35.8617, 104.1954];
  const plottable = useMemo(() => getPlottableData(data), [data]);
  const companyPts = useMemo(() => companyPoints(companies), [companies]);
  const markReady = useCallback(() => setTileReady(true), []);
  const markFailed = useCallback(() => setTileFailed(true), []);

  const modeOptions: { key: MapDisplayMode; label: string }[] = [
    { key: 'opportunities', label: '📍 Opportunities' },
    { key: 'companies', label: '🏢 Companies' },
    { key: 'all', label: '📊 All' },
  ];

  return (
    <div style={{ position: 'relative', height: 645, borderRadius: 16, overflow: 'hidden' }}>
      {(!tileReady || tileFailed) && (
        <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
          <MapFallback data={data} companies={companies} onSelect={onSelect} loading={!tileFailed && !tileReady} />
        </div>
      )}
      <div style={{ position: 'absolute', right: 12, top: 12, zIndex: 3, background: 'rgba(255,255,255,.94)', borderRadius: 12, padding: '8px 10px', boxShadow: '0 6px 18px rgba(15,23,42,.12)', fontSize: 13, display: 'flex', flexDirection: 'column', gap: 6, minWidth: 180 }}>
        <strong style={{ marginBottom: 4 }}>Map Mode</strong>
        {modeOptions.map((opt) => (
          <button
            key={opt.key}
            type="button"
            style={{
              background: displayMode === opt.key ? '#3b82f6' : '#f1f5f9',
              color: displayMode === opt.key ? '#fff' : '#0f172a',
              border: 'none',
              borderRadius: 8,
              padding: '5px 10px',
              cursor: 'pointer',
              fontWeight: displayMode === opt.key ? 700 : 500,
              fontSize: 12,
            }}
            onClick={() => setDisplayMode(opt.key)}
          >
            {opt.label}
          </button>
        ))}
        <div style={{ borderTop: '1px solid #e2e8f0', marginTop: 4, paddingTop: 6, fontSize: 11, color: '#64748b' }}>
          {displayMode === 'opportunities' && `Mapped ${plottable.length}/${data.length}`}
          {displayMode === 'companies' && `Mapped ${companyPts.length}/${companies.length}`}
          {displayMode === 'all' && `Opportunities ${plottable.length} · Companies ${companyPts.length}`}
        </div>
      </div>
      <div style={{ position: 'absolute', inset: 0, zIndex: tileReady && !tileFailed ? 1 : 0, opacity: tileReady && !tileFailed ? 1 : 0.01 }}>
        <MapContainer key={`${displayMode}:${data.length}:${companies.length}`} center={center} zoom={4} style={{ height: '100%', width: '100%' }} scrollWheelZoom>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://tile.openstreetmap.de/{z}/{x}/{y}.png"
            eventHandlers={{
              load: markReady,
              tileload: markReady,
              tileerror: markFailed,
            }}
          />

          {/* Opportunity province aggregates */}
          {(displayMode === 'opportunities' || displayMode === 'all') && plottable.length > 0 && (
            <>
              {groupItems(plottable, normalizeProvince, normalizeProvince).map((point, idx) => (
                <Marker key={`opp-prov-${point.key}`} position={getPointDisplayPosition(point, idx, groupItems(plottable, normalizeProvince, normalizeProvince))}
                  icon={(() => {
                    const size = Math.min(48, 28 + Math.log2(point.count + 1) * 7);
                    const color = point.count >= 20 ? '#b91c1c' : point.count >= 10 ? '#ea580c' : point.count >= 5 ? '#d97706' : '#2563eb';
                    return L.divIcon({
                      html: `<div style="transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:4px;"><div style="width:${size}px;height:${size}px;border-radius:999px;background:${color};color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;box-shadow:0 8px 18px rgba(15,23,42,.24);border:2px solid rgba(255,255,255,.9);">${point.count}</div><div style="background:rgba(255,255,255,.94);color:#0f172a;border-radius:999px;padding:3px 8px;font-size:12px;font-weight:700;white-space:nowrap;">${escapeHtml(point.label)} · Opps</div></div>`,
                      className: '', iconSize: [1, 1], iconAnchor: [0, 0],
                    });
                  })()}
                >
                  <Popup><strong>{point.label}</strong><br />Opportunities: {point.count}</Popup>
                </Marker>
              ))}
            </>
          )}

          {/* Company markers with city-level coordinates */}
          {(displayMode === 'companies' || displayMode === 'all') && companyPts.map((pt, idx) => (
            <Marker key={`company-${pt.id}`}
              position={spreadSamePosition(pt, idx, companyPts, (v) => [v.latitude, v.longitude], (v) => `c${v.id}`)}
              eventHandlers={{ click: () => onCompanySelect?.(pt.id) }}
              icon={L.divIcon({
                html: `<div style="background:${pt.company.company_type === 'manufacturer' ? '#059669' : pt.company.company_type === 'supplier' ? '#8b5cf6' : '#2563eb'};color:white;border-radius:16px;padding:5px 10px;font-size:12px;font-weight:600;box-shadow:0 6px 18px rgba(0,0,0,.25);white-space:nowrap;">🏢 ${escapeHtml(pt.name)}</div>`,
                className: '', iconSize: [180, 28], iconAnchor: [90, 14],
              })}
            >
              <Popup>
                <strong>{pt.name}</strong><br />
                {pt.company.company_type || '-'}<br />
                {[pt.company.province, pt.company.city].filter(Boolean).join(' ') || '-'}<br />
                {pt.company.website && <a href={pt.company.website} target="_blank" rel="noopener noreferrer">Website</a>}<br />
                Confidence: {pt.company.confidence_score}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default IndustryMapContainer;
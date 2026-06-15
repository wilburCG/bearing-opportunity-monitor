'use client';

import AgentChat from '@/components/AgentChat';
import OpportunityDetailDrawer from '@/components/OpportunityDetailDrawer';
import OpportunityMap from '@/components/OpportunityMap';
import { getIndustryGraph, listCompanies, listOpportunities, listProducts, listRelationships } from '@/lib/api';
import { industryLabel, opportunityTypeLabel, scoreColor, statusColor, statusLabel } from '@/lib/format';
import type { Company, EntityRelationship, IndustryGraph, Opportunity, Product } from '@/types/opportunity';
import { AimOutlined, ApartmentOutlined, FilterOutlined, ReloadOutlined } from '@ant-design/icons';
import { App, Button, Card, Col, Descriptions, Drawer, Empty, Input, InputNumber, Layout, Row, Select, Space, Statistic, Table, Tabs, Tag, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import type { ReactNode } from 'react';
import { useEffect, useMemo, useState } from 'react';

const { Header, Content } = Layout;

type OpportunityFilters = {
  industry?: string;
  opportunityType?: string;
  status?: string;
  minScore?: number;
  maxScore?: number;
  minUrgency?: number;
  maxUrgency?: number;
  minConfidence?: number;
  maxConfidence?: number;
};

type CompanyFilters = {
  q?: string;
  industry?: string;
  companyType?: string;
  province?: string;
  city?: string;
  status?: string;
  minConfidence?: number;
  maxConfidence?: number;
};

type ProductFilters = {
  q?: string;
  industry?: string;
  category?: string;
  manufacturerName?: string;
  status?: string;
  minConfidence?: number;
  maxConfidence?: number;
};

type RelationshipFilters = {
  entityType?: string;
  sourceType?: string;
  targetType?: string;
  relationType?: string;
  minConfidence?: number;
  maxConfidence?: number;
};

type ActiveTab = 'opportunities' | 'companies' | 'products' | 'relationships';

const industries = [
  { value: '风电', label: 'Wind Power' },
  { value: '钢铁', label: 'Steel' },
  { value: '矿山', label: 'Mining' },
  { value: '水泥', label: 'Cement' },
  { value: '轨交', label: 'Rail Transit' },
  { value: '化工', label: 'Chemical' },
  { value: '数据中心', label: 'Data Center' },
  { value: '破碎筛分', label: 'Crushing & Screening' },
  { value: '砂石骨料', label: 'Aggregates' },
];

const opportunityTypes = [
  { value: '询价', label: 'RFQ' },
  { value: '采购', label: 'Procurement' },
  { value: '招标', label: 'Tender' },
  { value: '项目', label: 'Project' },
  { value: 'early_signal', label: 'Early Signal' },
  { value: '招聘信号', label: 'Hiring Signal' },
  { value: '维护服务', label: 'Maintenance Service' },
];

const opportunityStatuses = [
  { value: 'new', label: 'New' },
  { value: 'pending_verify', label: 'Pending Verification' },
  { value: 'followed', label: 'Followed Up' },
  { value: 'converted', label: 'Converted' },
  { value: 'invalid', label: 'Invalid' },
];

const entityStatuses = [
  { value: 'active', label: 'Active' },
  { value: 'inactive', label: 'Inactive' },
  { value: 'deleted', label: 'Deleted' },
];

const companyTypes = [
  { value: 'oem', label: 'OEM' },
  { value: 'owner', label: 'Owner / Buyer' },
  { value: 'buyer', label: 'Buyer' },
  { value: 'manufacturer', label: 'Manufacturer' },
  { value: 'integrator', label: 'Integrator' },
  { value: 'competitor', label: 'Competitor' },
  { value: 'distributor', label: 'Distributor' },
  { value: 'supplier', label: 'Supplier' },
];

const productCategories = [
  { value: '轴承', label: 'Bearing' },
  { value: '调心滚子轴承', label: 'Spherical Roller Bearing' },
  { value: '圆锥滚子轴承', label: 'Tapered Roller Bearing' },
  { value: '深沟球轴承', label: 'Deep Groove Ball Bearing' },
  { value: '破碎机', label: 'Crusher' },
  { value: '筛分设备', label: 'Screening Equipment' },
  { value: '风电主轴', label: 'Wind Turbine Main Shaft' },
];

const entityTypes = [
  { value: 'company', label: 'Company' },
  { value: 'product', label: 'Product' },
  { value: 'opportunity', label: 'Opportunity' },
];

const relationTypes = [
  { value: 'manufactures', label: 'Manufactures' },
  { value: 'mentions', label: 'Mentions' },
  { value: 'buys', label: 'Buys' },
  { value: 'supplies', label: 'Supplies' },
  { value: 'competes', label: 'Competes' },
  { value: 'used_in', label: 'Used In' },
  { value: 'related_to', label: 'Related To' },
];

const scorePresets = [
  { value: '80-100', label: 'Score: High ≥ 80' },
  { value: '70-100', label: 'Score: Priority ≥ 70' },
  { value: '60-69.99', label: 'Score: Medium 60-69' },
  { value: '0-59.99', label: 'Score: Low < 60' },
];

const confidencePresets = [
  { value: '80-100', label: 'Confidence: High ≥ 80' },
  { value: '60-79.99', label: 'Confidence: Medium 60-79' },
  { value: '0-59.99', label: 'Confidence: Low < 60' },
];

const urgencyPresets = [
  { value: '80-100', label: 'Urgency: Urgent ≥ 80' },
  { value: '60-79.99', label: 'Urgency: Watch 60-79' },
  { value: '0-59.99', label: 'Urgency: Later < 60' },
];

function parseRange(value?: string) {
  if (!value) return [undefined, undefined] as const;
  const [min, max] = value.split('-').map(Number);
  return [Number.isFinite(min) ? min : undefined, Number.isFinite(max) ? max : undefined] as const;
}

function rangeValue(min?: number, max?: number) {
  if (min === undefined && max === undefined) return undefined;
  return `${min ?? 0}-${max ?? 100}`;
}

function FilterField({ label, children }: { label: string; children: ReactNode }) {
  return (
    <Space direction="vertical" size={4} style={{ minWidth: 120 }}>
      <Typography.Text type="secondary" style={{ fontSize: 12, lineHeight: '16px' }}>{label}</Typography.Text>
      {children}
    </Space>
  );
}

export default function HomePage() {
  const { message } = App.useApp();
  const [data, setData] = useState<Opportunity[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [relationships, setRelationships] = useState<EntityRelationship[]>([]);
  const [graph, setGraph] = useState<IndustryGraph | null>(null);
  const [loading, setLoading] = useState(false);
  const [industryLoading, setIndustryLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<ActiveTab>('opportunities');
  const [opportunityFilters, setOpportunityFilters] = useState<OpportunityFilters>({});
  const [companyFilters, setCompanyFilters] = useState<CompanyFilters>({});
  const [productFilters, setProductFilters] = useState<ProductFilters>({});
  const [relationshipFilters, setRelationshipFilters] = useState<RelationshipFilters>({});
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [selectedCompanyId, setSelectedCompanyId] = useState<number | null>(null);

  function updateOpportunityFilter<K extends keyof OpportunityFilters>(key: K, value: OpportunityFilters[K]) {
    setOpportunityFilters((prev) => ({ ...prev, [key]: value }));
  }

  function updateCompanyFilter<K extends keyof CompanyFilters>(key: K, value: CompanyFilters[K]) {
    setCompanyFilters((prev) => ({ ...prev, [key]: value }));
  }

  function updateProductFilter<K extends keyof ProductFilters>(key: K, value: ProductFilters[K]) {
    setProductFilters((prev) => ({ ...prev, [key]: value }));
  }

  function updateRelationshipFilter<K extends keyof RelationshipFilters>(key: K, value: RelationshipFilters[K]) {
    setRelationshipFilters((prev) => ({ ...prev, [key]: value }));
  }

  function clearActiveFilters() {
    if (activeTab === 'opportunities') setOpportunityFilters({});
    if (activeTab === 'companies') setCompanyFilters({});
    if (activeTab === 'products') setProductFilters({});
    if (activeTab === 'relationships') setRelationshipFilters({});
  }

  async function load() {
    setLoading(true);
    try {
      const items = await listOpportunities({
        industry: opportunityFilters.industry,
        opportunity_type: opportunityFilters.opportunityType,
        status: opportunityFilters.status,
        min_score: opportunityFilters.minScore,
        max_score: opportunityFilters.maxScore,
        min_urgency: opportunityFilters.minUrgency,
        max_urgency: opportunityFilters.maxUrgency,
        min_confidence: opportunityFilters.minConfidence,
        max_confidence: opportunityFilters.maxConfidence,
        limit: 300,
      });
      setData(items);
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Failed to load opportunities');
    } finally {
      setLoading(false);
    }
  }

  async function loadIndustryData() {
    setIndustryLoading(true);
    try {
      const [companyItems, productItems, relationshipItems, graphData] = await Promise.all([
        listCompanies({
          q: companyFilters.q,
          industry: companyFilters.industry,
          company_type: companyFilters.companyType,
          province: companyFilters.province,
          city: companyFilters.city,
          status: companyFilters.status,
          min_confidence: companyFilters.minConfidence,
          max_confidence: companyFilters.maxConfidence,
          limit: 300,
        }),
        listProducts({
          q: productFilters.q,
          industry: productFilters.industry,
          category: productFilters.category,
          manufacturer_name: productFilters.manufacturerName,
          status: productFilters.status,
          min_confidence: productFilters.minConfidence,
          max_confidence: productFilters.maxConfidence,
          limit: 300,
        }),
        listRelationships({
          entity_type: relationshipFilters.entityType,
          source_type: relationshipFilters.sourceType,
          target_type: relationshipFilters.targetType,
          relation_type: relationshipFilters.relationType,
          min_confidence: relationshipFilters.minConfidence,
          max_confidence: relationshipFilters.maxConfidence,
          limit: 300,
        }),
        getIndustryGraph({
          entity_type: relationshipFilters.entityType,
          source_type: relationshipFilters.sourceType,
          target_type: relationshipFilters.targetType,
          relation_type: relationshipFilters.relationType,
          min_confidence: relationshipFilters.minConfidence,
          max_confidence: relationshipFilters.maxConfidence,
          limit: 300,
        }),
      ]);
      setCompanies(companyItems);
      setProducts(productItems);
      setRelationships(relationshipItems);
      setGraph(graphData);
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Failed to load industry entities');
    } finally {
      setIndustryLoading(false);
    }
  }

  useEffect(() => { load(); }, [opportunityFilters]);
  useEffect(() => { loadIndustryData(); }, [companyFilters, productFilters, relationshipFilters]);

  const stats = useMemo(() => {
    const high = data.filter((item) => item.total_score >= 70).length;
    const urgent = data.filter((item) => item.urgency_score >= 80).length;
    const avg = data.length ? data.reduce((sum, item) => sum + item.total_score, 0) / data.length : 0;
    return { total: data.length, high, urgent, avg: avg.toFixed(1) };
  }, [data]);

  const columns: ColumnsType<Opportunity> = [
    {
      title: 'Opportunity',
      dataIndex: 'title',
      render: (_, record) => (
        <Space direction="vertical" size={2}>
          <Button type="link" style={{ padding: 0, height: 'auto', whiteSpace: 'normal', textAlign: 'left' }} onClick={() => setSelectedId(record.id)}>
            {record.title}
          </Button>
          <Typography.Text type="secondary">{record.company_name || '-'} · {[record.province, record.city].filter(Boolean).join(' ')}</Typography.Text>
        </Space>
      ),
    },
    { title: 'Industry', dataIndex: 'industry', width: 130, render: (value) => <Tag>{industryLabel(value)}</Tag> },
    { title: 'Type', dataIndex: 'opportunity_type', width: 140, render: (value) => opportunityTypeLabel(value) },
    {
      title: 'Score',
      dataIndex: 'total_score',
      width: 100,
      sorter: (a, b) => a.total_score - b.total_score,
      defaultSortOrder: 'descend',
      render: (value) => <span><span className="score-dot" style={{ background: scoreColor(value) }} />{value}</span>,
    },
    { title: 'Urgency', dataIndex: 'urgency_score', width: 100, sorter: (a, b) => a.urgency_score - b.urgency_score },
    { title: 'Confidence', dataIndex: 'confidence_score', width: 120, sorter: (a, b) => a.confidence_score - b.confidence_score },
    { title: 'Status', dataIndex: 'status', width: 150, render: (value) => <Tag color={statusColor(value)}>{statusLabel(value)}</Tag> },
  ];

  const companyColumns: ColumnsType<Company> = [
    { title: 'Company', dataIndex: 'name', render: (value, record) => <Space direction="vertical" size={2}><Typography.Text strong>{value}</Typography.Text><Typography.Text type="secondary">{record.description || '-'}</Typography.Text></Space> },
    { title: 'Type', dataIndex: 'company_type', width: 130, render: (value) => value || '-' },
    { title: 'Industry', dataIndex: 'industry', width: 130, render: (value) => <Tag>{industryLabel(value)}</Tag> },
    { title: 'Location', width: 160, render: (_, record) => [record.province, record.city].filter(Boolean).join(' ') || '-' },
    { title: 'Confidence', dataIndex: 'confidence_score', width: 120 },
    { title: 'Status', dataIndex: 'status', width: 110, render: (value) => <Tag>{value}</Tag> },
  ];

  const productColumns: ColumnsType<Product> = [
    { title: 'Product', dataIndex: 'name', render: (value, record) => <Space direction="vertical" size={2}><Typography.Text strong>{value}</Typography.Text><Typography.Text type="secondary">{record.description || '-'}</Typography.Text></Space> },
    { title: 'Model', dataIndex: 'model', width: 140, render: (value) => value || '-' },
    { title: 'Category', dataIndex: 'category', width: 130, render: (value) => value || '-' },
    { title: 'Manufacturer', dataIndex: 'manufacturer_name', width: 180, render: (value) => value || '-' },
    { title: 'Industry', dataIndex: 'industry', width: 130, render: (value) => <Tag>{industryLabel(value)}</Tag> },
    { title: 'Confidence', dataIndex: 'confidence_score', width: 120 },
  ];

  const relationshipColumns: ColumnsType<EntityRelationship> = [
    { title: 'Source', width: 150, render: (_, record) => `${record.source_type}:${record.source_id}` },
    { title: 'Relation', dataIndex: 'relation_type', width: 160, render: (value) => <Tag color="blue">{value}</Tag> },
    { title: 'Target', width: 150, render: (_, record) => `${record.target_type}:${record.target_id}` },
    { title: 'Evidence', dataIndex: 'evidence', render: (value) => value || '-' },
    { title: 'Confidence', dataIndex: 'confidence_score', width: 120 },
  ];

  const opportunityFilterPanel = (
    <Space wrap align="end" size={[12, 12]}>
      <FilterField label="Industry">
        <Select allowClear placeholder="Select industry" style={{ width: 150 }} options={industries} value={opportunityFilters.industry} onChange={(value) => updateOpportunityFilter('industry', value)} />
      </FilterField>
      <FilterField label="Opportunity Type">
        <Select allowClear placeholder="Select type" style={{ width: 170 }} options={opportunityTypes} value={opportunityFilters.opportunityType} onChange={(value) => updateOpportunityFilter('opportunityType', value)} />
      </FilterField>
      <FilterField label="Score Range">
        <Select
          allowClear
          placeholder="Select score"
          style={{ width: 175 }}
          options={scorePresets}
          value={rangeValue(opportunityFilters.minScore, opportunityFilters.maxScore)}
          onChange={(value) => {
            const [min, max] = parseRange(value);
            setOpportunityFilters((prev) => ({ ...prev, minScore: min, maxScore: max }));
          }}
        />
      </FilterField>
      <FilterField label="Min Score">
        <InputNumber min={0} max={100} placeholder="0-100" style={{ width: 112 }} value={opportunityFilters.minScore} onChange={(value) => updateOpportunityFilter('minScore', value ?? undefined)} />
      </FilterField>
      <FilterField label="Max Score">
        <InputNumber min={0} max={100} placeholder="0-100" style={{ width: 112 }} value={opportunityFilters.maxScore} onChange={(value) => updateOpportunityFilter('maxScore', value ?? undefined)} />
      </FilterField>
      <FilterField label="Urgency Range">
        <Select
          allowClear
          placeholder="Select urgency"
          style={{ width: 180 }}
          options={urgencyPresets}
          value={rangeValue(opportunityFilters.minUrgency, opportunityFilters.maxUrgency)}
          onChange={(value) => {
            const [min, max] = parseRange(value);
            setOpportunityFilters((prev) => ({ ...prev, minUrgency: min, maxUrgency: max }));
          }}
        />
      </FilterField>
      <FilterField label="Confidence Range">
        <Select
          allowClear
          placeholder="Select confidence"
          style={{ width: 205 }}
          options={confidencePresets}
          value={rangeValue(opportunityFilters.minConfidence, opportunityFilters.maxConfidence)}
          onChange={(value) => {
            const [min, max] = parseRange(value);
            setOpportunityFilters((prev) => ({ ...prev, minConfidence: min, maxConfidence: max }));
          }}
        />
      </FilterField>
      <FilterField label="Status">
        <Select allowClear placeholder="Select status" style={{ width: 180 }} options={opportunityStatuses} value={opportunityFilters.status} onChange={(value) => updateOpportunityFilter('status', value)} />
      </FilterField>
      <Button onClick={clearActiveFilters}>Clear</Button>
    </Space>
  );

  const companyFilterPanel = (
    <Space wrap align="end" size={[12, 12]}>
      <FilterField label="Keyword">
        <Input allowClear placeholder="Name / desc / city" style={{ width: 180 }} value={companyFilters.q} onChange={(event) => updateCompanyFilter('q', event.target.value || undefined)} />
      </FilterField>
      <FilterField label="Industry">
        <Select allowClear placeholder="Select industry" style={{ width: 150 }} options={industries} value={companyFilters.industry} onChange={(value) => updateCompanyFilter('industry', value)} />
      </FilterField>
      <FilterField label="Company Type">
        <Select allowClear placeholder="Select type" style={{ width: 170 }} options={companyTypes} value={companyFilters.companyType} onChange={(value) => updateCompanyFilter('companyType', value)} />
      </FilterField>
      <FilterField label="Province">
        <Input allowClear placeholder="Province" style={{ width: 130 }} value={companyFilters.province} onChange={(event) => updateCompanyFilter('province', event.target.value || undefined)} />
      </FilterField>
      <FilterField label="City">
        <Input allowClear placeholder="City" style={{ width: 120 }} value={companyFilters.city} onChange={(event) => updateCompanyFilter('city', event.target.value || undefined)} />
      </FilterField>
      <FilterField label="Confidence Range">
        <Select
          allowClear
          placeholder="Select confidence"
          style={{ width: 205 }}
          options={confidencePresets}
          value={rangeValue(companyFilters.minConfidence, companyFilters.maxConfidence)}
          onChange={(value) => {
            const [min, max] = parseRange(value);
            setCompanyFilters((prev) => ({ ...prev, minConfidence: min, maxConfidence: max }));
          }}
        />
      </FilterField>
      <FilterField label="Status">
        <Select allowClear placeholder="Select status" style={{ width: 140 }} options={entityStatuses} value={companyFilters.status} onChange={(value) => updateCompanyFilter('status', value)} />
      </FilterField>
      <Button onClick={clearActiveFilters}>Clear</Button>
    </Space>
  );

  const productFilterPanel = (
    <Space wrap align="end" size={[12, 12]}>
      <FilterField label="Keyword">
        <Input allowClear placeholder="Name / model / desc" style={{ width: 180 }} value={productFilters.q} onChange={(event) => updateProductFilter('q', event.target.value || undefined)} />
      </FilterField>
      <FilterField label="Industry">
        <Select allowClear placeholder="Select industry" style={{ width: 150 }} options={industries} value={productFilters.industry} onChange={(value) => updateProductFilter('industry', value)} />
      </FilterField>
      <FilterField label="Category">
        <Select allowClear showSearch placeholder="Select category" style={{ width: 210 }} options={productCategories} value={productFilters.category} onChange={(value) => updateProductFilter('category', value)} />
      </FilterField>
      <FilterField label="Manufacturer">
        <Input allowClear placeholder="Manufacturer" style={{ width: 180 }} value={productFilters.manufacturerName} onChange={(event) => updateProductFilter('manufacturerName', event.target.value || undefined)} />
      </FilterField>
      <FilterField label="Confidence Range">
        <Select
          allowClear
          placeholder="Select confidence"
          style={{ width: 205 }}
          options={confidencePresets}
          value={rangeValue(productFilters.minConfidence, productFilters.maxConfidence)}
          onChange={(value) => {
            const [min, max] = parseRange(value);
            setProductFilters((prev) => ({ ...prev, minConfidence: min, maxConfidence: max }));
          }}
        />
      </FilterField>
      <FilterField label="Status">
        <Select allowClear placeholder="Select status" style={{ width: 140 }} options={entityStatuses} value={productFilters.status} onChange={(value) => updateProductFilter('status', value)} />
      </FilterField>
      <Button onClick={clearActiveFilters}>Clear</Button>
    </Space>
  );

  const relationshipFilterPanel = (
    <Space wrap align="end" size={[12, 12]}>
      <FilterField label="Entity Type">
        <Select allowClear placeholder="Either endpoint" style={{ width: 150 }} options={entityTypes} value={relationshipFilters.entityType} onChange={(value) => updateRelationshipFilter('entityType', value)} />
      </FilterField>
      <FilterField label="Source Type">
        <Select allowClear placeholder="Source" style={{ width: 140 }} options={entityTypes} value={relationshipFilters.sourceType} onChange={(value) => updateRelationshipFilter('sourceType', value)} />
      </FilterField>
      <FilterField label="Target Type">
        <Select allowClear placeholder="Target" style={{ width: 140 }} options={entityTypes} value={relationshipFilters.targetType} onChange={(value) => updateRelationshipFilter('targetType', value)} />
      </FilterField>
      <FilterField label="Relation Type">
        <Select allowClear showSearch placeholder="Select relation" style={{ width: 170 }} options={relationTypes} value={relationshipFilters.relationType} onChange={(value) => updateRelationshipFilter('relationType', value)} />
      </FilterField>
      <FilterField label="Confidence Range">
        <Select
          allowClear
          placeholder="Select confidence"
          style={{ width: 205 }}
          options={confidencePresets}
          value={rangeValue(relationshipFilters.minConfidence, relationshipFilters.maxConfidence)}
          onChange={(value) => {
            const [min, max] = parseRange(value);
            setRelationshipFilters((prev) => ({ ...prev, minConfidence: min, maxConfidence: max }));
          }}
        />
      </FilterField>
      <Button onClick={clearActiveFilters}>Clear</Button>
    </Space>
  );

  const activeFilterPanel = {
    opportunities: opportunityFilterPanel,
    companies: companyFilterPanel,
    products: productFilterPanel,
    relationships: relationshipFilterPanel,
  }[activeTab];

  const activeFilterMeta = {
    opportunities: `Matched: ${stats.total} opportunities`,
    companies: `Matched: ${companies.length} companies`,
    products: `Matched: ${products.length} products`,
    relationships: `Matched: ${relationships.length} relationships`,
  }[activeTab];

  const graphSummary = graph && graph.nodes.length > 0 ? (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Descriptions size="small" column={3} bordered>
        <Descriptions.Item label="Nodes">{graph.nodes.length}</Descriptions.Item>
        <Descriptions.Item label="Edges">{graph.edges.length}</Descriptions.Item>
        <Descriptions.Item label="Scope">Company · Product · Opportunity</Descriptions.Item>
      </Descriptions>
      <Typography.Text type="secondary">Latest nodes</Typography.Text>
      <Space wrap>
        {graph.nodes.slice(0, 20).map((node) => <Tag key={node.id} color={node.entity_type === 'company' ? 'green' : node.entity_type === 'product' ? 'purple' : 'orange'}>{node.label}</Tag>)}
      </Space>
    </Space>
  ) : <Empty description="No graph relationships yet" />;

  return (
    <Layout>
      <Header style={{ height: 110, background: '#0f172a', color: '#fff', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', paddingTop: 38 }}>
        <Space align="center">
          <AimOutlined style={{ fontSize: 26, marginTop: 2 }} />
          <div>
            <Typography.Title level={4} style={{ color: '#fff', margin: 0 }}>Industry Intelligence System</Typography.Title>
            <Typography.Text style={{ color: '#cbd5e1' }}>Opportunities · Companies · Products · Relationship Graph · Agent Q&A</Typography.Text>
          </div>
        </Space>
        <Button icon={<ReloadOutlined />} onClick={() => { load(); loadIndustryData(); }}>Refresh</Button>
      </Header>

      <Content style={{ padding: 20 }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} md={6}><Card><Statistic title="Filtered Opportunities" value={stats.total} /></Card></Col>
          <Col xs={24} md={6}><Card><Statistic title="Companies" value={companies.length} /></Card></Col>
          <Col xs={24} md={6}><Card><Statistic title="Products" value={products.length} /></Card></Col>
          <Col xs={24} md={6}><Card><Statistic title="Relationships" value={relationships.length} /></Card></Col>

          <Col xs={24} lg={16}>
            <Card
              title="Opportunity Map"
              extra={<Typography.Text type="secondary">Map follows the list filters</Typography.Text>}
            >
              <OpportunityMap data={data} companies={companies} onSelect={setSelectedId} onCompanySelect={setSelectedCompanyId} />
            </Card>
          </Col>

          <Col xs={24} lg={8}>
            <AgentChat />
          </Col>

          <Col span={24}>
            <Card
              title={<Space><FilterOutlined />{activeTab === 'opportunities' ? 'Opportunity Filters' : activeTab === 'companies' ? 'Company Filters' : activeTab === 'products' ? 'Product Filters' : 'Relationship Filters'}</Space>}
              extra={<Typography.Text type="secondary">{activeFilterMeta}</Typography.Text>}
            >
              {activeFilterPanel}
            </Card>
          </Col>

          <Col span={24}>
            <Tabs
              activeKey={activeTab}
              onChange={(key) => setActiveTab(key as ActiveTab)}
              items={[
                {
                  key: 'opportunities',
                  label: 'Opportunities',
                  children: (
                    <Card title="Opportunity List" extra={<Typography.Text type="secondary">Compatible with existing opportunity API</Typography.Text>}>
                      <Table rowKey="id" loading={loading} columns={columns} dataSource={data} pagination={{ pageSize: 10, showSizeChanger: true }} scroll={{ x: 1050 }} />
                    </Card>
                  ),
                },
                {
                  key: 'companies',
                  label: 'Companies',
                  children: (
                    <Card title="Company / Vendor Entities" extra={<Typography.Text type="secondary">Manufacturers, buyers, integrators, competitors</Typography.Text>}>
                      <Table rowKey="id" loading={industryLoading} columns={companyColumns} dataSource={companies} pagination={{ pageSize: 10, showSizeChanger: true }} scroll={{ x: 1050 }} />
                    </Card>
                  ),
                },
                {
                  key: 'products',
                  label: 'Products',
                  children: (
                    <Card title="Product Entities" extra={<Typography.Text type="secondary">Bearing products, models, and application scenarios</Typography.Text>}>
                      <Table rowKey="id" loading={industryLoading} columns={productColumns} dataSource={products} pagination={{ pageSize: 10, showSizeChanger: true }} scroll={{ x: 1050 }} />
                    </Card>
                  ),
                },
                {
                  key: 'relationships',
                  label: 'Relationships / Graph',
                  children: (
                    <Row gutter={[16, 16]}>
                      <Col xs={24} lg={8}>
                        <Card title={<Space><ApartmentOutlined />Graph Overview</Space>} loading={industryLoading}>{graphSummary}</Card>
                      </Col>
                      <Col xs={24} lg={16}>
                        <Card title="Relationship Edges" extra={<Typography.Text type="secondary">company/product/opportunity relationship records</Typography.Text>}>
                          <Table rowKey="id" loading={industryLoading} columns={relationshipColumns} dataSource={relationships} pagination={{ pageSize: 10, showSizeChanger: true }} scroll={{ x: 900 }} />
                        </Card>
                      </Col>
                    </Row>
                  ),
                },
              ]}
            />
          </Col>
        </Row>
      </Content>

      <OpportunityDetailDrawer id={selectedId} open={!!selectedId} onClose={() => setSelectedId(null)} onUpdated={load} />
      <Drawer
        title="Company Detail"
        open={!!selectedCompanyId}
        onClose={() => setSelectedCompanyId(null)}
        width={520}
      >
        {(() => {
          const company = companies.find((item) => item.id === selectedCompanyId);
          if (!company) return <Empty description="No company selected" />;
          return (
            <Space direction="vertical" size={16} style={{ width: '100%' }}>
              <Typography.Title level={4} style={{ margin: 0 }}>{company.name}</Typography.Title>
              <Descriptions bordered size="small" column={1}>
                <Descriptions.Item label="Type">{company.company_type || '-'}</Descriptions.Item>
                <Descriptions.Item label="Industry">{company.industry || '-'}</Descriptions.Item>
                <Descriptions.Item label="Location">{[company.province, company.city].filter(Boolean).join(' ') || '-'}</Descriptions.Item>
                <Descriptions.Item label="Confidence">{company.confidence_score}</Descriptions.Item>
                <Descriptions.Item label="Website">{company.website ? <a href={company.website} target="_blank" rel="noopener noreferrer">{company.website}</a> : '-'}</Descriptions.Item>
                <Descriptions.Item label="Source">{company.source_url ? <a href={company.source_url} target="_blank" rel="noopener noreferrer">{company.source_url}</a> : '-'}</Descriptions.Item>
              </Descriptions>
              <Typography.Paragraph>{company.description || 'No description yet.'}</Typography.Paragraph>
              <Space wrap>
                {(company.tags?.items || []).map((tag) => <Tag key={tag}>{tag}</Tag>)}
              </Space>
            </Space>
          );
        })()}
      </Drawer>
    </Layout>
  );
}

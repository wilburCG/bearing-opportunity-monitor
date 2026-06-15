'use client';

import { createOpportunityNote, getOpportunity, listOpportunityNotes, updateOpportunityStatus } from '@/lib/api';
import { fmtTime, industryLabel, opportunityTypeLabel, scoreColor, statusColor, statusLabel } from '@/lib/format';
import type { OpportunityDetail, OpportunityNote } from '@/types/opportunity';
import { App, Button, Descriptions, Divider, Drawer, Empty, Input, List, Space, Spin, Tag, Typography } from 'antd';
import { useEffect, useState } from 'react';

const { Paragraph, Text } = Typography;

interface Props {
  id?: number | null;
  open: boolean;
  onClose: () => void;
  onUpdated: () => void;
}

const statusOptions = [
  ['new', 'New'],
  ['pending_verify', 'Pending Verification'],
  ['followed', 'Followed Up'],
  ['converted', 'Converted'],
  ['invalid', 'Invalid'],
];

function itemList(value?: { items?: string[] } | null) {
  if (!value?.items?.length) return '-';
  return value.items.join(', ');
}

export default function OpportunityDetailDrawer({ id, open, onClose, onUpdated }: Props) {
  const { message } = App.useApp();
  const [detail, setDetail] = useState<OpportunityDetail | null>(null);
  const [notes, setNotes] = useState<OpportunityNote[]>([]);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  async function load() {
    if (!id) return;
    setLoading(true);
    try {
      const [detailData, notesData] = await Promise.all([getOpportunity(id), listOpportunityNotes(id)]);
      setDetail(detailData);
      setNotes(notesData);
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Failed to load opportunity details');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (open) load();
  }, [id, open]);

  async function changeStatus(status: string) {
    if (!id) return;
    setSaving(true);
    try {
      const updated = await updateOpportunityStatus(id, status);
      setDetail(updated);
      onUpdated();
      message.success('Status updated');
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Failed to update status');
    } finally {
      setSaving(false);
    }
  }

  async function submitNote() {
    if (!id || !note.trim()) return;
    setSaving(true);
    try {
      const created = await createOpportunityNote(id, note.trim(), 'Mose/Web');
      setNotes([created, ...notes]);
      setNote('');
      message.success('Note saved');
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Failed to save note');
    } finally {
      setSaving(false);
    }
  }

  return (
    <Drawer width={760} title="Opportunity Details" open={open} onClose={onClose} destroyOnClose>
      {loading ? <Spin /> : detail ? (
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <div>
            <Space wrap>
              <Tag color={statusColor(detail.status)}>{statusLabel(detail.status)}</Tag>
              <Tag>{industryLabel(detail.industry)}</Tag>
              <Tag>{opportunityTypeLabel(detail.opportunity_type)}</Tag>
              <Tag color="volcano">Score {detail.total_score}</Tag>
            </Space>
            <Typography.Title level={4} style={{ marginTop: 12 }}>{detail.title}</Typography.Title>
            <Paragraph>{detail.summary}</Paragraph>
          </div>

          <Descriptions bordered size="small" column={2}>
            <Descriptions.Item label="Company">{detail.company_name || '-'}</Descriptions.Item>
            <Descriptions.Item label="Project">{detail.project_name || '-'}</Descriptions.Item>
            <Descriptions.Item label="Location">{[detail.province, detail.city, detail.district].filter(Boolean).join(' / ') || '-'}</Descriptions.Item>
            <Descriptions.Item label="Coordinates">{detail.latitude && detail.longitude ? `${detail.latitude}, ${detail.longitude}` : '-'}</Descriptions.Item>
            <Descriptions.Item label="Bearing Types">{itemList(detail.bearing_types)}</Descriptions.Item>
            <Descriptions.Item label="Bearing Models">{itemList(detail.bearing_models)}</Descriptions.Item>
            <Descriptions.Item label="Equipment">{itemList(detail.equipment_types)}</Descriptions.Item>
            <Descriptions.Item label="Estimated Amount/Level">{detail.estimated_amount || '-'}</Descriptions.Item>
            <Descriptions.Item label="Volume Score"><Text style={{ color: scoreColor(detail.volume_score) }}>{detail.volume_score}</Text></Descriptions.Item>
            <Descriptions.Item label="Urgency Score"><Text style={{ color: scoreColor(detail.urgency_score) }}>{detail.urgency_score}</Text></Descriptions.Item>
            <Descriptions.Item label="Confidence"><Text style={{ color: scoreColor(detail.confidence_score) }}>{detail.confidence_score}</Text></Descriptions.Item>
            <Descriptions.Item label="Fit Score"><Text style={{ color: scoreColor(detail.fit_score) }}>{detail.fit_score}</Text></Descriptions.Item>
            <Descriptions.Item label="Updated At" span={2}>{fmtTime(detail.updated_at)}</Descriptions.Item>
          </Descriptions>

          <div>
            <Text strong>Confidence Rationale</Text>
            <Paragraph style={{ marginTop: 8 }}>{detail.confidence_reason || '-'}</Paragraph>
            <Text strong>Recommended Action</Text>
            <Paragraph style={{ marginTop: 8 }}>{detail.recommended_action || '-'}</Paragraph>
          </div>

          <Divider orientation="left">Status</Divider>
          <Space wrap>
            {statusOptions.map(([value, label]) => (
              <Button key={value} loading={saving} type={detail.status === value ? 'primary' : 'default'} onClick={() => changeStatus(value)}>
                {label}
              </Button>
            ))}
          </Space>

          <Divider orientation="left">Follow-up Notes</Divider>
          <Space.Compact style={{ width: '100%' }}>
            <Input value={note} onChange={(event) => setNote(event.target.value)} placeholder="Add verification results, sales actions, or next steps" onPressEnter={submitNote} />
            <Button type="primary" loading={saving} onClick={submitNote}>Save</Button>
          </Space.Compact>
          <List
            locale={{ emptyText: <Empty description="No notes yet" /> }}
            dataSource={notes}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta title={item.operator || 'Unknown'} description={item.note} />
              </List.Item>
            )}
          />
        </Space>
      ) : <Empty description="No opportunity selected" />}
    </Drawer>
  );
}

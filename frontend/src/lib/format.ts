export function scoreColor(score: number): string {
  if (score >= 80) return '#d4380d';
  if (score >= 70) return '#fa8c16';
  if (score >= 60) return '#d4b106';
  return '#389e0d';
}

export function statusLabel(status: string): string {
  const map: Record<string, string> = {
    new: 'New',
    pending_verify: 'Pending Verification',
    followed: 'Followed Up',
    converted: 'Converted',
    invalid: 'Invalid',
  };
  return map[status] || status;
}

export function statusColor(status: string): string {
  const map: Record<string, string> = {
    new: 'blue',
    pending_verify: 'gold',
    followed: 'purple',
    converted: 'green',
    invalid: 'red',
  };
  return map[status] || 'default';
}

export function industryLabel(industry?: string | null): string {
  const map: Record<string, string> = {
    风电: 'Wind Power',
    钢铁: 'Steel',
    矿山: 'Mining',
    水泥: 'Cement',
    轨交: 'Rail Transit',
    化工: 'Chemical',
    数据中心: 'Data Center',
  };
  return industry ? (map[industry] || industry) : '-';
}

export function opportunityTypeLabel(type?: string | null): string {
  const map: Record<string, string> = {
    询价: 'RFQ',
    采购: 'Procurement',
    招标: 'Tender',
    项目: 'Project',
    招聘信号: 'Hiring Signal',
    维护服务: 'Maintenance Service',
    early_signal: 'Early Signal',
  };
  return type ? (map[type] || type) : '-';
}

export function fmtTime(value?: string | null): string {
  if (!value) return '-';
  return value.replace('T', ' ').slice(0, 16);
}

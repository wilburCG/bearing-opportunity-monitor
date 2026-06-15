'use client';

import { chatWithAgent } from '@/lib/api';
import { RobotOutlined, SendOutlined } from '@ant-design/icons';
import { App, Button, Card, Input, List, Space, Typography } from 'antd';
import { useState } from 'react';

interface ChatItem { role: 'user' | 'agent'; content: string; mode?: string; }

export default function AgentChat() {
  const { message } = App.useApp();
  const [items, setItems] = useState<ChatItem[]>([
    { role: 'agent', content: 'Ask me about bearing opportunities. I can answer from the current opportunity database; when LLM credentials are configured, I will use the configured doc2graph-compatible LLM model.' },
  ]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!text.trim() || loading) return;
    const question = text.trim();
    setText('');
    setItems((prev) => [...prev, { role: 'user', content: question }]);
    setLoading(true);
    try {
      const response = await chatWithAgent(question);
      setItems((prev) => [...prev, { role: 'agent', content: response.answer, mode: response.mode }]);
    } catch (error) {
      const msg = error instanceof Error ? error.message : 'Agent request failed';
      message.error(msg);
      setItems((prev) => [...prev, { role: 'agent', content: `Agent request failed: ${msg}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card title={<Space><RobotOutlined />Opportunity Agent</Space>} style={{ height: '100%' }}>
      <List
        size="small"
        dataSource={items}
        style={{ height: 300, overflow: 'auto', marginBottom: 12 }}
        renderItem={(item) => (
          <List.Item style={{ justifyContent: item.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <Typography.Text
              style={{
                maxWidth: '92%',
                whiteSpace: 'pre-wrap',
                background: item.role === 'user' ? '#e6f4ff' : '#f6ffed',
                padding: '8px 10px',
                borderRadius: 10,
              }}
            >
              {item.content}
              {item.mode ? `\n\n[mode: ${item.mode}]` : ''}
            </Typography.Text>
          </List.Item>
        )}
      />
      <Space.Compact style={{ width: '100%' }}>
        <Input value={text} disabled={loading} onChange={(e) => setText(e.target.value)} onPressEnter={send} placeholder="e.g. Show high-confidence steel RFQs" />
        <Button type="primary" loading={loading} icon={<SendOutlined />} onClick={send}>Send</Button>
      </Space.Compact>
    </Card>
  );
}

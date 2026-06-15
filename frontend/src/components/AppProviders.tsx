'use client';

import { ConfigProvider, App as AntdApp } from 'antd';
import enUS from 'antd/locale/en_US';

export default function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <ConfigProvider locale={enUS} theme={{ token: { colorPrimary: '#1677ff', borderRadius: 10 } }}>
      <AntdApp>{children}</AntdApp>
    </ConfigProvider>
  );
}

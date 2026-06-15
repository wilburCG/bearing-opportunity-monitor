import type { Metadata } from 'next';
import AppProviders from '@/components/AppProviders';
import 'leaflet/dist/leaflet.css';
import './globals.css';

export const metadata: Metadata = {
  title: 'Bearing Opportunity Intelligence Platform',
  description: 'Bearing sales opportunity monitoring and intelligence platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}

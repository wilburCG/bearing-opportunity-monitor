import { NextRequest, NextResponse } from 'next/server';

const BACKEND_INTERNAL_URL = process.env.BACKEND_INTERNAL_URL || 'http://backend:8000';

type Ctx = { params: { path?: string[] } };

async function proxy(request: NextRequest, ctx: Ctx) {
  const path = (ctx.params.path || []).join('/');
  const target = new URL(`${BACKEND_INTERNAL_URL}/api/${path}`);
  request.nextUrl.searchParams.forEach((value, key) => target.searchParams.set(key, value));

  const headers: Record<string, string> = {};
  const contentType = request.headers.get('content-type');
  if (contentType) headers['Content-Type'] = contentType;

  const init: RequestInit = {
    method: request.method,
    headers,
    cache: 'no-store',
  };

  if (!['GET', 'HEAD'].includes(request.method)) {
    init.body = await request.text();
  }

  const response = await fetch(target.toString(), init);
  const body = await response.text();

  return new NextResponse(body, {
    status: response.status,
    headers: {
      'Content-Type': response.headers.get('content-type') || 'application/json',
      'Cache-Control': 'no-store',
    },
  });
}

export const GET = proxy;
export const POST = proxy;
export const PATCH = proxy;
export const PUT = proxy;
export const DELETE = proxy;

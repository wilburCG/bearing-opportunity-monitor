# bearing-opportunity-monitor

轴承销售机会舆情监测与分析平台。

## MVP 决策

- 当前服务器部署
- 高德地图
- Qdrant 向量数据库
- MySQL + Neo4j
- 重点行业：风电、钢铁、矿山、水泥、轨交
- 第一版不做登录权限，不接 CRM

## 文档

- `docs/PRD_AND_ARCHITECTURE.md`：产品需求、架构、数据模型、MVP 计划
- `docs/DECISIONS.md`：关键决策记录
- `docs/MVP_TASKS.md`：开发任务拆分

## 本地启动草案

```bash
cd projects/bearing-opportunity-monitor
cp backend/.env.example backend/.env
# 补充 LLM / 高德 API Key 后启动
docker compose up -d --build
```

健康检查：

```bash
curl http://localhost:8000/health
```

## 当前端口

- 前端：`http://127.0.0.1:3002`
- 后端：`http://127.0.0.1:8002`
- MySQL：`3306`
- Qdrant：`6333/6334`
- Neo4j：`7475/7688`

说明：服务器已有服务占用 `8000` 和 Neo4j 默认端口 `7474/7687`，本项目已避让。

## 前端功能状态

第一版前端已完成：统计卡片、地图点位、机会列表、筛选、详情抽屉、状态更新、跟进备注、Agent 对话框占位。

高德地图 Key 尚未配置，因此当前地图使用坐标散点占位图。配置 `frontend/.env.local` 的 `NEXT_PUBLIC_AMAP_KEY` 后会使用高德地图。

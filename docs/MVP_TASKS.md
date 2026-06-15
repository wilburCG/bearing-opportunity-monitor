# MVP 开发任务拆分

## 目标

4 周内完成可用 MVP：每周采集公开轴承机会数据，结构化入库，地图展示，机会列表/详情，Agent 问答。

## Milestone 1：后端与数据模型

- [ ] FastAPI 项目骨架
- [ ] MySQL 表结构：sources、opportunities、opportunity_sources、search_tasks、opportunity_notes
- [ ] SQLAlchemy Models
- [ ] Alembic migration
- [ ] 健康检查接口 `/health`
- [ ] 机会列表接口 `/api/opportunities`
- [ ] 机会详情接口 `/api/opportunities/{id}`
- [ ] 状态更新接口 `/api/opportunities/{id}/status`

## Milestone 2：采集与 AI 抽取

- [ ] 搜索 query 配置：采购、招标、项目、招聘
- [ ] 搜索任务 worker
- [ ] 网页正文抽取
- [ ] URL/title/content hash 去重
- [ ] LLM 判断是否相关
- [ ] LLM 抽取结构化 opportunity
- [ ] 评分模型：机会量、紧急程度、可信度、匹配度
- [ ] 每周任务调度

## Milestone 3：向量库与图谱

- [ ] Qdrant collection 初始化
- [ ] 原文分块与 embedding
- [ ] source chunk 入向量库
- [ ] doc2graph 适配层
- [ ] Neo4j schema 初始化
- [ ] 实体/关系导入 Neo4j

## Milestone 4：Web MVP

- [ ] 机会地图页，高德地图
- [ ] 机会列表页，支持排序和筛选
- [ ] 机会详情页
- [ ] 机会状态标记
- [ ] Agent 对话框

## Milestone 5：Agent 问答

- [ ] 用户问题分类：SQL / Vector / Graph / Hybrid
- [ ] SQL 查询工具
- [ ] Qdrant 语义召回工具
- [ ] Neo4j 图谱查询工具
- [ ] 综合回答生成
- [ ] 回答附来源和证据

## 暂不做

- 登录和权限
- CRM 对接
- 复杂组织架构
- 移动端适配

## 2026-06-05 进展

已完成 Milestone 1 的第一批骨架：

- [x] FastAPI 项目骨架
- [x] MySQL 核心模型：sources、opportunities、opportunity_sources、search_tasks、opportunity_notes
- [x] Alembic 初始化文件与首版 migration
- [x] 健康检查接口 `/health`
- [x] 机会列表接口 `/api/opportunities`
- [x] 机会详情接口 `/api/opportunities/{id}`
- [x] 状态更新接口 `/api/opportunities/{id}/status`
- [x] 跟进备注接口 `/api/opportunities/{id}/notes`
- [x] mock 数据脚本 `backend/app/scripts/seed_mock.py`

下一步：启动 Docker 服务并执行 migration/seed，验证接口。

## 2026-06-05 服务验证记录

已启动并验证基础服务：

- MySQL：`bearing_mysql`，外部端口 `3306`
- Qdrant：`bearing_qdrant`，外部端口 `6333/6334`
- Neo4j：`bearing_neo4j`，外部端口 `7475/7688`
  - 说明：服务器已有 `doc2graph-neo4j` 占用 `7474/7687`，所以本项目避让到 `7475/7688`。
- Backend：`bearing_backend`，外部端口 `8002`
  - 说明：服务器已有进程占用 `8000`，所以本项目避让到 `8002`。

已验证接口：

- [x] `GET http://127.0.0.1:8002/health`
- [x] `GET http://127.0.0.1:8002/api/opportunities?limit=10`
- [x] `GET http://127.0.0.1:8002/api/opportunities/1`
- [x] `PATCH http://127.0.0.1:8002/api/opportunities/1/status`
- [x] `POST http://127.0.0.1:8002/api/opportunities/1/notes`
- [x] `GET http://127.0.0.1:8002/api/opportunities/1/notes`

修复记录：

- 后端 Dockerfile 改为使用清华 PyPI 镜像，解决 pip 下载过慢导致构建被系统杀掉的问题。
- `sources.url` 从 `String(1024)` 改为 `String(512)`，解决 MySQL utf8mb4 唯一索引长度超过 3072 bytes 的问题。

## 2026-06-05 前端 MVP 进展

已完成前端第一版：

- [x] Next.js + TypeScript + Ant Design 项目结构
- [x] 后端 API 客户端封装
- [x] 首页统计卡片：机会数、高优先级机会、平均评分
- [x] 机会地图组件
  - 支持高德地图 Key 后切换真实地图
  - 未配置 Key 时使用坐标散点占位图
- [x] 机会列表表格
  - 展示标题、企业、地区、行业、类型、总分、紧急、可信、状态
  - 支持总分/紧急/可信排序
- [x] 行业和状态筛选
- [x] 机会详情抽屉
  - 展示评分、企业、项目、地区、轴承类型、设备类型、可信度说明、推荐动作
  - 支持状态更新
  - 支持添加和查看跟进备注
- [x] Agent 对话框占位组件
- [x] Docker frontend 服务，外部端口 `3002`
- [x] 前端生产构建 `npm run build` 通过
- [x] 浏览器验证页面、地图点位、列表数据、详情抽屉加载成功

修复记录：

- 增加 TypeScript path alias `@/*`。
- 增加 FastAPI CORS 中间件，解决前端 `3002` 调后端 `8002` 被浏览器拦截的问题。
- 修正 `docker-compose.yml` 中 frontend 服务缩进位置。
- 增加 `frontend/.dockerignore`，避免后续 Docker build 传入 `node_modules` 和 `.next` 导致上下文过大。

访问地址：

- Frontend: `http://127.0.0.1:3002`
- Backend: `http://127.0.0.1:8002`

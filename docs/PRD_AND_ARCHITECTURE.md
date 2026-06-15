# 轴承销售机会舆情监测与分析平台 — PRD 与技术方案

## 1. 项目目标

建设一个面向轴承销售与服务业务的机会监测平台，定期从公开信息中发现潜在业务线索，包括：

- 轴承采购、招标、询价、供应商征集、项目建设、设备维护等公开信息
- 招聘信息中隐含的产线扩张、设备运维、轴承相关岗位需求
- 项目公告中涉及的行业、地区、设备类型、潜在轴承型号和用量
- 对机会进行结构化分析、地图展示和智能问答

最终目标：帮助销售团队快速识别“哪里有机会、机会有多大、是否紧急、可信度如何、应如何跟进”。

## 2. 核心用户

- 销售负责人：查看全国/区域机会分布、排序、跟进优先级
- 区域销售：查看自己区域内的机会、线索来源、联系方式、项目阶段
- 售后/服务团队：发现维护、检修、替换、设备故障相关服务机会
- 管理层：查看行业趋势、区域热度、客户/项目画像

## 3. 功能范围

### 3.1 数据检索、整理与存储

每周由 AI Agent 自动检索公开网络数据，覆盖以下信息类型：

1. 采购类
   - 轴承采购公告
   - 招投标公告
   - 询价单
   - 供应商入围/征集
   - 备件采购

2. 项目类
   - 新建工厂/产线
   - 风电、矿山、钢铁、水泥、轨交、港口、造纸、化工等重资产项目
   - 设备技改、检修、扩产公告

3. 招聘类
   - 设备维修工程师
   - 轴承工程师
   - 旋转设备工程师
   - 风电运维、矿山设备、轧机维护等岗位
   - 从招聘中推断企业扩产、设备类型、服务需求

4. 行业资讯类
   - 企业产能扩张
   - 设备故障/停产检修
   - 重大工程进展

数据存储分三层：

- MySQL：结构化业务机会、来源、地区、行业、评分、状态等
- 向量数据库：原文、网页正文、摘要、分块文本，用于语义检索和 RAG 问答
- Neo4j：利用 doc2graph 能力识别实体和关系，构建知识图谱

### 3.2 Web 展示页面

1. 地图展示
   - 按地理位置展示机会点
   - 点位颜色表示机会等级/紧急程度/可信度
   - 点位大小表示预估机会量或金额
   - 支持省、市、行业、机会类型、时间范围筛选

2. 机会列表
   - 按机会量、紧急程度、可信度、更新时间排序
   - 支持查看详情、来源链接、AI 摘要、证据片段
   - 支持人工标记状态：待核实、已跟进、无效、转商机

3. 机会详情页
   - 原始来源
   - AI 结构化字段
   - 可信度解释
   - 相关企业、项目、设备、型号、行业关系图
   - 推荐跟进动作

4. 对话框 / Agent 问答
   - 基于 MySQL + 向量数据库 + Neo4j 回答问题
   - 示例：
     - “最近一周华东地区有哪些高可信轴承采购机会？”
     - “风电行业有哪些潜在服务机会？”
     - “哪些企业可能需要调心滚子轴承？”
     - “把机会按紧急程度排序，并说明原因。”

## 4. 机会识别模型

### 4.1 机会对象 Opportunity

一个 Opportunity 表示一条潜在销售或服务线索，不等同于一条网页。多条来源可以合并为一个机会。

核心字段：

- 标题
- 摘要
- 机会类型：采购 / 招标 / 项目 / 招聘 / 维护服务 / 行业资讯
- 行业：风电 / 钢铁 / 水泥 / 矿山 / 轨交 / 港口 / 化工 / 造纸 / 其他
- 企业/业主/招标方
- 地区：省、市、区县、经纬度
- 涉及产品：轴承类型、型号、品牌、数量、设备
- 预估机会量：金额或等级
- 紧急程度：高 / 中 / 低
- 可信度：高 / 中 / 低，附解释
- 发现时间、发布时间、截止时间
- 来源链接与证据片段
- 状态：新发现 / 待核实 / 已跟进 / 转商机 / 无效

### 4.2 评分维度

综合得分 = 机会量评分 + 紧急程度评分 + 可信度评分 + 战略匹配评分

建议字段：

- `volume_score`：潜在用量/金额/项目规模
- `urgency_score`：截止日期、采购阶段、检修时间窗口
- `confidence_score`：来源权威性、字段完整度、多源验证情况
- `fit_score`：与目标行业、优势产品、区域策略匹配程度
- `total_score`：综合排序分

### 4.3 可信度解释

每条机会必须保留 evidence：

- 来源 URL
- 原文标题
- 原文发布时间
- 命中的关键词
- LLM 抽取依据片段
- 是否多源验证

平台不应只给结论，要能解释“为什么这是一条机会”。

## 5. 技术架构

```text
┌────────────────────────────┐
│ Weekly Search Agent         │
│ 检索公开数据 / 去重 / 抽取     │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│ Ingestion Pipeline          │
│ 抓取正文 / 清洗 / 分块 / 标准化 │
└───────┬────────┬────────────┘
        │        │
        │        ├──────────────► Vector DB
        │        │                原文、分块、embedding
        │        │
        ▼        ▼
      MySQL    doc2graph
  结构化机会     实体关系抽取
        │        │
        │        ▼
        │      Neo4j
        │    知识图谱
        │        │
        └────────┴──────────────┐
                                 ▼
┌────────────────────────────┐
│ Backend API / Agent Service │
│ 查询、排序、RAG、图谱查询      │
└──────────────┬─────────────┘
               ▼
┌────────────────────────────┐
│ Web UI                      │
│ 地图 / 列表 / 详情 / 对话框    │
└────────────────────────────┘
```

## 6. 推荐技术栈

### 后端

- Python + FastAPI
- SQLAlchemy / Alembic
- MySQL 8
- Neo4j
- Qdrant 或 Milvus 作为向量数据库；MVP 可先用 Qdrant
- APScheduler / Celery Beat 做每周任务
- Playwright / Requests / RSS / 搜索 API 组合做采集

### AI / Agent

- LLM：沿用当前可用模型，优先火山/Ark 或可配置 OpenAI-compatible API
- Embedding：使用支持中文语义检索的 embedding 模型
- RAG：结构化 SQL 检索 + 向量召回 + Neo4j 图谱查询混合
- doc2graph：复用已有“文档 → 实体关系 → Neo4j”方案，扩展轴承领域 schema

### 前端

- React / Next.js
- 地图：高德地图 JS API 或 Mapbox；国内使用建议高德
- UI：Ant Design / Arco Design
- 图谱可视化：AntV G6 / ECharts Graph / Neo4j Bloom 外链

## 7. 数据库设计初稿

### 7.1 MySQL 核心表

#### `sources`

存储原始来源。

- `id`
- `url`
- `title`
- `source_site`
- `source_type`
- `published_at`
- `fetched_at`
- `raw_text_hash`
- `content_text`
- `content_summary`
- `credibility_level`

#### `opportunities`

存储归并后的业务机会。

- `id`
- `title`
- `summary`
- `opportunity_type`
- `industry`
- `company_name`
- `project_name`
- `province`
- `city`
- `district`
- `address`
- `latitude`
- `longitude`
- `bearing_types`
- `bearing_models`
- `equipment_types`
- `estimated_quantity`
- `estimated_amount`
- `deadline_at`
- `volume_score`
- `urgency_score`
- `confidence_score`
- `fit_score`
- `total_score`
- `confidence_reason`
- `recommended_action`
- `status`
- `created_at`
- `updated_at`

#### `opportunity_sources`

机会与来源多对多关系。

- `opportunity_id`
- `source_id`
- `evidence_snippet`
- `extraction_confidence`

#### `search_tasks`

每周检索任务记录。

- `id`
- `task_type`
- `query`
- `status`
- `started_at`
- `finished_at`
- `found_count`
- `created_opportunity_count`
- `error_message`

#### `opportunity_notes`

人工跟进记录。

- `id`
- `opportunity_id`
- `note`
- `operator`
- `created_at`

### 7.2 Vector DB Collection

建议 collection：`bearing_source_chunks`

metadata：

- `source_id`
- `opportunity_id`
- `url`
- `title`
- `published_at`
- `province`
- `city`
- `industry`
- `opportunity_type`

### 7.3 Neo4j Schema

节点：

- `Company`
- `Project`
- `Location`
- `Industry`
- `Equipment`
- `BearingType`
- `BearingModel`
- `Opportunity`
- `Source`
- `Tender`
- `JobPosting`

关系：

- `(Company)-[:OWNS|BUILDS|OPERATES]->(Project)`
- `(Project)-[:LOCATED_IN]->(Location)`
- `(Project)-[:BELONGS_TO]->(Industry)`
- `(Project)-[:USES_EQUIPMENT]->(Equipment)`
- `(Equipment)-[:USES_BEARING_TYPE]->(BearingType)`
- `(Opportunity)-[:EVIDENCED_BY]->(Source)`
- `(Opportunity)-[:RELATED_TO_COMPANY]->(Company)`
- `(Opportunity)-[:INVOLVES_MODEL]->(BearingModel)`
- `(JobPosting)-[:INDICATES_NEED_FOR]->(Equipment)`

## 8. 采集与抽取流程

### 8.1 每周检索流程

1. 根据关键词模板生成搜索 query
2. 获取搜索结果或公开网页列表
3. 抓取网页正文
4. 去重：URL、标题、正文 hash、语义相似度
5. LLM 判断是否与轴承销售/服务机会相关
6. LLM 抽取结构化字段
7. 地理编码获取经纬度
8. 计算机会评分
9. 写入 MySQL
10. 原文分块写入向量数据库
11. 调用 doc2graph 抽取实体关系写入 Neo4j
12. 生成本周机会摘要

### 8.2 初始关键词模板

采购/招标：

- `轴承 采购 公告`
- `轴承 招标`
- `轴承 询价`
- `轴承 备件 采购`
- `滚子轴承 招标`
- `调心滚子轴承 采购`
- `风电 轴承 采购`
- `轧机 轴承 采购`

项目/行业：

- `新建 产线 设备 轴承`
- `风电项目 运维 轴承`
- `矿山设备 检修 轴承`
- `钢铁 轧机 检修 轴承`
- `水泥 回转窑 轴承`

招聘：

- `轴承 工程师 招聘`
- `设备维修工程师 轴承 招聘`
- `旋转设备工程师 招聘`
- `风电运维 轴承 招聘`
- `轧机维护 招聘`

## 9. Agent 问答设计

### 9.1 查询路由

用户问题进入后先分类：

- 统计/筛选类 → SQL
- 语义证据类 → 向量检索
- 关系推理类 → Neo4j
- 综合分析类 → SQL + Vector + Neo4j 混合

### 9.2 回答要求

- 明确引用数据来源
- 不确定时说明不确定原因
- 能给排序依据
- 能给销售建议
- 支持导出结果列表

## 10. MVP 范围建议

第一版不要一次做太大，建议 4 周 MVP：

### Week 1：数据模型与采集原型

- 建 FastAPI 项目骨架
- MySQL schema
- 搜索 query 配置
- 手动/定时采集 20-50 条样本
- LLM 抽取 Opportunity

### Week 2：存储与评分

- MySQL 入库
- Qdrant 入库
- 机会去重/合并
- 评分模型 v1
- 周报摘要任务

### Week 3：Web MVP

- 地图展示
- 机会列表
- 详情页
- 状态标记

### Week 4：Agent 问答 + Neo4j

- 接入 doc2graph 到 Neo4j
- SQL + 向量问答
- 简单图谱查询
- 部署到服务器

## 11. 开发任务拆分

### Backend

- 初始化 FastAPI 服务
- 配置管理 `.env`
- SQLAlchemy 模型与 migration
- 数据采集模块
- LLM 抽取模块
- 评分模块
- 向量库模块
- Neo4j/doc2graph 适配模块
- Agent 问答 API

### Frontend

- 项目初始化
- 登录/基础布局，可 MVP 暂不做权限
- 地图页
- 机会列表页
- 机会详情页
- 对话框组件

### Ops

- Docker Compose：backend、frontend、mysql、qdrant、neo4j
- 定时任务
- 日志与任务状态
- 备份策略

## 12. 关键风险与建议

1. 数据源稳定性
   - 公开网页格式变化大，MVP 先使用搜索结果 + 通用正文抽取。

2. 误报
   - 必须保留证据片段和可信度解释，不直接把所有抽取结果当事实。

3. 地理位置缺失
   - 需要从企业名、项目名、公告地区多路推断，低置信时不强行定位。

4. 机会量估算困难
   - 第一版用等级评分，后续根据行业设备参数估算轴承数量。

5. 法务/合规
   - 只抓取公开信息，遵守 robots、频率限制和来源标注。

## 13. 需要确认的问题

1. 部署服务器是否沿用当前 OpenClaw 所在服务器，还是另有业务服务器？
2. 目标用户是否需要登录和权限控制？
3. 地图优先使用高德地图可以吗？
4. 向量数据库倾向 Qdrant 还是 Milvus？MVP 建议 Qdrant。
5. 是否已有目标行业/区域优先级？例如先做风电、钢铁、矿山？
6. 是否需要对接 CRM，还是第一版只在平台内管理状态？
7. doc2graph 目前看只有设计文档，是否有代码在别的仓库/服务器？如果有，需要给我路径或接入方式。

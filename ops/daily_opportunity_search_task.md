# 每日轴承商机检索任务

执行频率：每天 04:00（Asia/Shanghai）

目标：检索最近发布的轴承相关商机/舆情线索，抽取为结构化 JSON，并合并更新到 `bearing-opportunity-monitor` 的 MySQL 数据库中。

## 执行步骤

1. 进入项目目录：
   `/root/.openclaw/workspace/projects/bearing-opportunity-monitor`

2. 读取查询词：
   `backend/app/workers/search_queries.py`

3. 用 web_search/web_fetch 检索最近 1-3 天的新结果。优先搜索这些类型：
   - 采购招标：轴承 采购 公告、轴承 招标、轴承 询价、轴承 备件 采购、滚子轴承 招标、调心滚子轴承 采购、风电 轴承 采购、轧机 轴承 采购
   - 项目机会：新建产线设备轴承、风电运维轴承、矿山设备检修轴承、钢铁轧机检修轴承、水泥回转窑轴承、轨交车辆检修轴承
   - 招聘信号：轴承工程师招聘、设备维修工程师轴承招聘、旋转设备工程师招聘、风电运维轴承招聘、轧机维护招聘

4. 只保留真实、有来源 URL 的商机线索。优先级：
   - 招投标/采购公告/询价公告
   - 工厂、产线、设备检修、运维项目
   - 能反映采购/维修需求的招聘或项目动态

5. 为每条线索抽取并生成 JSON list。字段尽量匹配 `backend/app/scripts/import_opportunities_json.py` 支持的字段：
   - `source_url` 必填
   - `title` 必填
   - `summary`
   - `opportunity_type`（采购招标/项目机会/招聘信号/其他）
   - `industry`（风电/钢铁/矿山/水泥/轨交/化工/其他）
   - `company_name`
   - `project_name`
   - `province` / `city` / `district` / `address`
   - `bearing_types` / `bearing_models` / `equipment_types`
   - `estimated_quantity` / `estimated_amount`
   - `deadline_at` / `published_at`
   - `volume_score` / `urgency_score` / `confidence_score` / `fit_score` / `total_score`
   - `confidence_reason`
   - `recommended_action`
   - `source_title` / `source_site` / `source_type`
   - `content_text`
   - `evidence_snippet`
   - `credibility_level`

6. 保存 JSON 到：
   `backend/app/data/daily_opportunities/YYYY-MM-DD.json`

7. 合并入库：
   ```bash
   docker compose exec -T backend python -m app.scripts.import_opportunities_json /app/app/data/daily_opportunities/YYYY-MM-DD.json
   ```

   说明：导入脚本已支持 upsert。相同 `source_url` 会更新来源和已关联商机；相同标题/公司会尽量合并到已有商机；新来源会新增并建立 `opportunity_sources` 关联。

8. 记录运行摘要到：
   `memory/YYYY-MM-DD.md`

   记录格式建议：
   ```markdown
   ## 轴承商机每日检索
   - 检索时间：YYYY-MM-DD 04:00 Asia/Shanghai
   - 检索查询数：N
   - 候选结果：N
   - 入库结果：created=X, updated=Y, linked=Z, skipped=W
   - 数据文件：projects/bearing-opportunity-monitor/backend/app/data/daily_opportunities/YYYY-MM-DD.json
   - 高分新增/更新商机：...
   ```

9. 如任务失败：
   - 保留错误日志
   - 最终回复用简短中文说明失败点
   - 不要伪造入库成功

## 输出要求

最终回复简洁说明：
- 今日发现/更新了多少条
- JSON 文件路径
- 入库命令输出
- 如果没有新商机，也说明“检索完成，暂无新商机”

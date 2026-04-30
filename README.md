# AR Industrial Anomaly Diagnosis + Root Cause Analysis Agent

一个面向**工业设备报警诊断、根因分析、处置建议与复盘**的多 Agent 项目模板，适合直接上传到 GitHub 作为作品集 / 毕设延展 / 面试项目。

> 核心价值：把“报警码 → 根因定位 → 处置建议 → 复盘报告”串成一条闭环链路，减少老师傅经验依赖，缩短 MTTR（Mean Time To Recovery）。

---

## 1. 项目定位

### 核心痛点
- 设备报警很多，但现场只看到**报码**，不知道真正根因
- 异常分析强依赖老师傅经验，恢复速度慢
- 手册、历史案例、SOP 分散，排障时来回翻资料
- 同类故障无法沉淀成可复用经验，团队知识不成体系

### 项目目标
构建一个多 Agent 工业异常诊断系统，实现：
1. **信号采集 Agent**：抓取 PLC 状态、报警码、最近操作记录、工艺上下文
2. **知识检索 Agent**：查询设备手册、历史故障案例、维修 SOP
3. **根因推理 Agent**：按“报警触发条件 → 设备上下文 → 最近动作链”做多步推理
4. **处置建议 Agent**：输出分级建议（可自恢复 / 需人工确认 / 需停机）
5. **复盘 Agent**：生成可追溯故障报告，沉淀案例库

### 适合展示的亮点
- 不是简单 RAG，而是**多 Agent 编排 + 结构化推理**
- 有明确工业语境：PLC、报警码、互锁、动作链、SOP、复盘
- 可以写出很漂亮的“长链推理”与“证据引用”流程
- 很容易量化业务收益：
  - 首次故障定位时间缩短 **50%**
  - 人工翻手册时间下降 **70%**
  - 常见报警自助处理覆盖率提升 **30%+**

---

## 2. 系统架构

```text
┌────────────────────────────────────────────────────────────────────┐
│                        Industrial RCA Agent                       │
├────────────────────────────────────────────────────────────────────┤
│  Signal Agent     │  Retrieval Agent   │  Reasoning Agent         │
│  - PLC snapshot   │  - Manual search   │  - Hypothesis generation │
│  - Alarm code     │  - SOP search      │  - Evidence scoring      │
│  - Recent ops     │  - Case search     │  - Root cause ranking    │
├────────────────────────────────────────────────────────────────────┤
│  Action Agent     │  Postmortem Agent  │  Connectors              │
│  - Severity       │  - RCA report      │  - Mock PLC              │
│  - Recovery steps │  - Timeline        │  - OPC UA adapter stub   │
│  - Safety guards  │  - Lessons learned │  - MES/SCADA extension   │
└────────────────────────────────────────────────────────────────────┘
```

### 数据流
1. **Signal Agent** 读取报警事件、最近动作、关键位号、互锁状态
2. **Retrieval Agent** 在手册 / SOP / 历史案例中找证据
3. **Reasoning Agent** 构造候选根因并打分排序
4. **Action Agent** 根据风险等级给出处置建议
5. **Postmortem Agent** 输出标准化故障复盘报告

---

## 3. 项目目录

```text
industrial-rca-agent/
├─ app/
│  ├─ main.py                      # FastAPI 入口
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ models.py
│  │  └─ orchestrator.py
│  ├─ agents/
│  │  ├─ signal_agent.py
│  │  ├─ retrieval_agent.py
│  │  ├─ reasoning_agent.py
│  │  ├─ action_agent.py
│  │  └─ postmortem_agent.py
│  ├─ connectors/
│  │  ├─ plc_mock.py
│  │  └─ opcua_adapter.py
│  ├─ knowledge/
│  │  ├─ alarm_dictionary.json
│  │  ├─ manuals/
│  │  │  └─ packaging_line_manual.md
│  │  ├─ sop/
│  │  │  └─ jam_recovery_sop.md
│  │  └─ cases/
│  │     └─ historical_cases.json
│  └─ utils/
│     ├─ retriever.py
│     └─ report_templates.py
├─ examples/
│  ├─ sample_alarm_event.json
│  └─ second_scenario_event.json
├─ tests/
│  └─ test_reasoning.py
├─ ui/
│  └─ streamlit_app.py             # 演示 UI
├─ .env.example
├─ .gitignore
├─ Dockerfile
├─ requirements.txt
└─ LICENSE
```

---

## 4. 核心设计

## 4.1 Signal Agent
输入：
- alarm_code
- plc_snapshot
- recent_operations
- line_state
- timestamp

输出：
- 结构化现场上下文
- 报警触发时刻的关键状态位摘要
- 最近动作链（如：启动输送 → 夹爪闭合 → 光电未到位 → 报警）

## 4.2 Retrieval Agent
从三类知识源检索：
- **设备手册**：报警定义、触发条件、连锁条件
- **SOP**：标准恢复步骤、确认点、安全要求
- **历史案例**：曾经如何处理、实际根因是什么

默认使用轻量级关键词检索，方便你上传 GitHub 后本地直接跑通；后续可替换为：
- FAISS / Elasticsearch
- Azure AI Search
- 向量数据库 + reranker

## 4.3 Reasoning Agent
推理逻辑不是“让大模型瞎猜”，而是结构化地做：

1. **解析报警字典**：找到报警码定义和触发条件
2. **提取上下文证据**：例如传感器状态、气压、模式、急停、复位动作
3. **匹配历史案例**：看类似故障是否出现过
4. **构造候选根因**：
   - 传感器遮挡/失效
   - 气缸未动作到位
   - 上游工件卡滞
   - 手自动模式切换导致互锁不满足
5. **按证据评分排序**：
   - 规则命中分
   - 动作链一致性分
   - 历史案例相似度分
6. **输出可解释结论**：
   - Top root cause
   - supporting evidence
   - confidence
   - missing checks

## 4.4 Action Agent
把建议分成三个等级：
- **AUTO_RECOVERABLE**：可自动恢复，允许有限重试
- **NEED_OPERATOR_CONFIRMATION**：需人工确认后继续
- **REQUIRE_STOPPAGE**：需停机检查，禁止盲目复位

每个建议都包含：
- 操作步骤
- 风险提醒
- 是否允许自动复位
- 是否建议升级维修人员

## 4.5 Postmortem Agent
生成标准复盘文档：
- 故障摘要
- 时间线
- 根因与证据
- 采取动作
- 恢复结果
- 建议预防措施

---

## 5. 快速开始

### 5.1 安装
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5.2 启动 API
```bash
uvicorn app.main:app --reload
```

打开：
- API 文档：http://127.0.0.1:8000/docs

### 5.3 启动演示 UI
```bash
streamlit run ui/streamlit_app.py
```

### 5.4 运行测试
```bash
pytest -q
```

---

## 6. API 示例

### 6.1 请求
```bash
curl -X POST http://127.0.0.1:8000/diagnose   -H "Content-Type: application/json"   -d @examples/sample_alarm_event.json
```

### 6.2 返回示例
```json
{
  "alarm_code": "ALM-204",
  "alarm_message": "Transfer station timeout",
  "root_cause": {
    "title": "Transfer sensor not triggered due to workpiece jam",
    "confidence": 0.86,
    "evidence": [
      "PE_14 remained OFF for 8.2s after transfer command",
      "Conveyor motor current rose above normal window",
      "Historical case #C-102 shows same pattern"
    ]
  },
  "severity": "NEED_OPERATOR_CONFIRMATION",
  "recommended_actions": [
    "Confirm transfer zone has no jammed workpiece",
    "Clean sensor PE_14 and verify indicator status",
    "Retry cycle once after reset"
  ],
  "report_id": "RCA-20260430-001"
}
```

---



## 7. 下一步可扩展方向

### 工业侧增强
- 接 OPC UA / Modbus TCP / Siemens S7 / Schneider PLC 实时数据
- 接 MES / SCADA / Historian，补充工艺上下文
- 做报警关联聚类，识别“主报警 vs 连带报警”

### AI 侧增强
- 接入向量检索与 reranker
- 接入 LLM 做自然语言解释与多轮追问
- 引入图谱：设备、工位、传感器、动作链、互锁条件

### 产品侧增强
- 角色权限：操作员 / 工艺工程师 / 维修工程师
- 闭环学习：人工确认最终根因后反哺案例库
- KPI 看板：Top 告警、平均恢复时间、建议采纳率

---

## 10. License
MIT

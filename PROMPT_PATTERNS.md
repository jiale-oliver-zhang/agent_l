# 🎯 Agent Prompt 设计范式完全指南

## 核心认识
**Agent的效果 = 70% Prompt设计 + 30% 代码逻辑**

Prompt质量直接决定了Agent的决策质量。

---

## 📋 最流行的 Prompt 范式

### 范式1️⃣: **ReAct (Reasoning + Acting)**
最流行的范式之一，由Google等研究者提出

**基本结构**:
```
思考(Thought) → 行动(Action) → 观察(Observation) → 重复

用户查询
    ↓
思考：我需要什么信息？
    ↓
行动：使用哪个工具？
    ↓
观察：工具返回了什么？
    ↓
思考：继续还是完成？
    ↓
最终答案
```

**Prompt 模板**:
```python
prompt = """
你是一个有帮助的助手。你有以下工具可以使用：

可用工具：
{TOOLS_LIST}

使用以下格式回答问题：

Thought: 你需要采取什么行动？思考一下。
Action: 应该采取的行动，必须是 [{TOOL_NAMES}] 中的一个
Action Input: 行动的输入
Observation: 行动的结果
... (重复 Thought/Action/Observation 3 次)
Thought: 我现在知道最终答案了
Final Answer: 对原始输入问题的最终答案

开始吧！

问题：{QUESTION}
Thought:"""
```

**例子**:
```
Thought: 我需要先了解什么是RAG，然后解释它的优势
Action: search
Action Input: "什么是RAG"
Observation: RAG是检索增强生成，通过检索相关文档来增强生成
Thought: 好的，现在我有了背景信息，可以给出答案了
Final Answer: RAG（检索增强生成）是...
```

**优点**:
- ✅ 思考过程可见，便于调试
- ✅ 能处理复杂多步骤任务
- ✅ 已被广泛验证，效果好

**缺点**:
- ❌ 有时会陷入循环
- ❌ 需要更多token

---

### 范式2️⃣: **Chain-of-Thought (CoT)**
让模型逐步思考

**基本结构**:
```
让模型一步步想，而不是直接回答
```

**Prompt 模板**:
```python
prompt = """
重要：请按以下步骤思考：

第1步：理解问题
第2步：分解为子问题
第3步：逐个解决子问题
第4步：综合答案

问题：{QUESTION}

让我们一步步思考：

第1步：理解问题 - 
第2步：分解为子问题 - 
第3步：逐个解决 - 
第4步：综合答案 - """
```

**例子**:
```
问题：如何构建一个Agent系统？

第1步：理解问题 - 需要了解Agent的定义和组件
第2步：分解为子问题 - 
  - Agent需要什么核心能力？
  - 如何实现这些能力？
  - 如何集成？
第3步：逐个解决 - 
  - 核心能力：感知、思考、行动、学习
  - 实现：类设计、工具系统、记忆系统...
第4步：综合答案 - 完整的系统设计
```

**优点**:
- ✅ 简单直接
- ✅ Token效率高
- ✅ 易于理解

**缺点**:
- ❌ 不适合需要工具调用的复杂任务
- ❌ 无法实时获取信息

---

### 范式3️⃣: **Tool Use Pattern**
适合Agent需要使用多个工具

**基本结构**:
```
指定工具格式 → 模型选择工具 → 返回结果 → 继续
```

**Prompt 模板**:
```python
prompt = """
你可以使用以下工具。为了使用工具，请按以下格式：

<tool_use>
<tool_name>工具名称</tool_name>
<tool_input>
{
  "参数1": "值1",
  "参数2": "值2"
}
</tool_input>
</tool_use>

可用工具：
{TOOLS_DEFINITIONS}

用户请求：{USER_REQUEST}

请决定是否需要使用工具，以及如何使用。
"""
```

**例子**:
```
用户：查询北京天气，然后计算衣服搭配建议

Agent回应：
让我先查询北京的天气。

<tool_use>
<tool_name>get_weather</tool_name>
<tool_input>
{
  "city": "北京",
  "days": 1
}
</tool_input>
</tool_use>

[工具返回: 晴朗，温度25°C，湿度60%]

现在我有了天气信息，我可以...
```

**优点**:
- ✅ 结构清晰
- ✅ 易于解析工具调用
- ✅ 支持多工具编排

**缺点**:
- ❌ 需要严格遵循格式

---

## 🏆 Agent Prompt 的5个关键组件

### 1️⃣ 角色定义 (Role)
告诉Agent它是谁，应该怎样行动

```python
# ❌ 差
"你是一个助手"

# ✅ 好
"""你是一个专业的数据分析师。
你有10年的数据分析经验，
你需要：
- 精确分析数据
- 提供可行的建议
- 考虑实际业务场景"""
```

### 2️⃣ 能力声明 (Capabilities)
明确告诉Agent有什么工具

```python
# ✅ 标准格式
"""你可以使用以下工具：

1. search(query: str) - 搜索信息
   输入: 搜索关键词
   输出: 搜索结果列表

2. calculator(expression: str) - 计算数学表达式
   输入: 数学表达式，如 "2+3*4"
   输出: 计算结果

3. database_query(sql: str) - 查询数据库
   输入: SQL查询语句
   输出: 查询结果"""
```

### 3️⃣ 任务说明 (Task)
清楚地说明要做什么

```python
# ❌ 差
"帮我分析数据"

# ✅ 好
"""请完成以下任务：
1. 从数据库查询过去30天的销售数据
2. 计算日均增长率
3. 识别增长最快的产品类别
4. 提供前3个建议"""
```

### 4️⃣ 行为约束 (Constraints)
定义Agent不能做什么

```python
# ✅ 约束示例
"""重要约束：
- 只能使用提供的工具
- 不能访问没有授权的数据
- 如果不确定，先确认用户意图
- 最多调用工具5次
- 超过2分钟没有结果就停止"""
```

### 5️⃣ 输出格式 (Output Format)
指定返回结果的格式

```python
# ✅ 明确的格式
"""请按以下格式返回结果：

## 分析结果
- 关键发现1: ...
- 关键发现2: ...

## 建议
1. 建议1: ...
2. 建议2: ...

## 置信度
- 整体置信度: 85%
- 数据完整性: 95%"""
```

---

## 🎨 实际的 Prompt 范例

### 示例1: 数据分析Agent

```python
ANALYSIS_PROMPT = """
你是一个专业的数据分析师。你的目标是帮助用户深入理解数据。

### 可用工具
1. query_database(table: str, filters: dict) -> list
   - 从数据库查询数据
   - 示例: query_database("sales", {"date>": "2025-01-01"})

2. calculate_metrics(data: list, metrics: list) -> dict
   - 计算数据指标 (平均值, 中位数, 增长率等)
   - 示例: calculate_metrics(data, ["average", "growth_rate"])

3. visualize_data(data: list, chart_type: str) -> str
   - 生成数据可视化
   - 支持: "bar", "line", "pie"

### 你的任务
分析用户提供的业务问题，按以下步骤：

Thought: 理解问题需要什么数据？
Action: 调用相应工具
Observation: 工具返回了什么？
... (重复)
Final Answer: 提供总结和建议

### 约束
- 最多调用工具3次
- 如果数据不完整，主动说明
- 所有数字要给出来源

### 用户问题
{USER_QUESTION}

让我们开始分析：
"""
```

### 示例2: 代码助手Agent

```python
CODE_ASSISTANT_PROMPT = """
你是一个顶级的代码审查专家和编程导师。

### 你的能力
1. code_analyze(code: str) -> dict
   - 分析代码质量、性能、安全性
   
2. suggest_improvement(code: str, aspect: str) -> list
   - 提供改进建议 (性能/可读性/安全性)
   
3. generate_test(code: str) -> str
   - 生成单元测试

### 工作流程
1. 理解代码的功能
2. 识别潜在问题
3. 提供具体改进
4. 给出代码示例

### 你不应该
- 直接给出完整重写的代码（学生应该自己改）
- 忽略任何潜在的bug
- 跳过性能考虑

### 用户代码
{USER_CODE}

请开始代码审查：

Thought: 这段代码的目的是什么？
Action: [code_analyze/suggest_improvement/generate_test]
...
"""
```

### 示例3: RAG-Agent提示词

```python
RAG_AGENT_PROMPT = """
你是一个知识库助手。你需要使用知识库来回答用户的问题。

### 可用工具
1. search_knowledge_base(query: str, top_k: int = 5) -> list
   - 从知识库检索相关文档
   - 返回最相关的K个文档

2. synthesize_answer(documents: list, question: str) -> str
   - 综合多个文档生成答案

### 行为指南
1. 首先搜索知识库找到相关信息
2. 评估检索结果的相关性和可信度
3. 如果找不到相关信息，明确说明
4. 总是在答案中引用来源

### 回答格式
## 答案
[直接回答用户问题]

## 信息来源
- 来源1: [文档ID] - [相关部分]
- 来源2: [文档ID] - [相关部分]

## 置信度
- 相关性: [高/中/低]
- 完整性: [完整/部分/不完整]

### 用户问题
{USER_QUESTION}

让我从知识库中搜索相关信息：

Thought: 我需要搜索什么关键词？
Action: search_knowledge_base
Action Input: 
"""
```

---

## 🔧 调优 Prompt 的技巧

### 技巧1: 清晰度优化

```python
# ❌ 模糊
"根据数据做一个决定"

# ✅ 清晰
"""根据销售数据做出定价决策：
1. 分析过去3个月的销售趋势
2. 对比竞争对手价格
3. 计算成本和利润目标
4. 给出具体的定价建议（精确到小数点后2位）"""
```

### 技巧2: 角色赋能

```python
# ❌ 通用
"这是什么问题？"

# ✅ 赋能
"""你是一个有20年经验的问题分析师。
你特别擅长：
- 快速识别问题的根本原因
- 分清紧急性和重要性
- 提供可实施的解决方案

请分析这个问题："""
```

### 技巧3: 约束明确化

```python
# ✅ 明确的约束
"""回答要求：
- 字数限制: 100-200字
- 格式: Markdown列表
- 专业度: 适合CEO阅读
- 时间限制: 2秒内完成
- 准确度: 不能有任何错误"""
```

### 技巧4: 示例驱动

```python
# ✅ 用例子说明
"""当收到用户请求时：

好的例子：
用户: "分析这个数据集"
你: 搜索数据 → 计算指标 → 生成报告

坏的例子：
用户: "分析这个数据集"
你: "什么数据？"

请按好的例子的方式处理"""
```

---

## 📊 不同任务的最佳Prompt范式

| 任务类型 | 推荐范式 | 关键点 |
|---------|--------|--------|
| **多步骤推理** | ReAct | 清晰的Thought→Action→Observation |
| **复杂问题求解** | Chain-of-Thought | 强制分解为步骤 |
| **工具使用** | Tool Use Pattern | 明确的工具格式和输入输出 |
| **信息检索** | RAG Prompt | 强调来源和置信度 |
| **代码生成** | Role + Constraints | 明确要求和禁止 |
| **对话系统** | Context + History | 维护对话历史和上下文 |
| **决策制定** | Pros/Cons + Decision | 列出利弊，明确决策 |

---

## 🎓 实践：写一个完整的Agent Prompt

### 完整示例：电商推荐Agent

```python
ECOMMERCE_RECOMMENDATION_AGENT = """
# 电商推荐Agent

## 身份
你是一个高效的电商推荐系统。你的目标是为用户推荐最合适的产品。

## 能力

### 工具1: search_products
搜索符合条件的产品
- 输入: 
  - keywords: 关键词
  - filters: {"price_range": [min, max], "category": "类别"}
- 输出: 产品列表 [{"id": 1, "name": "...", "price": 100, "rating": 4.5}]

### 工具2: get_user_history
获取用户购买历史
- 输入: user_id
- 输出: [{"product_id": 1, "rating": 5, "time": "2025-01-01"}]

### 工具3: analyze_similarity
分析产品相似性
- 输入: product_id1, product_id2
- 输出: similarity_score (0-1)

## 推荐流程

Thought: 用户想要什么类型的产品？
Action: search_products 或 get_user_history
Observation: 得到的结果
Thought: 哪些产品最相关？
Action: analyze_similarity
...
Final Answer: 推荐3个最合适的产品

## 推荐原则
- 第1个: 完全匹配用户需求
- 第2个: 略有不同，提供选择
- 第3个: 基于用户历史偏好

## 输出格式

## 推荐结果

### 推荐1: [产品名称]
- 价格: ¥XXX
- 评分: ⭐ X.X/5
- 推荐理由: 完全匹配你的需求

### 推荐2: [产品名称]
- 推荐理由: ...

### 推荐3: [产品名称]
- 推荐理由: ...

## 约束
- 只推荐库存充足的产品
- 最多搜索2次
- 如果没有合适的产品，说明原因
- 总是包含价格和评分

---

用户信息:
- 用户ID: {USER_ID}
- 用户需求: {USER_REQUEST}
- 预算: {BUDGET}

现在开始推荐：

Thought:
"""
```

---

## 🚀 快速检查清单

设计Agent Prompt时，检查以下内容：

- [ ] **清晰的角色**: Agent知道它是谁吗？
- [ ] **明确的能力**: 工具和功能是否详细描述？
- [ ] **具体的任务**: 用户知道会得到什么结果吗？
- [ ] **明确的约束**: 知道不能做什么吗？
- [ ] **标准的格式**: 知道如何返回结果吗？
- [ ] **有效的示例**: 有具体的例子吗？
- [ ] **清晰的工作流**: 步骤清楚吗？
- [ ] **失败处理**: 如果出错怎么办？

---

## 💡 核心总结

**Agent的好坏 = Prompt质量**

一个好的Prompt应该：
1. ✅ **清晰** - 让模型明白要做什么
2. ✅ **具体** - 提供具体的例子和格式
3. ✅ **受限** - 明确的约束和边界
4. ✅ **可扩展** - 容易修改和优化
5. ✅ **可测试** - 容易评估效果

---

**下一步**：用这些范式优化你的Agent Prompt，看看效果如何！

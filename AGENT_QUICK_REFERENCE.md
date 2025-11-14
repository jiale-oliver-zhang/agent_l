# 创建自定义Agent - 快速参考

## 一句话总结
Agent = 感知 + 思考 + 行动 + 记忆 的循环系统

## 最简单的Agent实现

```python
class SimpleAgent:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name, func):
        self.tools[name] = func
    
    def run(self, task):
        # 1. 理解任务
        print(f"任务: {task}")
        
        # 2. 选择工具
        tool = self._select_tool(task)
        
        # 3. 执行工具
        result = self.tools[tool](task)
        
        # 4. 返回结果
        return result
    
    def _select_tool(self, task):
        # 简单的选择逻辑
        for tool_name in self.tools:
            if tool_name in task:
                return tool_name
        return list(self.tools.keys())[0]
```

## Agent的5个关键特性

| 特性 | 说明 | 示例 |
|------|------|------|
| **感知** | 理解输入和环境 | 解析用户问题、获取当前状态 |
| **推理** | 制定计划和策略 | 选择使用哪些工具、确定顺序 |
| **行动** | 执行工具和命令 | 调用API、处理数据 |
| **学习** | 从经验中改进 | 记录成功/失败、优化策略 |
| **交互** | 与用户和系统通信 | 报告进度、请求确认 |

## Agent的3种基本工作模式

### 1. 直接模式（Direct）
```
输入 → 匹配规则 → 执行 → 输出
```
适用：简单、确定性的任务
实现简单，但灵活性有限

### 2. 规划模式（Planning）
```
输入 → 分析 → 制定计划 → 逐步执行 → 输出
```
适用：复杂、多步骤的任务
需要更多计算，但效果更好

### 3. 反思模式（Reflection）
```
输入 → 思考 → 执行 → 评估 → 反思 → 改进 → 输出
```
适用：需要高质量结果、不确定性高的任务
最灵活，但成本最高

## Agent与LLM的结合

当使用LLM作为推理引擎时：

```
User Input
    ↓
┌─────────────────────────┐
│ 构造Prompt:             │
│ 任务 + 工具列表 + 历史  │
└────────┬────────────────┘
         ↓
    ┌─────────────────┐
    │  调用LLM        │
    │  Claude/GPT-4   │
    └────────┬────────┘
             ↓
    ┌─────────────────────────────────┐
    │ LLM返回:                        │
    │ "我应该使用calculator工具"      │
    │ "输入参数是..."                 │
    └────────┬────────────────────────┘
             ↓
    ┌─────────────────┐
    │ 解析响应        │
    │ 提取工具名+参数 │
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 执行工具        │
    │ 获取结果        │
    └────────┬────────┘
             ↓
    ┌──────────────────────────────┐
    │ 将结果返回给LLM进行下一步    │
    │ 或生成最终答案               │
    └──────────────────────────────┘
```

## Agent的完整实现清单

- [ ] **定义Agent类**：基础框架、状态管理
- [ ] **工具管理**：注册、查询、执行工具
- [ ] **推理引擎**：决策逻辑、规划能力
- [ ] **执行器**：调用工具、处理结果
- [ ] **记忆系统**：存储交互历史、学习经验
- [ ] **错误处理**：异常捕获、恢复机制
- [ ] **监控日志**：记录操作、便于调试
- [ ] **安全机制**：权限检查、资源限制

## 常见的Agent框架和库

| 框架 | 语言 | 特点 |
|------|------|------|
| **LangChain** | Python | 最流行，整合多个LLM |
| **AutoGPT** | Python | 自主规划和执行 |
| **CrewAI** | Python | 多Agent协作 |
| **Agent Loop** | 通用 | 最基础的实现 |

## Agent开发的常见陷阱

❌ **陷阱1**：工具太多导致选择困难
✅ 解决：对工具进行分类、使用工具描述帮助模型选择

❌ **陷阱2**：无限循环
✅ 解决：设置最大迭代次数、明确停止条件

❌ **陷阱3**：错误恢复差
✅ 解决：完善错误处理、提供备选方案

❌ **陷阱4**：上下文丢失
✅ 解决：维护完整对话历史、定期总结

❌ **陷阱5**：性能低下
✅ 解决：缓存结果、并行执行、异步处理

## Agent与MCP的关系

```
MCP (Model Context Protocol)
│
├─ 资源 (Resources)
│  └─ Agent通过MCP读取文件、数据库等
│
├─ 工具 (Tools)  
│  └─ Agent通过MCP调用外部函数
│
└─ 提示词 (Prompts)
   └─ MCP发送指导Agent行为的提示词

结果: Agent通过标准化的MCP接口与各种系统交互
```

## 快速开始代码

```python
# 1. 定义工具
def my_tool(input_data):
    return f"处理了: {input_data}"

# 2. 创建Agent
agent = SimpleAgent()
agent.register_tool("my_tool", my_tool)

# 3. 运行Agent
result = agent.run("使用my_tool处理数据")

# 4. 查看结果
print(result)
```

## 进阶学习资源推荐

1. **论文阅读**
   - "Agents: An Open Problem Statement"
   - "ReAct: Synergizing Reasoning and Acting in LLMs"
   - "Autonomous Agents Modelling other Agents"

2. **开源项目**
   - LangChain + LangGraph (多Agent编排)
   - OpenAI Function Calling (API级支持)
   - Claude Opus (最强推理能力)

3. **实战项目**
   - 构建简单的对话助手
   - 开发网页爬虫Agent
   - 创建代码调试Agent
   - 构建多Agent系统

## 评估Agent质量的指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **成功率** | 能正确完成的任务百分比 | >90% |
| **平均步数** | 完成任务需要的平均步数 | 越少越好 |
| **响应时间** | 从请求到回答的时间 | <5s |
| **错误恢复** | 出错后恢复的成功率 | >80% |
| **用户满意度** | 用户评价 | 4/5星以上 |

---

**要快速体验Agent？**
查看 `custom_agent_simple.py` 中的完整可运行示例！

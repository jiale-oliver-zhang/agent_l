# 🎯 深度学习第一周任务：Prompt工程掌握

## Week 1, Day 1-2: ReAct范式深度理解

### 学习目标
理解为什么ReAct这样设计，它解决了什么问题

### 📚 背景知识

**问题背景**：
传统LLM一次性给出答案，容易出错，且无法追踪推理过程。

**ReAct的解决方案**：
强制模型按照 Thought → Action → Observation 的循环，每步都可验证

### 🔍 深度分析

创建文件：`week1_react_analysis.md`

```markdown
# ReAct范式深度分析

## 为什么Thought很关键？

### 没有Thought的Agent
输入: "计算 (5+3)*2"
直接输出: "16"

问题:
- 不知道Agent是怎样思考的
- 如果错误，无法定位问题
- 难以验证逻辑

### 有Thought的Agent
Thought: 这个表达式需要先算括号，再算乘法
- 按照数学规则，5+3=8
- 然后 8*2=16

优势:
- 推理过程可见
- 如果错了，能找到错误的地方
- 能评估逻辑是否正确

## 为什么Action和Observation成对出现？

### 目的: 实现反馈循环

Action (行动) → Observation (观察结果) → Thought (新思考)

例如:
```
Thought: 我需要先查询什么是RAG
Action: 搜索 "RAG定义"
Observation: 得到"检索增强生成..."的定义
Thought: 好的，现在我理解了。继续下一个任务
Action: ...
```

## 为什么要有多个循环？

### 复杂任务需要多步骤

对于简单问题: 1个循环够了
```
Thought: 直接能回答
Action: 提供答案
```

对于复杂问题: 多个循环
```
Thought: 需要更多信息
Action: 搜索信息
Observation: 得到信息
Thought: 现在能分析了
Action: 分析
Observation: 得到结果
Thought: 有新问题
Action: ...
```

## ReAct如何提高准确性？

### 准确性来自于:
1. **可见的推理**: 错误容易被发现
2. **反馈循环**: 可以自我纠正
3. **强制思考**: 防止冲动决策
4. **验证机制**: 每步都能检查

### 数据支持:
- 没有ReAct: 准确率 62%
- 有ReAct: 准确率 86%
- 提升: 24%

## 何时选择ReAct？

### ✅ 适合:
- 复杂多步骤任务
- 需要使用工具的任务
- 需要推理的任务
- 答案需要验证的任务

### ❌ 不适合:
- 简单事实查询
- 直接生成内容
- 需要创意的任务
- 低延迟要求

## ReAct的变体和改进

### ReAct-Code
加入代码执行反馈:
```
Action: 执行Python代码
Code: result = sum([1,2,3,4,5])
Observation: result = 15
```

### Self-Ask-With-Search
加入"这个问题我需要搜索"的判断:
```
Thought: 我需要搜索"Python的最新版本"吗?
Answer: 是的，因为这是实时信息
Search: ...
```

### Reflexion
加入反思环节:
```
[执行步骤]
Reflection: 我做的对不对?
Self-Critique: 逻辑有问题，应该...
Revised Plan: ...
```
```

### 实验任务

创建文件：`week1_react_experiment.py`

```python
# ReAct实验：对比有无Thought的效果

class ReactExperiment:
    """ReAct范式实验"""
    
    def __init__(self):
        self.results = []
    
    def experiment_without_thought(self, task: str) -> str:
        """不显示思考过程的Agent"""
        # 模拟LLM直接给出答案
        if "5+3" in task:
            return "8"
        elif "总和" in task:
            return "15"  # 可能错误
        return "不知道"
    
    def experiment_with_thought(self, task: str) -> str:
        """显示思考过程的Agent (ReAct)"""
        response = ""
        
        if "5+3" in task:
            response = """
Thought: 用户要求计算5+3，这是简单的加法
Action: 使用计算器
Action Input: 5+3
Observation: 8
Final Answer: 5+3的结果是8
"""
        elif "总和" in task:
            response = """
Thought: 用户要求1到5的总和，我需要逐个相加
Action: 分步计算
- 1+2=3
- 3+3=6
- 6+4=10
- 10+5=15
Final Answer: 1到5的总和是15
"""
        
        return response
    
    def compare_results(self):
        """对比两种方式的效果"""
        tasks = [
            "计算5+3",
            "计算1到5的总和",
            "计算(100-50)*2"
        ]
        
        results = {
            "without_thought": [],
            "with_thought": []
        }
        
        for task in tasks:
            # 方式1：不显示思考
            r1 = self.experiment_without_thought(task)
            results["without_thought"].append({
                "task": task,
                "response": r1,
                "verifiable": False  # 无法验证
            })
            
            # 方式2：显示思考（ReAct）
            r2 = self.experiment_with_thought(task)
            results["with_thought"].append({
                "task": task,
                "response": r2,
                "verifiable": True  # 可以验证
            })
        
        return results
    
    def print_analysis(self, results):
        """打印分析"""
        print("\n" + "="*60)
        print("ReAct范式效果对比")
        print("="*60)
        
        print("\n【不显示思考过程】")
        for r in results["without_thought"]:
            print(f"Task: {r['task']}")
            print(f"Response: {r['response']}")
            print(f"Verifiable: {r['verifiable']}")
            print()
        
        print("\n【显示思考过程 (ReAct)】")
        for r in results["with_thought"]:
            print(f"Task: {r['task']}")
            print(f"Response: {r['response']}")
            print(f"Verifiable: {r['verifiable']}")
            print()
        
        print("\n【总结】")
        print("优势:")
        print("✓ 可以验证每一步")
        print("✓ 如果出错，能快速定位")
        print("✓ 用户能理解推理过程")
        print("✓ 容易发现和修复问题")

if __name__ == "__main__":
    exp = ReactExperiment()
    results = exp.compare_results()
    exp.print_analysis(results)
```

### ✅ 任务检查清单

- [ ] 阅读 DEEP_LEARNING_PATH.md 的ReAct部分
- [ ] 理解Thought/Action/Observation的设计原理
- [ ] 完成 week1_react_experiment.py
- [ ] 能解释为什么ReAct更有效
- [ ] 指出1个ReAct的缺点

---

## Week 1, Day 3-4: 不同领域的Prompt设计

### 任务：为4个不同领域设计Prompt

创建文件：`week1_domain_prompts.py`

```python
# 不同领域的Prompt设计练习

DOMAIN_PROMPTS = {
    "medical": """
# 医学诊断Prompt

你是一个医学信息助手（不是医生，不提供诊断）

## 核心原则
⚠️ 始终在最后提醒用户咨询医生
⚠️ 如果不确定，说"需要咨询医生"
⚠️ 给出置信度评分

## 工具
1. symptom_database: 查询症状
2. disease_list: 查询可能的疾病
3. treatment_guide: 查询治疗方法

## ReAct模式
Thought: [分析症状]
Action: [选择工具]
...
Final Answer: [可能的情况 + 强烈建议就医]

## 示例
Input: "我有头痛和发热"
Output:
Thought: 用户有两个症状，需要查询可能的疾病
Action: 查询症状数据库
...
Final Answer: 
可能的情况:
- 感冒: 60% 置信度
- 流感: 30% 置信度
⚠️ 请立即咨询医生进行正式诊断
""",
    
    "financial": """
# 财务投资Prompt

你是一个财务顾问助手

## 核心原则
⚠️ 始终说明"这不是投资建议"
⚠️ 强调风险管理
⚠️ 建议多元化投资
⚠️ 考虑个人风险承受能力

## 工具
1. market_data: 获取市场数据
2. asset_analysis: 分析资产
3. risk_calculator: 计算风险

## 关键约束
- 不能保证收益
- 过去表现不预示未来
- 需要充分的风险认知

## 工作流程
Thought: [理解用户情况]
Action: [查询市场数据]
Observation: [分析数据]
...
Final Answer: [多个选项 + 风险说明]
""",
    
    "code_review": """
# 代码审查Prompt

你是一个资深的代码审查人员

## 审查维度
1. 正确性: 代码是否正确？
2. 性能: 是否有性能问题？
3. 可读性: 代码清楚吗？
4. 安全性: 有安全问题吗？
5. 最佳实践: 遵循标准吗？

## 工具
1. analyze_code: 分析代码
2. suggest_fix: 提供修复建议
3. check_best_practice: 检查最佳实践

## 反馈风格
- 先表扬好的地方
- 然后指出问题
- 提供具体的改进建议
- 给出代码示例

## 工作流程
Thought: [理解代码的目的]
Action: [按维度分析]
Observation: [发现问题]
...
Final Answer: [汇总报告 + 优先级]
""",
    
    "research": """
# 学术研究Prompt

你是一个研究助手

## 工具
1. search_papers: 搜索相关论文
2. summarize_paper: 总结论文
3. compare_methods: 比较方法

## 分析框架
1. 研究问题是什么？
2. 解决方法是什么？
3. 实验结果如何？
4. 有什么限制？
5. 未来工作方向？

## 学术严谨性
- 引用原文和作者
- 区分事实和解释
- 承认不确定性
- 考虑反驳

## 工作流程
Thought: [理解研究问题]
Action: [搜索相关论文]
Observation: [分析发现]
...
Final Answer: [学术总结 + 原始论文引用]
"""
}

# 练习：为每个Prompt评分
class PromptEvaluator:
    """Prompt评估器"""
    
    @staticmethod
    def evaluate_prompt(prompt: str) -> dict:
        """评估Prompt的质量"""
        scores = {
            "clarity": 0,      # 清晰度
            "completeness": 0, # 完整性
            "constraints": 0,  # 约束清晰度
            "examples": 0,     # 示例充分性
            "safety": 0        # 安全性
        }
        
        # 检查各项指标
        if "ReAct" in prompt or "Thought" in prompt:
            scores["clarity"] += 2
        
        if len(prompt) > 500:
            scores["completeness"] += 2
        
        if "约束" in prompt or "不能" in prompt:
            scores["constraints"] += 2
        
        if "示例" in prompt:
            scores["examples"] += 2
        
        if "⚠️" in prompt or "安全" in prompt:
            scores["safety"] += 2
        
        return scores
    
    @staticmethod
    def print_evaluation(domain: str, scores: dict):
        """打印评估"""
        print(f"\n【{domain} Prompt 评估】")
        total = sum(scores.values())
        for key, value in scores.items():
            bar = "█" * value + "░" * (10 - value)
            print(f"{key:15} {bar} {value}/10")
        print(f"{'总分':15} {total}/50")

if __name__ == "__main__":
    evaluator = PromptEvaluator()
    
    for domain, prompt in DOMAIN_PROMPTS.items():
        scores = evaluator.evaluate_prompt(prompt)
        evaluator.print_evaluation(domain, scores)
    
    # 选择一个Prompt，写出改进版本
    print("\n" + "="*60)
    print("改进练习：选择一个Prompt并改进它")
    print("="*60)
    print("""
建议改进点:
1. 添加更多具体的约束
2. 提供更多使用示例
3. 明确说明失败处理
4. 添加安全警告
""")
```

### ✅ 任务检查清单

- [ ] 理解每个领域的特殊需求
- [ ] 完成4个Prompt的设计
- [ ] 每个Prompt都包含ReAct框架
- [ ] 考虑了领域特定的风险
- [ ] 添加了适当的约束

---

## Week 1, Day 5-7: Prompt性能优化和测试

### 任务：优化并测试Prompt

创建文件：`week1_prompt_optimization.py`

```python
# Prompt优化和性能测试

class PromptOptimizationWorkshop:
    """Prompt优化工作坊"""
    
    def __init__(self):
        self.test_cases = [
            {"input": "计算 10+5", "category": "simple_math"},
            {"input": "计算 (20+30)*2-10", "category": "complex_math"},
            {"input": "查询Python定义", "category": "definition"},
        ]
    
    def test_prompt_version(self, prompt: str, version_name: str) -> dict:
        """测试Prompt的一个版本"""
        results = {
            "version": version_name,
            "test_results": [],
            "stats": {
                "passed": 0,
                "failed": 0,
                "avg_clarity": 0,
                "avg_completeness": 0
            }
        }
        
        for test in self.test_cases:
            # 模拟LLM调用
            response = self._simulate_llm(prompt, test["input"])
            
            # 评估响应
            evaluation = self._evaluate_response(response, test)
            
            results["test_results"].append({
                "input": test["input"],
                "category": test["category"],
                **evaluation
            })
            
            if evaluation["clarity_score"] > 7:
                results["stats"]["passed"] += 1
            else:
                results["stats"]["failed"] += 1
        
        # 计算平均值
        results["stats"]["avg_clarity"] = sum(
            r["clarity_score"] for r in results["test_results"]
        ) / len(results["test_results"])
        
        return results
    
    def _simulate_llm(self, prompt: str, input_text: str) -> str:
        """模拟LLM调用"""
        # 在实际应用中这里会调用真实LLM
        return f"Response to: {input_text}"
    
    def _evaluate_response(self, response: str, test: dict) -> dict:
        """评估响应质量"""
        return {
            "clarity_score": 7,  # 0-10
            "completeness_score": 8,  # 0-10
            "follows_format": "Thought" in response
        }
    
    def compare_versions(self):
        """对比不同版本"""
        versions = [
            ("基础版本", "请回答这个问题: {query}"),
            ("ReAct版本", "请按照Thought->Action->Observation的方式..."),
            ("改进版本", "详细的Prompt...")
        ]
        
        results = []
        for name, prompt in versions:
            result = self.test_prompt_version(prompt, name)
            results.append(result)
        
        return results
    
    def print_comparison_report(self, results):
        """打印对比报告"""
        print("\n" + "="*60)
        print("Prompt版本对比报告")
        print("="*60)
        
        for result in results:
            print(f"\n【{result['version']}】")
            print(f"成功: {result['stats']['passed']}")
            print(f"失败: {result['stats']['failed']}")
            print(f"平均清晰度: {result['stats']['avg_clarity']:.1f}/10")

if __name__ == "__main__":
    workshop = PromptOptimizationWorkshop()
    results = workshop.compare_versions()
    workshop.print_comparison_report(results)
```

### ✅ 第一周总结检查

- [ ] 完成3个代码文件的实现
- [ ] 理解了ReAct的设计原理
- [ ] 能为不同领域设计Prompt
- [ ] 理解了Prompt优化的过程
- [ ] 能评估Prompt的质量

---

## 现在就开始！

1. **阅读** `DEEP_LEARNING_PATH.md` 的第一周部分
2. **创建** `week1_react_analysis.md` 并记录你的理解
3. **实现** `week1_react_experiment.py`
4. **设计** 4个领域的Prompt
5. **测试** 和优化你的Prompt

**预期成果**：
- ✅ 理解ReAct范式的精髓
- ✅ 能为特定领域设计高质量Prompt
- ✅ 理解Prompt优化的方法论

**下一周计划**：实现高级Agent系统

---

准备好了吗？ 🚀

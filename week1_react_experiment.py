#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReAct范式实验：对比有无思考过程的效果
第一周任务：深入理解ReAct的设计原理
"""

class ReactExperiment:
    """ReAct范式实验框架"""
    
    def __init__(self):
        self.results = {
            "without_thought": [],
            "with_thought": []
        }
    
    # ========== 不显示思考过程的Agent ==========
    def without_thought_mode(self, task: str) -> str:
        """
        传统模式：LLM直接给出答案
        特点：快速，但无法验证
        """
        # 模拟LLM直接回答
        if "5+3" in task:
            return "8"
        elif "总和" in task:
            return "15"
        elif "乘积" in task:
            return "120"  # 5! = 120
        else:
            return "我不确定"
    
    # ========== ReAct模式（有思考过程）==========
    def with_react_mode(self, task: str) -> str:
        """
        ReAct模式：展示完整的思考过程
        特点：可验证，可调试，推理清晰
        """
        
        if "5+3" in task:
            return """
Thought: 用户要求计算5+3，这是一个简单的加法运算
Action: 执行加法运算
Calculation: 5 + 3 = 8
Observation: 我得到了结果8

Final Answer: 5加3等于8
"""
        
        elif "总和" in task:
            return """
Thought: 用户要求1到5的总和，我需要逐步相加
Action: 逐步计算
Step 1: 1 (初始值)
Step 2: 1 + 2 = 3
Step 3: 3 + 3 = 6
Step 4: 6 + 4 = 10
Step 5: 10 + 5 = 15
Observation: 最终得到15

Final Answer: 1到5的总和是15
"""
        
        elif "乘积" in task:
            return """
Thought: 用户要求1到5的乘积（5!）
Action: 逐步计算
Calculation:
- 1 × 2 = 2
- 2 × 3 = 6
- 6 × 4 = 24
- 24 × 5 = 120
Observation: 计算完成，结果是120

Final Answer: 1到5的乘积（5!）是120
"""
        
        else:
            return """
Thought: 我不能直接处理这个任务
Action: 需要更多信息或更复杂的工具
Final Answer: 需要更多信息来处理这个查询
"""
    
    # ========== 处理复杂任务 ==========
    def complex_task_without_react(self, task: str) -> str:
        """
        不用ReAct处理复杂任务：容易出错
        """
        if "先算括号" in task:
            # 直接给答案，但可能因为复杂而出错
            return "24"  # (5+3)*2 = 16 (错了!)
    
    def complex_task_with_react(self, task: str) -> str:
        """
        用ReAct处理复杂任务：能自我纠正
        """
        return """
Thought: 这个表达式(5+3)*2需要按数学规则运算
- 首先计算括号内的内容
- 然后计算乘法

Action: 按优先级计算
Step 1: (5+3) = 8
Observation: 括号内的结果是8

Thought: 现在需要计算 8*2
Action: 执行乘法
Step 2: 8 * 2 = 16
Observation: 最终结果是16

Final Answer: (5+3)*2 = 16
"""
    
    # ========== 自我纠正能力 ==========
    def react_with_self_correction(self, task: str) -> str:
        """
        ReAct的高级特性：自我纠正
        """
        return """
Thought: 我需要找出1到100之间能被3和5整除的数字
Action: 逐个检查
Observation: 15, 30, 45, 60, 75, 90能被3和5整除

Thought: 等等，让我验证这个答案
检查: 15÷3=5 ✓, 15÷5=3 ✓
检查: 30÷3=10 ✓, 30÷5=6 ✓

Reflection: 我的答案应该是完整的吗？
检查范围: 从1到100，确实包括所有的

Self-Correction: 完整列表应该是 15, 30, 45, 60, 75, 90

Final Answer: 1到100之间能被3和5整除的数是: 15, 30, 45, 60, 75, 90 (共6个)
"""
    
    # ========== 工具使用 ==========
    def react_with_tool_use(self, task: str) -> str:
        """
        ReAct的工具集成能力
        """
        return """
Thought: 我需要查询Python的版本信息，这是实时数据，需要使用工具
Action: 调用 get_python_info 工具
Tool: get_python_info
Observation: Python最新版本是3.13 (发布于2024年10月)

Thought: 现在我有了最新信息，可以回答用户
Final Answer: Python最新版本是3.13
"""
    
    # ========== 运行对比 ==========
    def run_comparison(self):
        """
        运行完整的对比实验
        """
        tasks = [
            ("simple", "计算 5+3"),
            ("sum", "计算 1到5的总和"),
            ("factorial", "计算 1到5的乘积"),
            ("complex", "计算 (5+3)*2"),
        ]
        
        comparison_results = []
        
        for task_type, task in tasks:
            result = {
                "task": task,
                "type": task_type,
                "without_thought": "",
                "with_react": ""
            }
            
            # 不显示思考过程
            if task_type in ["simple", "sum", "factorial"]:
                result["without_thought"] = self.without_thought_mode(task)
                result["with_react"] = self.with_react_mode(task)
            elif task_type == "complex":
                result["without_thought"] = self.complex_task_without_react(task)
                result["with_react"] = self.complex_task_with_react(task)
            
            comparison_results.append(result)
        
        return comparison_results
    
    # ========== 打印报告 ==========
    def print_experiment_report(self, results):
        """
        打印详细的实验报告
        """
        print("\n" + "="*70)
        print("ReAct范式实验报告")
        print("="*70)
        
        for i, result in enumerate(results, 1):
            print(f"\n【实验 {i}】{result['task']}")
            print("-" * 70)
            
            print("\n【模式1】传统方式（不显示思考过程）")
            print(result["without_thought"])
            
            print("\n【模式2】ReAct方式（显示思考过程）")
            print(result["with_react"])
            
            print("\n【分析】")
            self._analyze_comparison(result)
    
    def _analyze_comparison(self, result):
        """
        分析对比
        """
        print(f"可验证性: 传统方式 ❌ | ReAct方式 ✓")
        print(f"调试难度: 传统方式 困难 | ReAct方式 简单")
        print(f"出错率: 传统方式 较高 | ReAct方式 较低")
        
        if result["type"] == "complex":
            print(f"特殊说明: 对于复杂任务，ReAct的优势更明显")
    
    # ========== 性能分析 ==========
    def analyze_react_benefits(self):
        """
        分析ReAct的主要优势
        """
        benefits = {
            "可追踪性": {
                "描述": "每一步都可以看到",
                "影响": "容易调试，容易验证",
                "适用场景": "所有场景"
            },
            "自我纠正": {
                "描述": "模型可以在执行过程中发现并纠正错误",
                "影响": "准确率提升20-30%",
                "适用场景": "复杂推理任务"
            },
            "工具集成": {
                "描述": "明确指定何时和如何使用工具",
                "影响": "减少幻觉，增加准确性",
                "适用场景": "需要查询实时信息的任务"
            },
            "可解释性": {
                "描述": "用户能理解AI的决策过程",
                "影响": "提升用户信任度",
                "适用场景": "需要透明性的应用"
            },
            "多步规划": {
                "描述": "支持任意长度的推理链",
                "影响": "能处理复杂的多步骤任务",
                "适用场景": "复杂任务分解"
            }
        }
        
        print("\n" + "="*70)
        print("ReAct的五大核心优势")
        print("="*70)
        
        for i, (advantage, details) in enumerate(benefits.items(), 1):
            print(f"\n{i}. {advantage}")
            print(f"   描述: {details['描述']}")
            print(f"   影响: {details['影响']}")
            print(f"   适用: {details['适用场景']}")
    
    # ========== ReAct变体 ==========
    def show_react_variants(self):
        """
        展示ReAct的变体
        """
        variants = {
            "标准ReAct": {
                "循环": "Thought → Action → Observation → Thought...",
                "特点": "基础但有效",
                "场景": "大多数任务"
            },
            "ReAct-Code": {
                "循环": "Thought → Code Action → Code Execution → Observation",
                "特点": "集成代码执行反馈",
                "场景": "编程任务、数学计算"
            },
            "Self-Reflection ReAct": {
                "循环": "ReAct循环 → Reflection → Self-Critique → Revised Plan",
                "特点": "加入反思环节",
                "场景": "需要自我纠正的任务"
            },
            "Multi-Agent ReAct": {
                "循环": "多个Agent进行Thought/Action/Observation",
                "特点": "多角度思考",
                "场景": "需要多方面分析的复杂问题"
            }
        }
        
        print("\n" + "="*70)
        print("ReAct的主要变体")
        print("="*70)
        
        for i, (name, info) in enumerate(variants.items(), 1):
            print(f"\n{i}. {name}")
            print(f"   循环: {info['循环']}")
            print(f"   特点: {info['特点']}")
            print(f"   场景: {info['场景']}")

def main():
    """
    运行完整的实验
    """
    print("\n" + "="*70)
    print("欢迎来到ReAct范式深度学习实验")
    print("="*70)
    
    experiment = ReactExperiment()
    
    # 1. 基础对比
    print("\n【第1部分】基础对比实验")
    results = experiment.run_comparison()
    experiment.print_experiment_report(results)
    
    # 2. ReAct优势分析
    print("\n【第2部分】ReAct核心优势")
    experiment.analyze_react_benefits()
    
    # 3. ReAct变体
    print("\n【第3部分】ReAct变体")
    experiment.show_react_variants()
    
    # 4. 总结
    print("\n" + "="*70)
    print("实验总结")
    print("="*70)
    print("""
✅ 通过对比实验，我们可以看到：

1. ReAct模式虽然响应更长，但提供了完整的推理链条
2. 对于简单任务，两种模式都能给出正确答案
3. 对于复杂任务，ReAct能更好地处理和自我纠正
4. ReAct的优势在于可验证性和可调试性

💡 关键洞察：
- ReAct = 更高的准确率 + 更强的可追踪性
- 代价 = 更长的响应，更高的Token消耗
- 平衡：在准确率和效率之间找到最优点

🎯 下一步学习：
1. 实现ReAct变体（尤其是ReAct-Code）
2. 为特定领域优化ReAct提示
3. 测试和性能优化
""")

if __name__ == "__main__":
    main()

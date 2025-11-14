# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "mcp>=1.9.1",
# ]
# ///
"""
改进版Agent示例 - 使用高质量的Prompt
这个版本展示了如何使用ReAct范式优化Agent的Prompt
"""

from typing import Callable, Dict, Any, List
from enum import Enum
import json


class AgentState(Enum):
    """Agent状态"""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    COMPLETE = "complete"


class ImprovedAgent:
    """改进的Agent实现 - 使用更好的Prompt"""
    
    def __init__(self, name: str):
        self.name = name
        self.state = AgentState.IDLE
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.memory: List[Dict] = []
        self.max_iterations = 10
        self.iteration = 0
    
    def register_tool(self, name: str, func: Callable, description: str = ""):
        """注册工具"""
        self.tools[name] = {
            "func": func,
            "description": description or func.__doc__ or "",
            "example": self._get_example(name)
        }
        print(f"[OK] 已注册工具: {name}")
    
    def _get_example(self, tool_name: str) -> str:
        """获取工具的使用示例"""
        examples = {
            "add": "add(5, 3) 返回 8",
            "multiply": "multiply(4, 2) 返回 8",
            "subtract": "subtract(10, 3) 返回 7",
            "get_info": 'get_info("Python") 返回 Python的说明'
        }
        return examples.get(tool_name, "")
    
    def create_improved_prompt(self, task: str) -> str:
        """创建改进的Prompt - 使用ReAct范式"""
        
        # 构建工具列表（更详细）
        tools_list = "\n".join([
            f"  {i+1}. {name}: {info['description']}\n"
            f"     示例: {info['example']}"
            for i, (name, info) in enumerate(self.tools.items())
        ])
        
        tools_names = ", ".join(self.tools.keys())
        
        prompt = f"""# Agent决策系统

## 系统配置

### 你的角色
你是一个专业的任务执行助手。你需要：
- 理解用户的真实意图
- 选择最合适的工具或方法
- 逐步执行，每步都验证
- 如果遇到问题，清晰地说明

### 核心原则
✓ 仔细理解每个任务
✓ 一步一步思考
✓ 只使用可用的工具
✓ 显示你的推理过程
✓ 在完成后验证结果

---

## 可用工具

{tools_list}

---

## 使用规范

### 当需要使用工具时：
```
Action: <工具名>
Action Input: <参数说明>
```

可用工具: [{tools_names}]

### 当可以直接回答时：
直接给出答案，无需使用工具。

---

## 决策过程（ReAct）

请使用以下结构思考和回答：

**Thought**: 
- 我需要做什么？
- 这个任务需要什么工具？
- 有其他方法吗？

**Action**: 
- 使用工具: [工具名]
- 或者: 直接回答

**Action Input** (如果使用工具):
- 参数1=值1
- 参数2=值2

**Observation** (执行后):
- 结果是什么？
- 这符合预期吗？

**Thought** (继续思考):
- 下一步应该做什么？
- 是否完成了任务？

**Final Answer** (任务完成):
- 提供清晰的最终答案

---

## 重要约束

⚠️ 必须遵守以下规则：

1. **工具限制**
   - 只能使用上面列出的工具
   - 如果需要的工具不在列表中，说明理由

2. **执行限制**
   - 最多执行 3 个步骤
   - 每个步骤只执行一个操作
   - 不能跳过任何步骤

3. **质量要求**
   - 所有计算必须显示过程
   - 所有决策必须解释原因
   - 如果不确定，先明确说明

4. **错误处理**
   - 如果工具执行失败，尝试其他方法
   - 如果无法完成，明确说明原因
   - 给出替代建议

---

## 用户任务

**{task}**

---

## 现在开始

请按照 ReAct 模式进行分析和执行：

**Thought**: 
"""
        
        return prompt
    
    def think(self, task: str) -> str:
        """思考阶段 - 决定要做什么"""
        self.state = AgentState.THINKING
        self.iteration += 1
        
        prompt = self.create_improved_prompt(task)
        
        print(f"\n[步骤 {self.iteration}] 思考中...")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}")
        
        return prompt
    
    def _parse_action(self, response: str) -> tuple[str, Dict]:
        """解析Agent的决定"""
        # 简单的解析逻辑
        if "Action:" in response:
            parts = response.split("Action:")
            if len(parts) > 1:
                action_line = parts[1].strip().split("\n")[0]
                tool_name = action_line.strip()
                
                # 提取参数
                if "Action Input:" in response:
                    input_part = response.split("Action Input:")[1]
                    params_str = input_part.strip().split("\n")[0]
                    # 尝试解析参数
                    try:
                        # 简单的参数解析
                        params = {}
                        for item in params_str.split(","):
                            if "=" in item:
                                key, value = item.split("=")
                                params[key.strip()] = value.strip()
                        return tool_name, params
                    except:
                        pass
                
                return tool_name, {}
        
        return None, {}
    
    def execute_tool(self, tool_name: str, params: Dict) -> str:
        """执行工具"""
        if tool_name not in self.tools:
            return f"❌ 错误: 工具'{tool_name}'不存在"
        
        try:
            func = self.tools[tool_name]["func"]
            # 尝试调用工具
            if not params:
                # 如果没有参数，尝试从函数签名推断
                result = func()
            else:
                result = func(**params)
            return f"✓ 工具结果: {result}"
        except Exception as e:
            return f"❌ 执行错误: {str(e)}"
    
    def run(self, task: str, max_steps: int = 3) -> str:
        """运行Agent"""
        print(f"\n{'='*70}")
        print(f"【 {self.name} 】")
        print(f"【 任务 】{task}")
        print(f"{'='*70}")
        
        self.iteration = 0
        final_result = ""
        
        for step in range(1, max_steps + 1):
            print(f"\n【 第 {step} 步 】")
            
            # 思考
            decision = self.think(task)
            
            # 解析动作
            tool_name, params = self._parse_action(decision)
            
            # 执行
            if tool_name and tool_name in self.tools:
                self.state = AgentState.EXECUTING
                result = self.execute_tool(tool_name, params)
                print(f"\n[执行结果]")
                print(result)
                final_result = result
                
                # 记录
                self.memory.append({
                    "step": step,
                    "task": task,
                    "tool": tool_name,
                    "result": result
                })
                
                # 如果看起来完成了，就停止
                if "✓" in result:
                    print(f"\n✓ 任务在第 {step} 步完成")
                    break
            else:
                print(f"\n[决策]")
                print(decision)
                final_result = decision
                self.memory.append({
                    "step": step,
                    "task": task,
                    "decision": decision,
                    "result": final_result
                })
                break
        
        self.state = AgentState.COMPLETE
        
        print(f"\n{'='*70}")
        print(f"【 任务完成 】")
        print(f"【 最终结果 】\n{final_result}")
        print(f"{'='*70}\n")
        
        return final_result


# 工具函数示例
def add_numbers(a: float = 0, b: float = 0) -> float:
    """加法运算
    
    参数:
        a: 第一个数
        b: 第二个数
    
    返回:
        两数之和
    """
    return a + b


def multiply_numbers(a: float = 1, b: float = 1) -> float:
    """乘法运算
    
    参数:
        a: 第一个数
        b: 第二个数
    
    返回:
        两数之积
    """
    return a * b


def subtract_numbers(a: float = 0, b: float = 0) -> float:
    """减法运算
    
    参数:
        a: 被减数
        b: 减数
    
    返回:
        两数之差
    """
    return a - b


def get_info(topic: str = "") -> str:
    """获取信息
    
    参数:
        topic: 要查询的主题
    
    返回:
        主题的相关信息
    """
    info_db = {
        "Python": "Python是一种高级编程语言，具有简洁易读的语法",
        "Agent": "Agent是自主执行任务的AI系统，能够感知、思考和行动",
        "MCP": "MCP是模型上下文协议，为AI提供标准化接口",
        "RAG": "RAG是检索增强生成，通过检索信息来增强AI生成能力"
    }
    return info_db.get(topic, f"未找到关于'{topic}'的信息")


# 使用示例
if __name__ == "__main__":
    print("\n" + "="*70)
    print("改进版Agent演示 - 使用优质Prompt")
    print("="*70 + "\n")
    
    # 创建Agent
    agent = ImprovedAgent("高级智能助手")
    
    # 注册工具
    agent.register_tool("add", add_numbers, "执行两个数的加法运算")
    agent.register_tool("multiply", multiply_numbers, "执行两个数的乘法运算")
    agent.register_tool("subtract", subtract_numbers, "执行两个数的减法运算")
    agent.register_tool("get_info", get_info, "查询关于某个主题的信息")
    
    # 演示1：简单计算
    print("\n【演示1】简单计算任务")
    agent.run("计算 15 + 8 的结果", max_steps=2)
    
    # 演示2：信息查询
    print("\n【演示2】信息查询任务")
    agent2 = ImprovedAgent("信息查询助手")
    agent2.register_tool("get_info", get_info, "查询关于某个主题的信息")
    agent2.run("告诉我什么是RAG", max_steps=2)
    
    # 演示3：复杂任务
    print("\n【演示3】复杂任务（多步骤）")
    agent3 = ImprovedAgent("复杂任务执行者")
    agent3.register_tool("get_info", get_info, "查询信息")
    agent3.register_tool("add", add_numbers, "加法运算")
    agent3.register_tool("multiply", multiply_numbers, "乘法运算")
    agent3.run("先查询Python是什么，然后计算 2 * 3", max_steps=3)
    
    # 显示Agent记忆
    print("\n" + "="*70)
    print("Agent记忆总结")
    print("="*70)
    print(json.dumps(agent3.memory, indent=2, ensure_ascii=False))

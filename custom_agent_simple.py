# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "mcp>=1.9.1",
# ]
# ///
"""
自定义Agent示例 - 使用状态机模式
这是一个简化的Agent实现，演示核心概念
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


class CustomAgent:
    """简化的自定义Agent实现"""
    
    def __init__(self, name: str):
        self.name = name
        self.state = AgentState.IDLE
        self.tools: Dict[str, Callable] = {}
        self.memory: List[Dict] = []
        self.max_iterations = 10
    
    def register_tool(self, name: str, func: Callable, description: str = ""):
        """注册工具"""
        self.tools[name] = {
            "func": func,
            "description": description or func.__doc__ or ""
        }
        print(f"✓ 已注册工具: {name}")
    
    def _parse_action(self, response: str) -> tuple[str, Dict]:
        """解析Agent的决定"""
        # 简单的解析逻辑
        if "使用" in response:
            parts = response.split("使用")
            if len(parts) > 1:
                tool_name = parts[1].split("(")[0].strip()
                # 提取参数
                if "(" in response and ")" in response:
                    params_str = response.split("(")[1].split(")")[0]
                    # 简单参数解析
                    return tool_name, {"input": params_str}
        return None, {}
    
    def execute_tool(self, tool_name: str, params: Dict) -> str:
        """执行工具"""
        if tool_name not in self.tools:
            return f"错误: 工具'{tool_name}'不存在"
        
        try:
            result = self.tools[tool_name]["func"](**params)
            return str(result)
        except Exception as e:
            return f"执行错误: {str(e)}"
    
    def think(self, task: str) -> str:
        """思考阶段 - 决定要做什么"""
        self.state = AgentState.THINKING
        
        # 可用工具列表
        tools_info = "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])
        
        prompt = f"""
                任务: {task}

                可用工具:
                {tools_info}

                请决定如何完成这个任务。你可以:
                1. 直接回答
                2. 使用工具(格式: 使用 工具名(参数))
                """
        print(f"\n[思考] {self.name}正在思考...")
        print(f"提示: {prompt}")
        
        # 这里在实际应用中会调用LLM
        # 为了演示，我们返回一个简单的决定
        return prompt
    
    def act(self, decision: str) -> str:
        """行动阶段 - 执行决定"""
        self.state = AgentState.EXECUTING
        print(f"\n[执行] {self.name}正在执行...")
        
        tool_name, params = self._parse_action(decision)
        
        if tool_name and tool_name in self.tools:
            result = self.execute_tool(tool_name, params)
            print(f"工具执行结果: {result}")
            return result
        else:
            return decision
    
    def run(self, task: str) -> str:
        """运行Agent"""
        print(f"\n{'='*50}")
        print(f"Agent: {self.name}")
        print(f"任务: {task}")
        print(f"{'='*50}")
        
        # 思考
        decision = self.think(task)
        
        # 行动
        result = self.act(decision)
        
        # 记忆
        self.memory.append({
            "task": task,
            "decision": decision,
            "result": result
        })
        
        self.state = AgentState.COMPLETE
        print(f"\n[完成] Agent执行完毕")
        print(f"最终结果: {result}")
        
        return result


class MultiToolAgent(CustomAgent):
    """支持多工具协作的高级Agent"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.step = 0
    
    def run_with_steps(self, task: str, max_steps: int = 5) -> str:
        """分步骤执行任务"""
        print(f"\n{'='*60}")
        print(f"多步骤Agent: {self.name}")
        print(f"任务: {task}")
        print(f"最大步数: {max_steps}")
        print(f"{'='*60}")
        
        current_task = task
        
        for self.step in range(1, max_steps + 1):
            print(f"\n[步骤 {self.step}/{max_steps}]")
            
            # 思考
            decision = self.think(current_task)
            
            # 行动
            result = self.act(decision)
            
            # 记录
            self.memory.append({
                "step": self.step,
                "task": current_task,
                "result": result
            })
            
            # 判断是否完成
            if "完成" in result or "成功" in result:
                print(f"\n[完成] 任务在第{self.step}步完成")
                break
            
            # 更新任务
            current_task = f"前面的步骤结果: {result}。请继续完成任务: {task}"
        
        return result


# 工具函数示例
def add_numbers(a: float, b: float) -> float:
    """加法运算"""
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """乘法运算"""
    return a * b


def get_info(topic: str) -> str:
    """获取信息"""
    info_db = {
        "Python": "Python是一种高级编程语言",
        "Agent": "Agent是自主执行任务的AI系统",
        "MCP": "MCP是模型上下文协议"
    }
    return info_db.get(topic, f"未找到关于'{topic}'的信息")


# 使用示例
if __name__ == "__main__":
    # 创建基础Agent
    print("=" * 60)
    print("演示1: 基础Agent")
    print("=" * 60)
    
    agent = CustomAgent("基础Agent")
    agent.register_tool("add", add_numbers, "执行加法运算")
    agent.register_tool("multiply", multiply_numbers, "执行乘法运算")
    
    agent.run("计算 5 + 3 的结果")
    
    # 创建多工具Agent
    print("\n" + "=" * 60)
    print("演示2: 多工具Agent")
    print("=" * 60)
    
    multi_agent = MultiToolAgent("多工具Agent")
    multi_agent.register_tool("add", add_numbers, "执行加法运算")
    multi_agent.register_tool("get_info", get_info, "查询信息")
    
    multi_agent.run_with_steps("查询Python的信息，然后进行计算", max_steps=3)
    
    # 显示记忆
    print("\n" + "=" * 60)
    print("Agent记忆回顾")
    print("=" * 60)
    print(json.dumps(multi_agent.memory, indent=2, ensure_ascii=False))

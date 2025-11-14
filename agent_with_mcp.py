# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "mcp>=1.9.1",
# ]
# ///
"""
MCP集成的自定义Agent
展示如何将Agent与MCP服务器结合
"""

from mcp.server.fastmcp import FastMCP
from typing import Any


class AgentWithMCP:
    """支持MCP的Agent"""
    
    def __init__(self, mcp_instance: FastMCP, name: str = "MCPAgent"):
        self.mcp = mcp_instance
        self.name = name
        self.tools = {}
        self.state = "idle"
    
    def register_mcp_tool(self, tool_name: str, description: str):
        """注册MCP工具"""
        self.tools[tool_name] = {
            "type": "mcp",
            "description": description
        }
    
    def plan(self, task: str) -> list:
        """规划任务步骤"""
        print(f"\n[{self.name}] 正在规划: {task}")
        
        # 简单的任务规划逻辑
        steps = []
        if "计算" in task:
            steps.append({"tool": "calculator", "action": "evaluate"})
        if "查询" in task or "搜索" in task:
            steps.append({"tool": "search", "action": "query"})
        if "保存" in task or "存储" in task:
            steps.append({"tool": "storage", "action": "save"})
        
        if not steps:
            steps.append({"tool": "default", "action": "process"})
        
        return steps
    
    def execute(self, tool_name: str, action: str, **kwargs) -> Any:
        """执行工具"""
        print(f"  执行工具: {tool_name}, 动作: {action}")
        return f"执行{tool_name}:{action}的结果"
    
    def run_task(self, task: str) -> str:
        """执行任务"""
        print(f"\n{'='*60}")
        print(f"Agent: {self.name}")
        print(f"任务: {task}")
        print(f"{'='*60}")
        
        # 1. 规划
        steps = self.plan(task)
        print(f"\n规划的步骤: {len(steps)}")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")
        
        # 2. 执行
        print(f"\n开始执行...")
        results = []
        for step in steps:
            result = self.execute(
                tool_name=step.get("tool"),
                action=step.get("action")
            )
            results.append(result)
        
        # 3. 完成
        final_result = "\n".join(results)
        self.state = "complete"
        print(f"\n任务完成!")
        print(f"最终结果: {final_result}")
        
        return final_result


# 创建MCP服务器并添加Agent工具
mcp = FastMCP("agent-mcp-server")


# MCP工具1：计算器
@mcp.tool()
def calculator(expression: str) -> float:
    """计算数学表达式
    
    Args:
        expression: 数学表达式，例如 "2+3*4"
    
    Returns:
        计算结果
    """
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        return f"错误: {str(e)}"


# MCP工具2：搜索
@mcp.tool()
def search(query: str, limit: int = 5) -> str:
    """搜索信息
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量
    
    Returns:
        搜索结果
    """
    results = [
        f"结果{i}: 关于'{query}'的信息"
        for i in range(1, min(limit + 1, 6))
    ]
    return "\n".join(results)


# MCP工具3：数据处理
@mcp.tool()
def process_data(data: str, operation: str = "count") -> str:
    """处理数据
    
    Args:
        data: 输入数据
        operation: 操作类型 (count, length, reverse)
    
    Returns:
        处理结果
    """
    if operation == "count":
        return f"数据元素个数: {len(data)}"
    elif operation == "length":
        return f"数据长度: {len(data)}"
    elif operation == "reverse":
        return f"反转后: {data[::-1]}"
    return f"未知操作: {operation}"


# MCP工具4：保存结果
@mcp.tool()
def save_result(filename: str, content: str) -> str:
    """保存结果到文件
    
    Args:
        filename: 文件名
        content: 内容
    
    Returns:
        保存状态
    """
    return f"已保存到 {filename}: {len(content)} 字符"


# MCP资源：Agent信息
@mcp.resource("agent://info")
def agent_info() -> str:
    """获取Agent信息"""
    return """
    Agent 信息:
    - 名称: MCPAgent
    - 状态: 就绪
    - 可用工具: calculator, search, process_data, save_result
    - 支持的操作: plan, execute, report
    """


@mcp.resource("agent://tools")
def available_tools() -> str:
    """获取可用工具列表"""
    return """
    可用工具:
    1. calculator: 数学计算
    2. search: 信息搜索
    3. process_data: 数据处理
    4. save_result: 保存结果
    """


if __name__ == "__main__":
    # 创建Agent实例
    agent = AgentWithMCP(mcp, "MCPAgent")
    
    # 注册工具
    agent.register_mcp_tool("calculator", "执行数学计算")
    agent.register_mcp_tool("search", "搜索信息")
    agent.register_mcp_tool("process_data", "处理数据")
    agent.register_mcp_tool("save_result", "保存结果")
    
    # 演示1：计算任务
    print("\n【演示1】计算任务")
    agent.run_task("计算 10 + 20 * 2 的结果")
    
    # 演示2：搜索任务
    print("\n【演示2】搜索任务")
    agent.run_task("搜索关于Python的信息")
    
    # 演示3：复合任务
    print("\n【演示3】复合任务")
    agent.run_task("搜索信息并计算")
    
    print("\n" + "="*60)
    print("MCP服务器现在可以被外部客户端（如VS Code）连接")
    print("客户端可以调用已注册的工具和访问资源")
    print("="*60)
    
    # 启动MCP服务器（stdio传输）
    # 取消下面注释以启动真实的MCP服务器
    # mcp.run()

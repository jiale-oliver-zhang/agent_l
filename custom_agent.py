# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "anthropic>=0.21.0",
# ]
# ///
"""
自定义Agent示例 - 使用Claude作为基础模型
"""

import json
from anthropic import Anthropic

class CustomAgent:
    """基础的自定义Agent类"""
    
    def __init__(self, model="claude-3-5-sonnet-20241022"):
        self.client = Anthropic()
        self.model = model
        self.conversation_history = []
        self.tools = []
        
    def register_tool(self, name: str, description: str, func):
        """注册一个工具"""
        self.tools.append({
            "name": name,
            "description": description,
            "func": func
        })
    
    def execute_tool(self, tool_name: str, tool_input: dict):
        """执行指定的工具"""
        for tool in self.tools:
            if tool["name"] == tool_name:
                return tool["func"](**tool_input)
        return None
    
    def chat(self, user_message: str):
        """与Agent进行对话"""
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # 构建工具定义
        tools_def = [{
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        } for tool in self.tools]
        
        # 调用Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            tools=tools_def if tools_def else None,
            messages=self.conversation_history
        )
        
        # 处理响应
        while response.stop_reason == "tool_use":
            # 找到tool_use block
            tool_use_block = None
            for block in response.content:
                if block.type == "tool_use":
                    tool_use_block = block
                    break
            
            if not tool_use_block:
                break
            
            # 执行工具
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input
            tool_result = self.execute_tool(tool_name, tool_input)
            
            # 继续对话
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            self.conversation_history.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": str(tool_result)
                }]
            })
            
            # 再次调用API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=tools_def if tools_def else None,
                messages=self.conversation_history
            )
        
        # 提取最终文本响应
        final_response = ""
        for block in response.content:
            if hasattr(block, 'text'):
                final_response += block.text
        
        # 保存助手响应
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })
        
        return final_response


# 示例工具函数
def calculate(expression: str) -> float:
    """计算数学表达式"""
    try:
        return eval(expression)
    except Exception as e:
        return f"计算错误: {str(e)}"


def get_weather(city: str) -> str:
    """获取天气信息（模拟）"""
    weather_data = {
        "北京": "晴朗，温度25°C",
        "上海": "多云，温度22°C",
        "深圳": "晴朗，温度28°C"
    }
    return weather_data.get(city, "城市未找到")


def web_search(query: str) -> str:
    """网络搜索（模拟）"""
    return f"搜索'{query}'的结果..."


# 使用示例
if __name__ == "__main__":
    # 创建Agent实例
    agent = CustomAgent()
    
    # 注册工具
    agent.register_tool(
        "calculate",
        "用于进行数学计算的工具",
        calculate
    )
    
    agent.register_tool(
        "get_weather",
        "获取指定城市的天气信息",
        get_weather
    )
    
    agent.register_tool(
        "web_search",
        "在网络上搜索信息",
        web_search
    )
    
    # 与Agent交互
    print("=== 自定义Agent演示 ===\n")
    
    # 示例1：计算
    response = agent.chat("请计算 2024 + 1978")
    print(f"用户: 请计算 2024 + 1978")
    print(f"Agent: {response}\n")
    
    # 示例2：多步骤推理
    response = agent.chat("北京的天气如何？")
    print(f"用户: 北京的天气如何？")
    print(f"Agent: {response}\n")

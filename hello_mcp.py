# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "mcp>=1.9.1",
# 
# ]
# ///
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "hello-mcp"
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Return a + b."""
    return a + b

if __name__ == "__main__":
    # stdio 传输（供 VS Code Copilot、Claude Desktop 等 Host 连接）
    mcp.run()

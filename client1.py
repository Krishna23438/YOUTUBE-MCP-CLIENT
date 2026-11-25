import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# Server's configuration  info
SERVERS = {
  "math": {
    "transport":"stdio",
    "command":"/Library/Frameworks/Python.framework/Versions/3.11/bin/uv",
    "args":[
      "run",
      "fastmcp",
      "run",
      "/Users/nitish/Desktopn/mcp-math-server/main.py"
    ]
  }
}

async def main():
  print('')


if __name__ == "__main__":
  asyncio.run(main())
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# Server's configuration  info
SERVERS = {
  "math": {
    "transport":"stdio",
    "command":"\Users\Krishna gupta\AppData\Roaming\Python\Python313\Scripts\uv.exe",
    "args":[
      "run",
      "fastmcp",
      "run",
      "\Users\Krishna gupta\OneDrive\Desktop\MATH-MCP-SERVER\main.py"
    ]
  }
}

async def main():

  client = MultiServerMCPClient(SERVERS)
  tools = await client.get_tools()

  

async def main():
  print('')


if __name__ == "__main__":
  asyncio.run(main())
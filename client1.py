import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# Server's configuration  info
SERVERS = {
  "math": {
    "transport":"stdio",
    "command": "uv",
    "args":[
      "run",
      "fastmcp",
      "run",
       "C:\\Users\\Krishna gupta\\OneDrive\\Desktop\\MATH-MCP-SERVER\\main.py"
    ]
  }
}

async def main():

  client = MultiServerMCPClient(SERVERS)
  tools = await client.get_tools()
  #print(tools)

  named_tool = {}

  for tool in tools:
    named_tool[tool.name] = tool

  print(named_tool)



if __name__ == "__main__":
  asyncio.run(main())
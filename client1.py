import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq

from dotenv import load_dotenv

load_dotenv()



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

  named_tools = {}

  for tool in tools:
    named_tools[tool.name] = tool

  

  llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
   )

  llm_with_tools = llm.bind_tools(tools)

  prompt = "What is the product of 12 and 15 using the math tool ?"
  response = await llm_with_tools.ainvoke(prompt)


  selected_tool = response.tool_calls[0]["name"]
  selected_tool_args = response.tool_calls[0]["args"]

  print(f"Selected tool: {selected_tool}")
  print(f"Selected tool args: {selected_tool_args}")

  tool_result = await named_tools[selected_tool].ainvoke(selected_tool_args)
  print(f"Tool result: {tool_result}")


if __name__ == "__main__":
  asyncio.run(main())
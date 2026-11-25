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

  named_tool = {}

  for tool in tools:
    named_tool[tool.name] = tool

  

  llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
   )

  llm_with_tools = llm.bind_tools(tools)

  prompt = "What is the product of 12 and 15?"
  response = await llm_with_tools.ainvoke(prompt)

  print("Response:",response)



if __name__ == "__main__":
  asyncio.run(main())
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
import json

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

  if not getattr(response, "tool_calls",None):
    print("\n LLM Reply: ", response.content)
    return


  tool_messages = []
  for tc in response.tool_calls:
      selected_tool = tc["name"]
      selected_tool_args = tc["args"]
      selected_tool_id = tc['id']

      print(f"\n-> Executing remote tool: {selected_tool}")
      print("  with args: ", selected_tool_args)

      result = await named_tools[selected_tool].ainvoke(selected_tool_args)
      tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
    
      

  final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
  print(f"final response: {final_response.content}")


if __name__ == "__main__":
  asyncio.run(main())
import os 
import json
import asyncio
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import  HumanMessage,AIMessage,ToolMessage,SystemMessage

# MCP server: local math via uv + fastmcp

SERVERS = {
  "math": {
    "transport":"stdio",
    "command": "uv",
    "args":[
      "run",
      "fastmcp",
      "run",
       r"C:\Users\Krishna gupta\OneDrive\Desktop\MATH-MCP-SERVER\main.py"
    ]
  },
  "expense":{
    "transport": "streamable_http", # if this fails, try "sse"
    "url": "https://krishnagupta.fastmcp.app/mcp"
  },
  "manim-server":{
    "transport":"stdio",
    "command":r"C:\Users\Krishna gupta\AppData\Local\Python\bin\python.exe",
    "args":[
      r"C:\Users\Krishna gupta\AppData\Roaming\Python\Python313\Scripts\manim.exe"
    ],
    "env":{
      "MANIM_EXECUTABLE": r"/Users/Krishna_Gupta/anaconda3/envs/manim2/Scripts/manim.exe"
    }
  }
}

SYSTEM_PROMPT = (
   "You have access to tools. When you choose to call a tool, do not narrate status updates. "
    "After tools run, return only a concise final answer."
)

st.set_page_config(page_title="MCP CHAT", page_icon="🧰",layout="centered")
st.title("🧰 MCP Chat")

load_dotenv()

#One-time init

if "initialized" not in st.session_state:
  # 1) LLM
  st.session_state.llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
   )

  # 2) MCP Tools
  st.session_state.client = MultiServerMCPClient(SERVERS)
  tools = asyncio.run(st.session_state.client.get_tools())
  st.session_state.tools = tools
  st.session_state.tool_by_name = {t.name: t for t in tools}

  # 3) Bind tools
  st.session_state.llm_with_tools = st.session_state.llm.bind_tools(tools)

  # 4) Conversation state
  st.session_state.history = [SystemMessage(content=SYSTEM_PROMPT)]
  st.session_state.initialized = True

# Render Chat historu (skip system + tool messages ; hide intermediate AI with tool_calls)
for msg in  st.session_state.history:
  if isinstance(msg, HumanMessage):
    with st.chat_message('user'):
      st.markdown(msg.content)
  elif isinstance(msg, AIMessage):
    # Skip assistance messages that contain tool_calls(intermediate "fetching...")
    if getattr(msg, "tool_calls", None):
      continue
    with st.chat_message("assistance"):
      st.markdown(msg.content)

  # Tool message and SystemMessage are not rendered as bubbles

# Chat input 
user_text = st.chat_input("Type a message...")
if user_text:
  with st.chat_messagw("user"):
    st.markdown(user_text)
  st.session_state.history.append(HumanMessage(content=user_text))
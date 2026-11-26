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
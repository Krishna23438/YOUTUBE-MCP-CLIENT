import asyncio
from fastmcp import Client

async def main():
    async with Client(
        "https://krishnagupta.fastmcp.app/mcp",
        auth="oauth"
    ) as client:

        await client.ping()

        tools = await client.list_tools()

        print("Connected successfully!")
        print("Available tools:")

        for tool in tools:
            print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())
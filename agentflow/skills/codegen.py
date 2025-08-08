from agentflow.skills import skill
import aiohttp
import asyncio

@skill
async def codegen(query: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": f"Write code for: {query}", "stream": False}
            ) as resp:
                if resp.status != 200:
                    return f"Codegen error: HTTP {resp.status}"
                data = await resp.json()
                return data.get("response", "No code generated")
    except Exception as e:
        return f"Codegen error: {str(e)}"
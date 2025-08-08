import aiohttp
import asyncio

class LLM:
    def __init__(self, provider: str = "ollama"):
        self.provider = provider
    
    async def generate(self, prompt: str) -> str:
        if self.provider != "ollama":
            return "Only Ollama supported in MVP"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llama3", "prompt": prompt, "stream": False}
                ) as resp:
                    if resp.status != 200:
                        return f"LLM error: HTTP {resp.status}"
                    data = await resp.json()
                    return data.get("response", "No response")
        except Exception as e:
            return f"LLM error: {str(e)}"
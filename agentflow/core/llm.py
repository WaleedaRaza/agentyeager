import aiohttp
import asyncio
import json

class LLM:
    def __init__(self, provider: str = "ollama"):
        self.provider = provider
        self.base_url = {
            "ollama": "http://localhost:11434",
            "llama.cpp": "http://localhost:8080",
            "openai": "https://api.openai.com/v1"
        }.get(provider, "none")

    async def generate(self, prompt: str) -> str:
        if self.base_url == "none":
            return "No LLM configured"
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/api/generate"
                json_data = {
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": 100}
                }
                async with session.post(url, json=json_data) as resp:
                    if resp.status == 404:
                        return "LLM server not found or model unavailable."
                    if resp.status != 200:
                        return f"LLM error: HTTP {resp.status}"
                    data = await resp.json()
                    return data.get("response", "").strip()
        except aiohttp.ClientConnectionError:
            return "LLM server unreachable."
        except Exception as e:
            return f"LLM error: {str(e)}"
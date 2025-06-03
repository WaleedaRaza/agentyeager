from agentflow.skills import skill
import aiohttp
from bs4 import BeautifulSoup
import asyncio

@skill
async def web_scrape(query: str) -> str:
    try:
        url = query.strip()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return f"Scrape error: HTTP {resp.status}"
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                return text[:1000]  # Truncate for brevity
    except Exception as e:
        return f"Scrape error: {str(e)}"
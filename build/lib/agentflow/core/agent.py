from typing import List, Optional
import asyncio
from agentflow.skills import Skill
from .llm import LLM

class Agent:
    def __init__(
        self,
        skills: List[Skill],
        llm: str = "ollama",
        name: str = "default_agent"
    ):
        self.name = name
        self.skills = {skill.name: skill for skill in skills}
        self.llm = LLM(provider=llm)
    
    async def run(self, query: str) -> str:
        # For MVP, execute first skill directly (planning added in Iteration 2)
        if not self.skills:
            return "No skills available"
        skill = list(self.skills.values())[0]  # Use first skill
        try:
            result = await skill.execute(query)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
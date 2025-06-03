from typing import List, Optional
import asyncio
from agentflow.skills import Skill
from .llm import LLM
from .planner import Planner  # Correct import

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
        self.planner = Planner(self.llm)
    
    async def run(self, query: str) -> str:
        if not self.skills:
            return "No skills available"
        plan = await self.planner.generate_plan(query, list(self.skills.keys()))
        return await self.planner.execute_plan(self, query, plan)
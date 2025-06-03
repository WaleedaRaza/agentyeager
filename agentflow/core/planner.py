from typing import List, Dict
import asyncio
from agentflow.core.llm import LLM  # Fixed import

class Planner:
    def __init__(self, llm: LLM):
        self.llm = llm

    async def generate_plan(self, query: str, available_skills: List[str]) -> List[str]:
        """Generate a plan based on the query and available skills."""
        prompt = f"Given the query '{query}' and available skills {available_skills}, suggest a sequence of skills to execute."
        try:
            plan = await self.llm.generate(prompt)
            # Parse plan into a list (simplified)
            return [skill.strip() for skill in plan.split(",") if skill.strip() in available_skills]
        except Exception as e:
            return ["local_search"]  # Fallback to a default skill

    async def execute_plan(self, agent: "Agent", query: str, plan: List[str]) -> str:
        """Execute the plan step-by-step."""
        results = []
        for skill_name in plan:
            if skill_name in agent.skills:
                result = await agent.skills[skill_name].execute(query)
                results.append(f"Skill {skill_name}: {result}")
            else:
                results.append(f"Skill {skill_name} not found")
        return "\n".join(results)
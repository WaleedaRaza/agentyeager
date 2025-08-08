import asyncio
from typing import List, Dict
from agentflow.core.agent import Agent
from agentflow.memory import Memory

class Fabric:
    def __init__(self, agents: List[Agent], memory: Memory):
        self.agents = {agent.name: agent for agent in agents}
        self.memory = memory
        self.knowledge_graph = {}  # In-memory graph for agent interactions

    async def initialize(self):
        """Initialize the fabric by loading agent connections."""
        for agent_name in self.agents:
            connections = self.memory.retrieve(f"fabric_connections_{agent_name}")
            if connections:
                self.knowledge_graph[agent_name] = connections.split(",")

    async def run(self, query: str) -> str:
        """Run the fabric, allowing agents to collaborate dynamically."""
        await self.initialize()
        lead_agent = list(self.agents.values())[0]  # Simplified: pick first agent
        result = await lead_agent.run(query)

        # Update knowledge graph with new interactions
        for agent_name in self.agents:
            if agent_name != lead_agent.name:
                self.knowledge_graph.setdefault(lead_agent.name, []).append(agent_name)
                self.memory.store(f"fabric_connections_{lead_agent.name}", ",".join(self.knowledge_graph[lead_agent.name]))

        return result

class Swarm:
    def __init__(self, agents: List[Agent], memory: Memory):
        self.agents = {agent.name: agent for agent in agents}
        self.memory = memory
        self.performance_scores = {name: 1.0 for name in self.agents}

    async def run(self, query: str) -> str:
        """Run a swarm to process the query, optimizing task allocation."""
        for agent_name in self.agents:
            score = self.memory.retrieve(f"swarm_score_{agent_name}")
            if score:
                self.performance_scores[agent_name] = float(score)

        best_agent_name = max(self.performance_scores, key=self.performance_scores.get)
        best_agent = self.agents[best_agent_name]

        start_time = asyncio.get_event_loop().time()
        result = await best_agent.run(query)
        execution_time = asyncio.get_event_loop().time() - start_time

        reward = 1.0 / (execution_time + 1)
        self.performance_scores[best_agent_name] = (
            0.9 * self.performance_scores[best_agent_name] + 0.1 * reward
        )
        self.memory.store(f"swarm_score_{best_agent_name}", str(self.performance_scores[best_agent_name]))

        return result

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent
        self.performance_scores[agent.name] = 1.0
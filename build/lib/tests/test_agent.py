import pytest
import asyncio
from agentflow.core.agent import Agent
from agentflow.skills.local_search import local_search

@pytest.mark.asyncio
async def test_agent_run():
    agent = Agent(skills=[local_search], llm="ollama")
    result = await agent.run("test")
    assert isinstance(result, str)
    assert "files" in result.lower()  # Expect "Found X files" or "No files found"
from agentflow.skills import skill
from agentflow.core.llm import LLM

@skill
async def summarize(content: str) -> str:
    llm = LLM(provider="ollama")
    prompt = f"Summarize the following: {content}"
    try:
        response = await llm.generate(prompt)
        return response.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"
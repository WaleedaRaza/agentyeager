import typer
import yaml
import os
from agentflow.core.agent import Agent
from agentflow.skills import load_skill

app = typer.Typer()

@app.command()
def init():
    """Initialize an AgentFlow project."""
    os.makedirs("agentflow_project", exist_ok=True)
    with open("agentflow_project/requirements.txt", "w") as f:
        f.write("agentflow==1.0.0\n")
    with open("agentflow_project/sample_config.yaml", "w") as f:
        yaml.dump({"name": "sample", "skills": ["local_search"], "llm": "ollama"}, f)
    typer.echo("Initialized project in ./agentflow_project/")

@app.command()
def create_agent(
    name: str = typer.Argument(..., help="Name of the agent"),
    skills: str = typer.Option("", help="Comma-separated skill names"),
    llm: str = typer.Option("ollama", help="LLM provider (ollama, openai, huggingface)")
):
    """Create a new agent."""
    config = {
        "name": name,
        "skills": skills.split(",") if skills else [],
        "llm": llm
    }
    with open(f"{name}_config.yaml", "w") as f:
        yaml.dump(config, f)
    typer.echo(f"Created agent '{name}' with config: {name}_config.yaml")

@app.command()
def run(
    agent_config: str = typer.Argument(..., help="Path to agent config YAML"),
    query: str = typer.Argument(..., help="Query to run")
):
    """Run an agent with a query."""
    if not os.path.exists(agent_config):
        typer.echo(f"Error: Config {agent_config} not found")
        raise typer.Exit(1)
    with open(agent_config, "r") as f:
        config = yaml.safe_load(f)
    
    skills = [load_skill(skill) for skill in config["skills"] if skill]
    agent = Agent(skills=skills, llm=config["llm"], name=config["name"])
    
    result = asyncio.run(agent.run(query))
    typer.echo(result)

if __name__ == "__main__":
    app()
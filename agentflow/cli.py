import typer
import os
import yaml
import asyncio
import multiprocessing
from rich.console import Console
from agentflow.core.agent import Agent
from agentflow.core.swarm import Swarm, Fabric
from agentflow.skills import load_skill
from agentflow.memory import Memory
from agentflow.skills.marketplace import SkillMarketplace
from agentflow.task_aware.watcher import run_watcher
from agentflow.core.llm import LLM

app = typer.Typer()
console = Console()

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_project_dir():
    return os.path.join(get_project_root(), "agentflow_project")

@app.command()
def init():
    """Initialize AgentFlow ecosystem, create user profile, and start watching."""
    project_dir = get_project_dir()
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
        f.write("agentflow==0.1.0\n")
    with open(os.path.join(project_dir, "sample_config.yaml"), "w") as f:
        yaml.dump({"name": "sample", "skills": ["codegen"], "llm": "ollama"}, f)
    console.print(f"[bold green]Initialized project in {project_dir}[/bold green]")

    # Profile creation
    memory = Memory()
    llm = LLM(provider="ollama")
    profile = {}

    # Option 1: Natural language profile creation
    console.print("[bold blue]Building your profile with natural language...[/bold blue]")
    profile["workflow"] = typer.prompt("What’s your primary workflow? (e.g., coding, writing, data analysis)")
    profile["needs"] = typer.prompt("What do you need help with? (e.g., automation, debugging, summarizing)")
    profile["access"] = typer.prompt("Any specific access requirements? (e.g., local-only, specific dirs)")

    # Option 2: Deep search (complementary)
    console.print("[bold blue]Performing a deep search of your environment...[/bold blue]")
    file_types = {}
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            ext = os.path.splitext(file)[1]
            file_types[ext] = file_types.get(ext, 0) + 1
    profile["file_types"] = file_types
    console.print(f"[bold blue]Detected file types: {file_types}[/bold blue]")

    # Enhance profile with LLM reasoning
    prompt = f"Analyze this user profile: {profile}. Suggest workflows and skills."
    try:
        analysis = asyncio.run(llm.generate(prompt))
        console.print(f"[bold blue]Profile Analysis:[/bold blue] {analysis}")
    except Exception as e:
        console.print(f"[bold red]Error analyzing profile: {e}[/bold red]")

    # Store profile
    memory.store_json("user_profile", profile)
    console.print("[bold green]Profile created and saved![/bold green]")

    # Start background watcher
    pid = memory.retrieve("watcher_pid")
    if pid and os.path.exists(f"/proc/{pid}"):
        console.print("[bold yellow]Watcher already running.[/bold yellow]")
    else:
        watcher_process = multiprocessing.Process(target=run_watcher, args=(os.getcwd(), 3600))
        watcher_process.start()
        memory.store("watcher_pid", str(watcher_process.pid))
        console.print(f"[bold green]Started watcher (PID: {watcher_process.pid})[/bold green]")

@app.command()
def list_skills():
    """List available skills."""
    marketplace = SkillMarketplace()
    skills = marketplace.list_skills()
    console.print("[bold blue]Available Skills:[/bold blue]")
    for skill in skills:
        console.print(f"- {skill}")

@app.command()
def deploy(swarm_name: str, task: str = typer.Option(..., "--task")):
    """Deploy a swarm locally with suggested skills."""
    memory = Memory()
    profile = memory.retrieve_json("user_profile") or {}
    console.print(f"[bold blue]Deploying {swarm_name} for task: {task}[/bold blue]")
    swarm = Swarm(name=swarm_name, skills=["codegen"])  # Dynamic skills TBD
    swarm.run(task)
    console.print(f"[bold green]{swarm_name} deployed![/bold green]")

if __name__ == "__main__":
    app()
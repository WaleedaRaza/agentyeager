AgentFlow

A simple, local-first Python framework for building agentic AI with reusable skills.

Why AgentFlow?





Simple: Create agents in 5 lines, no complex chains.



Private: Run locally with Ollama, no cloud needed.



Powerful: Modular skills for any task.

Installation

pip install -r requirements.txt
# Install Ollama: https://ollama.com/
ollama pull llama3

Quick Start

agentflow init
cd agentflow_project
agentflow create-agent my_agent --skills local_search
agentflow run my_agent_config.yaml "Search for AgentFlow"

Contributing

See contributing.md.

License

MIT
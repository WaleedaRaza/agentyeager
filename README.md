# AgentYeager 🚀

**Local-first framework for building LLM-powered agent swarms with enterprise-grade capabilities**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-orange.svg)](https://ollama.ai)
[![Redis](https://img.shields.io/badge/Redis-State%20Management-red.svg)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Async%20API-purple.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-yellow.svg)](https://langchain.com)
[![PyObjC](https://img.shields.io/badge/PyObjC-macOS%20Native-green.svg)](https://pyobjc.readthedocs.io)

## 🎯 Overview

AgentYeager is a cutting-edge, local-first Python framework for building autonomous AI agent swarms with enterprise-grade capabilities. Built with privacy and performance in mind, it enables developers to create sophisticated multi-agent systems that run entirely on local infrastructure using Ollama-powered LLMs.

### ✨ Key Features

- **🔒 100% Local-First**: Complete privacy with no cloud dependencies
- **🤖 Multi-Agent Swarms**: Coordinate autonomous agents with shared state management
- **🧠 Advanced Memory System**: SQLite-backed persistent memory with reflection capabilities
- **🔧 Modular Skill System**: Pluggable skills for any automation task
- **📊 RAG Pipelines**: Local embedding lookup and retrieval-augmented generation
- **🎯 Task Chaining**: Complex workflow orchestration with persistent planning
- **🖥️ Native UI Integration**: macOS native interface via PyObjC
- **🔄 Auto-scaling**: Dynamic agent provisioning based on workload
- **🌐 API Gateway**: RESTful API for external integrations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AgentYeager Architecture                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   Agent Swarm   │    │   Redis State   │    │   SQLite Memory │        │
│  │   Coordinator   │◄──►│   Management    │◄──►│   Persistence   │        │
│  │   (Orchestrator)│    │   (Distributed) │    │   (Encrypted)   │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│           │                       │                       │                │
│           ▼                       ▼                       ▼                │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  Skill Modules  │    │  Ollama LLMs    │    │  FastAPI Server │        │
│  │  (Codegen, Web, │    │  (LLaMA3, etc.) │    │  (Async Tasks)  │        │
│  │   Summarize)    │    └─────────────────┘    └─────────────────┘        │
│  └─────────────────┘                                                       │
│           │                                                               │
│           ▼                                                               │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │   RAG Pipeline  │    │  Task Watcher   │    │  Native UI      │        │
│  │  (Embeddings)   │    │  (Monitoring)   │    │  (PyObjC)       │        │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🔄 Data Flow

1. **Task Input**: User submits task via CLI, API, or UI
2. **Swarm Coordination**: AgentSwarm distributes tasks across agents
3. **Memory Retrieval**: SQLite memory provides context and history
4. **Skill Execution**: Modular skills process task requirements
5. **LLM Processing**: Ollama-powered models generate responses
6. **State Management**: Redis coordinates distributed state
7. **Result Streaming**: Real-time response streaming to user
8. **Memory Persistence**: Results stored in encrypted SQLite

## 🚀 Quick Start

### Prerequisites

```bash
# Install Ollama for local LLM inference
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models
ollama pull llama3:8b
ollama pull llama3:70b  # For advanced reasoning
ollama pull mistral:7b   # For code generation
ollama pull codellama:7b # For programming tasks
```

### Installation

```bash
# Clone the repository
git clone https://github.com/WaleedaRaza/agentyeager.git
cd agentyeager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install Redis for swarm coordination
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server

# Verify installation
agentflow --version
```

### Your First Agent

```bash
# Initialize a new agent project
agentflow init --project-name my_ai_project

# Create an agent with multiple skills
agentflow create-agent research_agent \
  --skills local_search,web_scrape,summarize,codegen \
  --model llama3:8b \
  --memory sqlite \
  --redis-url redis://localhost:6379

# Run a complex task with live streaming
agentflow run research_agent_config.yaml \
  "Analyze today's top NVIDIA news from Reddit, summarize key trends, and generate a Python script to track similar news in the future"
```

## 📋 Core Components

### 🎯 Agent Configuration

AgentYeager uses YAML configuration files to define agent behavior, skills, and system settings. The configuration system supports hierarchical settings, environment-specific overrides, and dynamic skill loading. Each agent can be configured with specific LLM models, memory settings, security policies, and performance parameters.
The memory system provides persistent, encrypted storage with intelligent context retrieval. It supports reflection capabilities that allow agents to learn from past interactions, compression for efficient storage, and automatic backup systems. The memory manager integrates with the RAG pipeline for enhanced context understanding.

### 🔧 Skill Development Framework

The modular skill system allows developers to create custom automation capabilities. Skills can be rate-limited, validated, and versioned. The framework provides decorators for async execution, input validation, and error handling. Skills can be distributed through a marketplace system with automatic updates and dependency management.


### 🤖 Multi-Agent Swarms

AgentYeager's swarm system enables coordinated multi-agent workflows with load balancing, fault tolerance, and auto-scaling capabilities. The swarm coordinator manages task distribution, monitors agent health, and optimizes resource utilization. Agents can communicate through shared state management and coordinate complex workflows.

### 📊 RAG Pipeline Integration

The RAG (Retrieval-Augmented Generation) pipeline provides local embedding capabilities with hybrid retrieval strategies. It supports multiple vector stores, semantic search, and context reranking. The system integrates with the memory manager to provide enhanced context for agent decision-making.

### 🎯 Task-Aware Execution

The task-aware system provides real-time monitoring, intelligent scheduling, and performance optimization. It includes workflow orchestration with dependency management, resource monitoring, and automatic retry mechanisms. The system can optimize task execution based on available resources and agent capabilities.

### 🖥️ Native UI Integration

AgentYeager provides native macOS integration through PyObjC, offering a desktop application experience. The UI includes real-time dashboards, task monitoring, and memory visualization. The system supports both command-line and graphical interfaces for different use cases.

## 🛠️ CLI Commands

### Basic Operations

```bash
# Initialize project
agentflow init --project-name my_project --template advanced

# Create agents
agentflow create-agent research_agent --skills local_search,web_scrape,summarize
agentflow create-agent analyst_agent --skills codegen,local_search --model codellama:7b
agentflow create-agent coordinator_agent --skills marketplace,load --model llama3:70b

# Run tasks
agentflow run research_agent_config.yaml "Search for latest AI developments"
agentflow run analyst_agent_config.yaml "Analyze the search results"
agentflow run coordinator_agent_config.yaml "Coordinate the research workflow"

# Swarm operations
agentflow swarm create research_team --agents research_agent,analyst_agent,coordinator_agent
agentflow swarm run research_team "Conduct comprehensive market research"
agentflow swarm status research_team
agentflow swarm scale research_team --agents 5
```

### Memory Management

```bash
# Memory operations
agentflow memory list
agentflow memory show research_agent
agentflow memory clear research_agent --confirm
agentflow memory export research_agent --format json --output memory_backup.json
agentflow memory import research_agent --file memory_backup.json
agentflow memory optimize research_agent --compress --encrypt
agentflow memory backup research_agent --auto --interval 3600
```

### Skill Management

```bash
# Skill marketplace
agentflow skills list --available
agentflow skills install custom_skill --source github.com/user/custom_skill
agentflow skills update --all
agentflow skills validate custom_skill
agentflow skills test custom_skill --test-suite comprehensive
agentflow skills publish my_skill --version 1.0.0 --description "My custom skill"
```

### System Monitoring

```bash
# System status
agentflow status --detailed
agentflow logs --follow --level debug
agentflow metrics --format json --output metrics.json
agentflow health --check-all
agentflow performance --benchmark --iterations 100

# Resource monitoring
agentflow monitor cpu --threshold 80
agentflow monitor memory --threshold 85
agentflow monitor disk --threshold 90
agentflow monitor network --interface eth0
```

### Advanced Operations

```bash
# Configuration management
agentflow config show --all
agentflow config set redis_url redis://localhost:6379
agentflow config validate
agentflow config backup --auto

# Security operations
agentflow security audit --comprehensive
agentflow security encrypt --database agent_memory.db
agentflow security rotate-keys --auto
agentflow security check-vulnerabilities

# Backup and recovery
agentflow backup create --full --encrypted
agentflow backup restore --from backup_2024_01_15.tar.gz
agentflow backup schedule --daily --time 02:00
```


**⭐ Star this repository if you find it helpful!**

**🔄 Fork and contribute to make it even better!**

**📧 Contact for collaboration opportunities!**

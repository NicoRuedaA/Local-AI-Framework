<!-- prettier-ignore -->
<div align="center">

# SmartAI

**AI-powered multi-agent development orchestration framework**

[![OpenCode AI](https://img.shields.io/badge/OpenCode-AI-blue?style=flat-square)](https://opencode.ai)
[![Python](https://img.shields.io/badge/Python-3.11+-3c873a?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

[Overview](#overview) • [Architecture](#architecture) • [Getting Started](#getting-started) • [Agents](#agents) • [Pipeline](#pipeline)

</div>

---

## Overview

SmartAI is an autonomous software development framework that orchestrates a team of specialized AI agents to transform project ideas into production-ready code. Built on OpenCode AI, it implements a structured multi-agent architecture where each agent handles a specific responsibility — from architectural design to testing and documentation.

> [!TIP]
> SmartAI is ideal for developers who want to automate repetitive coding tasks while maintaining quality through role-based AI collaboration and security-first practices.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Request                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Orquestador (Orchestrator)                                │
│  - Analyzes request                                         │
│  - Coordinates agents                                      │
│  - Validates output quality                                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Planificador  │    │   Memoria     │    │   Guardia     │
│ (Planner)     │    │   (Memory)    │    │   (Security)  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                                         │
        ▼                                         ▼
┌───────────────┐                        ┌───────────────┐
│ Arquitecto    │                        │  Code Review  │
│ (Architect)   │                        └───────────────┘
└───────────────┘                               │
        │                                        ▼
        ▼                               ┌───────────────┐
┌───────────────┐                        │  Testing      │
│ Aparejador    │◄───────────────────────│  Optimization │
│ (Builder)     │                        │  Docs         │
└───────────────┘                        └───────────────┘
        │
        ▼
┌───────────────┐
│  Detective    │
│  (Debugging)  │
└───────────────┘
```

### Multi-Agent Team

| Agent            | Role                                            | Temperature |
| ---------------- | ----------------------------------------------- | ----------- |
| **Orquestador**  | Primary coordinator, delegates work             | 0.2         |
| **Planificador** | Breaks complex tasks into executable steps      | 0.2         |
| **Arquitecto**   | Designs interfaces, class hierarchies, patterns | 0.1         |
| **Aparejador**   | Main code generator                             | 0.2         |
| **Guardia**      | Pre-execution security auditor                  | 0.1         |
| **Detective**    | Bug analysis and root cause identification      | 0.1         |
| **Critico**      | Code reviewer                                   | 0.1         |
| **Optimizador**  | Performance refactoring                         | 0.2         |
| **Escudo**       | Test suite generator                            | 0.2         |
| **Narrador**     | Documentation generator                         | 0.3         |
| **Memoria**      | Project context keeper                          | 0.1         |

### Supported Platforms

- **Backend**: Python 3.11+ with Django 5.x and Django REST Framework
- **Databases**: PostgreSQL (production) / SQLite (development)
- **Game Development**: Unity via MCP (Model Context Protocol)
- **AI Models**: Configurable, supports auto-detection of optimal model

## Features

- **Multi-Agent Orchestration**: 11 specialized agents working in coordinated roles
- **Security-First Approach**: Guardian agent audits all code before execution
- **Structured Pipeline**: 8-stage development process from architecture to documentation
- **Clean Code Standards**: Static typing, explicit error handling, single responsibility
- **Unity Integration**: MCP-based workflow for game development automation
- **Multi-Tenant Ready**: Templates include tenant isolation patterns
- **Comprehensive Testing**: Generates unit, integration, concurrency, and security tests
- **Performance-Aware**: N+1 detection, pagination, and indexing guidance
- **Memory Persistence**: Project context maintained across sessions

## Getting Started

### Prerequisites

- [OpenCode AI](https://opencode.ai)
- Python 3.11+ (for Python projects)
- Unity 2022+ with MCP server (for Unity projects)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/NicoRuedaA/Local-AI-Framework.git
cd Local-AI-Framework
```

2. Configure your `opencode.json`:

```json
{
  "model": "auto",
  "agent": {
    "orquestador": {
      "prompt": "./opencode/agents/orquestador.md",
      "temperature": 0.2
    }
  }
}
```

3. Enable Unity MCP (optional):

```json
{
  "mcp": {
    "unityMCP": {
      "type": "remote",
      "url": "http://localhost:8080/mcp",
      "enabled": true
    }
  }
}
```

## Pipeline

The framework uses an 8-stage development pipeline:

| Stage | Agent                     | Purpose                              |
| ----- | ------------------------- | ------------------------------------ |
| 1     | Planificador + Arquitecto | Architecture design                  |
| 2     | Detective                 | Bug detection and fixing             |
| 3     | Critico                   | Code review (security + performance) |
| 4     | Optimizador               | Performance optimization             |
| 5     | Escudo                    | Test suite generation                |
| 6     | Narrador                  | Technical documentation              |

## Project Structure

```
SmartAI/
├── opencode/
│   ├── opencode.json      # Main configuration
│   ├── agents/            # 11 agent prompt definitions
│   └── skills/            # Specialized skills
│       ├── codigo_limpio  # Clean Code conventions
│       └── unity-mcp      # Unity integration patterns
├── Project/
│   ├── idea_inicial.md    # Project specification template
│   └── rules.md           # Project rules
├── prompts/               # 8-stage pipeline prompts
└── .gitignore
```

## Unity MCP Integration

SmartAI can automate Unity game development through MCP:

- **batch_execute**: Batch operations (10-100x faster than individual calls)
- **editor_selection**: Query current editor context
- **create_script**: Create and modify C# scripts
- **manage_scene**: Scene hierarchy management
- **unityMCP_find_gameobjects**: Find GameObjects

> [!NOTE]
> Unity MCP is disabled by default. Set `"enabled": true` in your `opencode.json` to activate it.

## Skills

### codigo_limpio

Clean Code enforcement rules applied to all generated code:

- Single Responsibility Principle (SRP)
- Static typing where available
- Explicit error handling
- No magic numbers or strings
- Descriptive naming conventions

### unity-mcp

Patterns for Unity Editor integration:

- Batch execution for performance
- Context-first approach
- API validation before writing code
- Domain reload awareness

## Configuration

### Agent Temperature Guidelines

| Task Type              | Recommended Temperature |
| ---------------------- | ----------------------- |
| Code generation        | 0.1 - 0.2               |
| Creative documentation | 0.3                     |
| Structured planning    | 0.15 - 0.2              |

### Permission Model

Each agent has configurable permissions:

```json
{
  "permission": {
    "edit": "allow", // Can modify files
    "bash": "allow" // Can execute commands
  }
}
```

## Documentation

For detailed information about each agent and pipeline stage, see:

- `opencode/agents/` - Individual agent definitions
- `prompts/` - Pipeline stage prompts
- `opencode/skills/` - Specialized skill conventions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Skill-Flow-Orchestrator (SFO)

**Skill-Flow-Orchestrator** is a production-ready meta-skill designed to transform isolated skills into an intelligent, self-coordinating ecosystem. It orchestrates complex workflows by dynamically routing tasks, maintaining context, and learning from execution outcomes.

## 🚀 Key Features

- **🧠 Intelligent Routing**: Matches "Task DNA" to "Skill DNA" using semantic analysis for optimal tool selection.
- **🔗 Flow Composition**: Constructs execution chains as Directed Acyclic Graphs (DAGs) for complex dependencies.
- **💾 Context Management**: Persists state across skill boundaries using a hybrid approach (memory file + in-prompt).
- **📝 Chain Templates**: Saves successful execution patterns as reusable workflow templates.
- **📈 Adaptive Learning**: Optimizes routing weights and decisions based on past execution logs.

## ⚙️ Orchestration Modes

SFO provides four distinct modes tailored to different complexity levels:

| Mode | Duration | Description | Best For |
|------|----------|-------------|----------|
| **QUICK** | 1-2 min | Basic routing, single skill execution. | Simple task delegation. |
| **STANDARD** | 5-10 min | Multi-skill chains with sequential context passing. | Common, multi-step workflows. |
| **DEEP** | 15-30 min | Full DAG composition with potential parallel execution. | Complex processing pipelines. |
| **EXPERT** | Custom | Full control with learning optimization and custom templates. | Production-grade, repetitive workflows. |

## 🛠️ Installation & Setup

1. **Prerequisites**: Ensure you have Python 3.x installed.

2. **Install Dependencies**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **Environment Setup**:
   Copy the example environment file and configure your keys (e.g., specific API keys if needed).
   ```bash
   cp .env.example .env
   ```

## 📖 Usage Guide

### 1. Scan and Index Skills
First, SFO needs to understand available skills. Run the scanner to generate the skill index (`skill_index.json`).

```bash
python3 scripts/scan_skills.py
```

### 2. Match Skills to a Task
To see which skills SFO recommends for a specific request without executing them:

```bash
python3 scripts/match_skills.py "Compare the quarterly financial reports"
```

### 3. Orchestrate a Workflow
To execute a task using the `STANDARD` orchestration mode:

```bash
python3 scripts/orchestrate.py --mode standard "Analyze the user feedback and extract top 3 feature requests"
```

## 📂 Project Structure

- **`scripts/`**: Contains the core Python implementation.
  - `orchestrate.py`: Main entry point for workflow execution.
  - `scan_skills.py`: Tools for indexing available skills.
  - `match_skills.py`: Logic for semantic task-to-skill matching.
- **`references/`**: detailed documentation.
  - `modes.md`: In-depth explanation of orchestration modes.
  - `dag.md`: How DAG composition works.
  - `templates.md`: Guide to using and creating templates.
- **`SKILL.md`**: The Skill Definition file containing metadata and core prompting logic.

## 📚 Documentation

For more detailed information on specific subsystems, check the [references](./references) directory.

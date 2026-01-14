# Antiskills

**Antiskills** is a modular repository of advanced "skills" designed to empower AI agents with specialized capabilities. Each skill is a self-contained unit of functionality—complete with instructions, scripts, and resources—that allows agents to perform complex, multi-step tasks reliably.

## 📦 Available Skills

### 1. [Skill Flow Orchestrator](./skill-flow-orchestrator)
A powerful **Meta-Skill** that acts as the "brain" for your agent's toolkit.
- **Function**: Orchestrates other skills into intelligent, self-correcting workflows.
- **Use Case**: Complex tasks requiring cooperation between multiple tools, context persistence, or adaptive skill routing.
- **Key Features**: Task DNA matching, DAG-based flow composition, and execution templates.

### 2. [Skill Creator](./skill-creator)
The foundational utility for identifying and generating new skills.
- **Function**: Scaffolds new skill directories following the Antiskills Standard.
- **Use Case**: When you want to formalize a new capability for your agent.
- **Key Features**: Interactive creation of `SKILL.md` and directory structures.

## 🔗 Integration with Antikit

This repository is designed to work seamlessly with **[Antikit](https://github.com/vunamhung/antikit)**.

While **Antiskills** provides the specialized capabilities (the "Skills"), **Antikit** serves as the agent framework (the "Brain") that runs them.
- **Antikit**: Manages the agent runtime, LLM connections, and tool execution.
- **Antiskills**: Provides the modular, standardized tools that Antikit agents can load and utilize.

To use them together, ensure your Antikit configuration points to your local or remote `antiskills` library.

## 🏗️ Repository Structure

This repository follows a strict **Skill Definition Standard** to ensure compatibility across different agents and orchestration tools.

```text
antiskills/
├── skill-creator/           # Tool for building new skills
├── skill-flow-orchestrator/ # The orchestration engine
├── .gitignore
└── README.md
```

### The Skill Structure
Every skill in this repository typically contains:
- **`SKILL.md`**: The source of truth. Contains YAML frontmatter and detailed prompt instructions for the agent.
- **`scripts/`**: Python/Node.js scripts providing the actual logic/tools for the skill.
- **`references/`**: (Optional) Documentation or context files.
- **`.env.example`**: (Optional) Environment variables required for the skill.

## 🚀 Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/vunamhung/antiskills.git
   cd antiskills
   ```

2. **Setup Dependencies**
   Most skills run on Python/Node.js. Check individual skill directories for specific `requirements.txt` or `package.json` files.
   
   *Example for Skill Flow Orchestrator:*
   ```bash
   pip install -r skill-flow-orchestrator/scripts/requirements.txt
   ```

3. **Developing a New Skill**
   Use the **Skill Creator** to start a new skill:
   ```bash
   # (Check specific usage in skill-creator/SKILL.md)
   ```

## 🤝 Contribution

1. Create a new branch for your skill.
2. Use `skill-creator` to scaffold the directory.
3. Ensure `SKILL.md` follows the standard format.
4. Submit a Pull Request.

---
*Powered by Agentic Workflows*

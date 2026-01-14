---
name: skill-flow-orchestrator
description: Meta-skill that orchestrates other skills into intelligent, self-coordinating workflows. Use when complex tasks require multiple skills working together, need automated skill routing based on task analysis, want to save and replay successful skill combinations, need state persistence across skill boundaries, or building multi-stage processing pipelines. Provides 4 modes - QUICK (1-2min, single skill), STANDARD (5-10min, multi-skill chains), DEEP (15-30min, DAG composition), EXPERT (custom, learning optimization).
version: 1.0.0
---

# Skill-Flow-Orchestrator (SFO)

Production-ready **Skill Orchestration System** that transforms isolated skills into an intelligent, self-coordinating ecosystem.

## Core Capabilities

1. **Intelligent Routing** - Match task DNA to skill DNA for optimal selection
2. **Flow Composition** - Build skill chains as Directed Acyclic Graphs (DAGs)
3. **Context Management** - Persist state across skill executions (hybrid: memory file + in-prompt)
4. **Chain Templates** - Save successful chains as reusable workflows
5. **Adaptive Learning** - Optimize routing based on execution outcomes

## When to Use

- **Complex tasks**: Require multiple skills working together
- **Automated selection**: Need intelligent skill routing based on task analysis
- **Workflow reuse**: Save and replay successful skill combinations
- **Context continuity**: Need state persistence across skill boundaries
- **Pipeline automation**: Building multi-stage processing workflows

## 4 Orchestration Modes

| Mode | Duration | Features | Best For |
|------|----------|----------|----------|
| QUICK | 1-2 min | Basic routing, single skill | Simple task delegation |
| STANDARD | 5-10 min | Multi-skill chains, context passing | Common workflows |
| DEEP | 15-30 min | Full DAG composition, parallel execution | Complex pipelines |
| EXPERT | Custom | Learning optimization, template management | Production workflows |

## Quick Start

### 1. Scan Available Skills
```bash
python3 .agent/skills/skill-flow-orchestrator/scripts/scan_skills.py
```
Output: `.agent/sfo/skill_index.json` - indexed skills with DNA

### 2. Match Skills to Task
```bash
python3 .agent/skills/skill-flow-orchestrator/scripts/match_skills.py "<task_description>"
```
Returns ranked skills with match scores

### 3. Orchestrate Workflow
```bash
python3 .agent/skills/skill-flow-orchestrator/scripts/orchestrate.py --mode standard "<task>"
```

## Orchestration Workflow

1. **INTAKE** - Parse task, extract requirements
2. **ANALYZE** - Match task DNA with skill DNA using semantic matching
3. **COMPOSE** - Build execution DAG from matched skills
4. **EXECUTE** - Run skills in order, passing context
5. **ADAPT** - Log outcomes, update routing weights

## Context Management

- **Long-term state**: `.agent/sfo/context.json`
- **Chain templates**: `.agent/sfo/templates/`
- **Execution logs**: `.agent/sfo/logs/`

## References

- [Orchestration Modes](references/modes.md) - Detailed mode configurations
- [DAG Composition](references/dag.md) - Building skill chains
- [Template System](references/templates.md) - Saving/loading workflows

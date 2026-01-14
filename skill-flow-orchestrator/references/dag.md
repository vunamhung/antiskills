# DAG Composition

## Overview
Build skill chains as **Directed Acyclic Graphs** for complex workflows.

## DAG Structure

```json
{
  "id": "research-and-implement",
  "nodes": [
    {"id": "n1", "skill": "research", "inputs": ["task"]},
    {"id": "n2", "skill": "planning", "inputs": ["n1.output"]},
    {"id": "n3", "skill": "frontend-dev", "inputs": ["n2.output"]},
    {"id": "n4", "skill": "backend-dev", "inputs": ["n2.output"]},
    {"id": "n5", "skill": "code-review", "inputs": ["n3.output", "n4.output"]}
  ],
  "edges": [
    ["n1", "n2"],
    ["n2", "n3"],
    ["n2", "n4"],
    ["n3", "n5"],
    ["n4", "n5"]
  ]
}
```

## Composition Rules

1. **No cycles** - Each skill executes once
2. **Clear dependencies** - Edges define execution order
3. **Parallel branches** - Independent nodes run simultaneously
4. **Merge points** - Nodes with multiple inputs wait for all

## Building DAGs

### From Task Analysis
```python
def compose_dag(task):
    skills = match_skills(task)
    dependencies = analyze_dependencies(skills)
    return build_dag(skills, dependencies)
```

### Manual Composition
```python
dag = DAG()
dag.add_node("research", skill="research")
dag.add_node("plan", skill="planning", depends=["research"])
dag.add_node("build", skill="frontend-dev", depends=["plan"])
dag.add_edge("research", "plan")
dag.add_edge("plan", "build")
```

## Execution Strategies

### Sequential
```python
for node in dag.topological_sort():
    execute(node)
```

### Parallel
```python
async def execute_parallel(dag):
    ready = dag.get_ready_nodes()
    while ready:
        await asyncio.gather(*[execute(n) for n in ready])
        ready = dag.get_ready_nodes()
```

## Context Flow

Each node receives:
```json
{
  "task": "original task",
  "inputs": {
    "n1.output": "...",
    "n2.output": "..."
  },
  "global_context": {}
}
```

## Validation

Before execution:
```python
dag.validate()  # Checks for cycles, missing deps, invalid skills
```

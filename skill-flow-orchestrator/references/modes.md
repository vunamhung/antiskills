# Orchestration Modes

## QUICK Mode (1-2 min)
**Best for**: Simple task delegation, single-skill tasks

```python
# Single skill selection based on highest match score
skills = match_skills(task)
execute(skills[0])
```

**Features**:
- Basic keyword + semantic matching
- No context persistence
- Direct skill execution

## STANDARD Mode (5-10 min)
**Best for**: Common workflows, multi-step tasks

```python
# Multi-skill chains with context passing
chain = compose_chain(task, max_skills=3)
context = {}
for skill in chain:
    context = execute(skill, context)
```

**Features**:
- Multi-skill chain composition
- In-prompt context passing
- Sequential execution

## DEEP Mode (15-30 min)
**Best for**: Complex pipelines, parallel processing

```python
# Full DAG composition with parallel execution
dag = compose_dag(task)
context = execute_dag(dag, parallel=True)
save_template(dag) if successful
```

**Features**:
- Directed Acyclic Graph composition
- Parallel skill execution
- Automatic template saving
- Memory file context

## EXPERT Mode (Custom)
**Best for**: Production workflows, optimization

```python
# Learning optimization + template management
template = load_template(task_pattern)
if template:
    execute_template(template)
else:
    dag = compose_dag(task, optimize=True)
    execute_dag(dag)
    update_routing_weights(outcomes)
```

**Features**:
- Template-first execution
- Routing weight optimization
- Execution analytics
- Custom timeouts

## Mode Selection Logic

```python
def select_mode(task):
    complexity = analyze_complexity(task)
    if complexity.skills_needed == 1:
        return "QUICK"
    elif complexity.skills_needed <= 3 and not complexity.parallel:
        return "STANDARD"
    elif complexity.parallel or complexity.skills_needed > 3:
        return "DEEP"
    elif task.production or task.optimize:
        return "EXPERT"
```

## Configuration

Set default mode in `.agent/sfo/config.json`:
```json
{
  "default_mode": "STANDARD",
  "timeouts": {
    "QUICK": 120,
    "STANDARD": 600,
    "DEEP": 1800,
    "EXPERT": null
  }
}
```

# Template System

## Overview
Save successful skill chains as reusable workflow templates.

## Template Structure

```json
{
  "name": "fullstack-feature",
  "description": "Full-stack feature implementation",
  "trigger_patterns": ["implement feature", "build feature", "create feature"],
  "dag": { ... },
  "variables": ["feature_name", "tech_stack"],
  "success_rate": 0.92,
  "avg_duration": 1800,
  "usage_count": 15
}
```

## Saving Templates

### Auto-save on Success
```python
if execution.success and execution.dag.nodes > 2:
    template = create_template(execution.dag, task)
    save_template(template)
```

### Manual Save
```python
template = Template(
    name="my-workflow",
    dag=current_dag,
    trigger_patterns=["when to use this"]
)
template.save()
```

## Loading Templates

### Pattern Matching
```python
def find_template(task):
    templates = load_all_templates()
    for t in templates:
        if matches_pattern(task, t.trigger_patterns):
            return t
    return None
```

### Template Execution
```python
template = find_template(task)
if template:
    dag = template.instantiate(variables={
        "feature_name": extract_feature_name(task)
    })
    execute_dag(dag)
```

## Template Storage

Location: `.agent/sfo/templates/`

```
templates/
├── fullstack-feature.json
├── api-development.json
├── ui-implementation.json
└── debug-and-fix.json
```

## Template Variables

Define placeholders in DAG:
```json
{
  "nodes": [
    {"skill": "frontend-dev", "config": {"component": "${component_name}"}}
  ]
}
```

Instantiate with values:
```python
dag = template.instantiate(component_name="LoginForm")
```

## Analytics

Track and optimize:
```python
template.record_execution(success=True, duration=1200)
templates = sorted(templates, key=lambda t: t.success_rate, reverse=True)
```

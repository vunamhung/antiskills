#!/usr/bin/env python3
"""
Main orchestration script for SFO.
Runs skill workflows based on mode and task.
"""

import os
import json
import argparse
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict

# Import local modules
from match_skills import match_skills


@dataclass
class ExecutionContext:
    """Context passed between skills."""
    task: str
    mode: str
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    current_step: int = 0
    total_steps: int = 0
    outputs: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ExecutionContext':
        return cls(**data)


@dataclass
class DAGNode:
    """Node in execution DAG."""
    id: str
    skill: str
    depends: list[str] = field(default_factory=list)
    completed: bool = False
    output: Optional[str] = None


class Orchestrator:
    """Main orchestrator class."""
    
    def __init__(self, mode: str = "STANDARD"):
        self.mode = mode.upper()
        self.sfo_dir = self._get_sfo_dir()
        self.context: Optional[ExecutionContext] = None
        self.dag: list[DAGNode] = []
        
    def _get_sfo_dir(self) -> Path:
        """Get SFO directory path."""
        script_dir = Path(__file__).parent
        return script_dir.parent.parent.parent / "sfo"
    
    def _load_context(self) -> Optional[ExecutionContext]:
        """Load context from file."""
        context_file = self.sfo_dir / "context.json"
        if context_file.exists():
            with open(context_file, 'r') as f:
                return ExecutionContext.from_dict(json.load(f))
        return None
    
    def _save_context(self):
        """Save context to file."""
        if self.context:
            self.sfo_dir.mkdir(parents=True, exist_ok=True)
            context_file = self.sfo_dir / "context.json"
            with open(context_file, 'w') as f:
                json.dump(self.context.to_dict(), f, indent=2)
    
    def _log_execution(self, message: str):
        """Log execution step."""
        logs_dir = self.sfo_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        timestamp = datetime.now().isoformat()
        
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] [{self.mode}] {message}\n")
    
    def compose_dag(self, skills: list[dict]) -> list[DAGNode]:
        """Compose execution DAG from matched skills."""
        dag = []
        prev_id = None
        
        for i, skill in enumerate(skills):
            node = DAGNode(
                id=f"n{i}",
                skill=skill['name'],
                depends=[prev_id] if prev_id else []
            )
            dag.append(node)
            prev_id = node.id
        
        return dag
    
    def execute_skill(self, node: DAGNode, context: ExecutionContext) -> str:
        """Execute a single skill."""
        print(f"   ▶ Executing skill: {node.skill}")
        self._log_execution(f"Executing skill: {node.skill}")
        
        # In practice, this triggers skill loading via SKILL.md
        # For now, return placeholder
        output = f"Skill '{node.skill}' executed successfully"
        node.completed = True
        node.output = output
        
        context.outputs[node.id] = output
        context.current_step += 1
        self._save_context()
        
        return output
    
    def run_quick(self, task: str):
        """QUICK mode: Single skill selection."""
        print("\n🚀 Running QUICK mode (1-2 min)")
        
        skills = match_skills(task, use_ai=True)
        if not skills:
            print("❌ No matching skills found")
            return
        
        top_skill = skills[0]
        print(f"\n📌 Selected skill: {top_skill['name']}")
        print(f"   Score: {top_skill.get('final_score', 0):.2f}")
        
        node = DAGNode(id="n0", skill=top_skill['name'])
        self.execute_skill(node, self.context)
        
        print(f"\n✅ Completed in QUICK mode")
    
    def run_standard(self, task: str):
        """STANDARD mode: Multi-skill chain."""
        print("\n🚀 Running STANDARD mode (5-10 min)")
        
        skills = match_skills(task, use_ai=True)[:3]
        if not skills:
            print("❌ No matching skills found")
            return
        
        self.dag = self.compose_dag(skills)
        self.context.total_steps = len(self.dag)
        
        print(f"\n📋 Execution chain ({len(self.dag)} skills):")
        for node in self.dag:
            print(f"   → {node.skill}")
        
        print("\n🔄 Executing chain:")
        for node in self.dag:
            self.execute_skill(node, self.context)
        
        print(f"\n✅ Completed chain with {len(self.dag)} skills")
    
    def run_deep(self, task: str):
        """DEEP mode: Full DAG composition."""
        print("\n🚀 Running DEEP mode (15-30 min)")
        
        skills = match_skills(task, use_ai=True)[:5]
        if not skills:
            print("❌ No matching skills found")
            return
        
        self.dag = self.compose_dag(skills)
        self.context.total_steps = len(self.dag)
        
        print(f"\n📋 Execution DAG ({len(self.dag)} nodes):")
        for node in self.dag:
            deps = f" [depends: {', '.join(node.depends)}]" if node.depends else ""
            print(f"   {node.id}: {node.skill}{deps}")
        
        print("\n🔄 Executing DAG:")
        for node in self.dag:
            self.execute_skill(node, self.context)
        
        # Auto-save template on success
        self._save_template(task)
        print(f"\n✅ Completed DAG and saved template")
    
    def run_expert(self, task: str):
        """EXPERT mode: Template-first with optimization."""
        print("\n🚀 Running EXPERT mode (custom)")
        
        # Try to load existing template
        template = self._find_template(task)
        
        if template:
            print(f"\n📄 Found template: {template['name']}")
            self._execute_template(template)
        else:
            print("\n📝 No template found, running DEEP mode")
            self.run_deep(task)
    
    def _find_template(self, task: str) -> Optional[dict]:
        """Find matching template for task."""
        templates_dir = self.sfo_dir / "templates"
        if not templates_dir.exists():
            return None
        
        for tpl_file in templates_dir.glob("*.json"):
            with open(tpl_file, 'r') as f:
                tpl = json.load(f)
                patterns = tpl.get('trigger_patterns', [])
                for pattern in patterns:
                    if pattern.lower() in task.lower():
                        return tpl
        return None
    
    def _execute_template(self, template: dict):
        """Execute a saved template."""
        print(f"   Executing template: {template['name']}")
        # Template execution logic
        self._log_execution(f"Executed template: {template['name']}")
    
    def _save_template(self, task: str):
        """Save current DAG as template."""
        templates_dir = self.sfo_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        template = {
            "name": f"auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "description": task[:100],
            "trigger_patterns": [task[:50]],
            "dag": [asdict(n) for n in self.dag],
            "created_at": datetime.now().isoformat()
        }
        
        tpl_file = templates_dir / f"{template['name']}.json"
        with open(tpl_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        self._log_execution(f"Saved template: {template['name']}")
    
    def run(self, task: str):
        """Main entry point."""
        self.context = ExecutionContext(task=task, mode=self.mode)
        self._save_context()
        self._log_execution(f"Started orchestration: {task[:50]}")
        
        print(f"🎯 Task: {task}")
        print(f"⚙️  Mode: {self.mode}")
        
        if self.mode == "QUICK":
            self.run_quick(task)
        elif self.mode == "STANDARD":
            self.run_standard(task)
        elif self.mode == "DEEP":
            self.run_deep(task)
        elif self.mode == "EXPERT":
            self.run_expert(task)
        else:
            print(f"❌ Unknown mode: {self.mode}")
            return
        
        self._log_execution(f"Completed orchestration")


def main():
    parser = argparse.ArgumentParser(description='SFO Orchestrator')
    parser.add_argument('task', help='Task to orchestrate')
    parser.add_argument('--mode', '-m', default='STANDARD',
                       choices=['QUICK', 'STANDARD', 'DEEP', 'EXPERT'],
                       help='Orchestration mode')
    
    args = parser.parse_args()
    
    orchestrator = Orchestrator(mode=args.mode)
    orchestrator.run(args.task)


if __name__ == "__main__":
    main()

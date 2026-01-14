#!/usr/bin/env python3
"""
Scan all skills and build skill index with DNA.
Output: .agent/sfo/skill_index.json
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, List


def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}


def extract_skill_dna(skill_path: Path) -> Optional[dict]:
    """Extract skill DNA from SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding='utf-8')
    frontmatter = parse_yaml_frontmatter(content)

    if not frontmatter.get('name') or not frontmatter.get('description'):
        return None

    # Extract keywords from description
    description = frontmatter.get('description', '')
    keywords = extract_keywords(description)

    # Check for scripts
    scripts_dir = skill_path / "scripts"
    scripts = []
    if scripts_dir.exists():
        scripts = [f.name for f in scripts_dir.iterdir() if f.is_file()]

    # Check for references
    refs_dir = skill_path / "references"
    references = []
    if refs_dir.exists():
        references = [f.name for f in refs_dir.iterdir() if f.is_file()]

    return {
        "name": frontmatter.get('name'),
        "description": description,
        "keywords": keywords,
        "scripts": scripts,
        "references": references,
        "path": str(skill_path),
        "version": frontmatter.get('version', '1.0.0')
    }


def extract_keywords(text: str) -> List[str]:
    """Extract keywords from description text."""
    keywords = set()
    text_lower = text.lower()

    # Action words
    action_patterns = [
        r'\b(build|create|generate|implement|develop|design)\b',
        r'\b(analyze|debug|test|validate|review|optimize)\b',
        r'\b(deploy|configure|setup|install|manage)\b',
        r'\b(process|transform|convert|parse|extract)\b',
        r'\b(search|query|fetch|retrieve|discover)\b',
        r'\b(authenticate|authorize|login|auth|oauth|jwt|session)\b',
        r'\b(payment|checkout|stripe|billing|subscription)\b',
        r'\b(database|db|sql|nosql|schema|migration)\b',
        r'\b(frontend|backend|fullstack|full-stack|api)\b',
        r'\b(mobile|ios|android|native|app)\b',
        r'\b(cloud|serverless|docker|kubernetes|k8s)\b',
        r'\b(ui|ux|design|styling|component|layout)\b',
        r'\b(image|video|audio|media|file)\b',
        r'\b(chart|graph|visualization|dashboard)\b',
        r'\b(e-commerce|ecommerce|shop|store|cart)\b',
    ]

    for pattern in action_patterns:
        matches = re.findall(pattern, text_lower)
        keywords.update(matches)

    # Technology names (case insensitive)
    tech_patterns = [
        r'\b(react|next\.?js|vue|angular|svelte|remix)\b',
        r'\b(node\.?js|python|typescript|javascript|go|rust)\b',
        r'\b(mongodb|postgresql|postgres|redis|mysql|sqlite)\b',
        r'\b(docker|kubernetes|aws|gcp|azure|cloudflare)\b',
        r'\b(api|rest|graphql|grpc|websocket)\b',
        r'\b(css|html|tailwind|sass|scss)\b',
        r'\b(express|fastapi|nestjs|django|flask)\b',
        r'\b(stripe|paypal|sepay|polar)\b',
        r'\b(gemini|openai|anthropic|claude|gpt)\b',
        r'\b(mcp|mern|jamstack)\b',
        r'\b(three\.?js|webgl|canvas|svg)\b',
        r'\b(shopify|woocommerce|magento)\b',
    ]

    for pattern in tech_patterns:
        matches = re.findall(pattern, text_lower)
        keywords.update(matches)

    # Extract significant words (4+ chars, not common words)
    stop_words = {'this', 'that', 'with', 'from', 'have', 'been', 'will', 'would',
                  'could', 'should', 'when', 'where', 'what', 'which', 'their',
                  'there', 'these', 'those', 'your', 'about', 'into', 'over',
                  'such', 'only', 'other', 'some', 'than', 'then', 'them', 'well',
                  'also', 'back', 'after', 'most', 'made', 'being', 'through',
                  'using', 'used', 'uses', 'need', 'needs', 'like', 'make', 'just'}

    words = re.findall(r'\b([a-z][a-z0-9-]{3,})\b', text_lower)
    for word in words:
        if word not in stop_words and not word.startswith('http'):
            keywords.add(word)

    return list(keywords)


def scan_skills(skills_dir: Path) -> List[dict]:
    """Scan all skills in directory."""
    skills = []

    for item in skills_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith('.') or item.name == 'common':
            continue

        dna = extract_skill_dna(item)
        if dna:
            skills.append(dna)

    return skills


def main():
    # Determine paths
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    skills_root = skill_dir.parent
    sfo_dir = skills_root.parent / "sfo"

    # Create output directory
    sfo_dir.mkdir(parents=True, exist_ok=True)

    # Scan skills
    print(f"📂 Scanning skills in: {skills_root}")
    skills = scan_skills(skills_root)

    # Build index
    index = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "skills_count": len(skills),
        "skills": skills
    }

    # Save index
    output_file = sfo_dir / "skill_index.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"✅ Indexed {len(skills)} skills")
    print(f"📄 Output: {output_file}")

    # Print summary
    print("\n📋 Skills found:")
    for skill in skills:
        print(f"   - {skill['name']}: {len(skill['keywords'])} keywords")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Match skills to task using YAML descriptions + AI semantic matching.
Uses Google Gemini API for semantic understanding.
"""

import os
import re
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_paths = [
    Path(__file__).parent / '.env',
    Path(__file__).parent.parent / '.env',
    Path(__file__).parent.parent.parent / '.env',
    Path(__file__).parent.parent.parent.parent / '.env'
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break


def load_skill_index() -> dict:
    """Load skill index from JSON."""
    script_dir = Path(__file__).parent
    sfo_dir = script_dir.parent.parent.parent / "sfo"
    index_file = sfo_dir / "skill_index.json"
    
    if not index_file.exists():
        print("❌ Skill index not found. Run scan_skills.py first.")
        return {"skills": []}
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def keyword_match(task: str, skill: dict) -> float:
    """Calculate keyword match score with weighted relevance."""
    task_lower = task.lower()
    task_words = set(re.findall(r'\b[a-z][a-z0-9-]{2,}\b', task_lower))
    keywords = set(skill.get('keywords', []))
    skill_name = skill.get('name', '').lower().replace('-', ' ')
    description = skill.get('description', '').lower()
    
    if not keywords and not skill_name:
        return 0.0
    
    score = 0.0
    
    # 1. Skill name matching (high weight)
    name_words = set(skill_name.split())
    name_matches = len(task_words & name_words)
    if name_matches > 0:
        score += 0.4 * (name_matches / len(name_words))
    
    # 2. Keyword overlap (medium weight)
    keyword_matches = len(task_words & keywords)
    if keywords:
        score += 0.35 * (keyword_matches / min(len(keywords), 20))
    
    # 3. Task words in description (low weight for semantic relevance)
    desc_matches = sum(1 for w in task_words if w in description)
    if task_words:
        score += 0.25 * min(desc_matches / len(task_words), 1.0)
    
    return min(score, 1.0)


def semantic_match_gemini(task: str, skills: list[dict]) -> list[dict]:
    """Use Gemini API for semantic matching."""
    try:
        from google import genai
    except ImportError:
        print("⚠️ google-genai not installed. Using keyword matching only.")
        return []
    
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("⚠️ GEMINI_API_KEY not set. Using keyword matching only.")
        return []
    
    client = genai.Client(api_key=api_key)
    
    # Build skill descriptions for matching
    skill_list = "\n".join([
        f"- {s['name']}: {s['description'][:200]}"
        for s in skills[:20]  # Limit to top 20 for token efficiency
    ])
    
    prompt = f"""Given this task: "{task}"

And these available skills:
{skill_list}

Return a JSON array of the top 5 most relevant skills for this task, ranked by relevance.
Format: [{{"name": "skill-name", "score": 0.95, "reason": "why relevant"}}]

Only return valid JSON, no markdown or explanation."""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        # Parse response
        text = response.text.strip()
        # Remove markdown code blocks if present
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        
        return json.loads(text)
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        return []


def match_skills(task: str, use_ai: bool = True) -> list[dict]:
    """Match skills to task using hybrid approach."""
    index = load_skill_index()
    skills = index.get('skills', [])
    
    if not skills:
        return []
    
    # Step 1: Keyword matching for initial ranking
    for skill in skills:
        skill['keyword_score'] = keyword_match(task, skill)
    
    # Sort by keyword score
    skills_sorted = sorted(skills, key=lambda s: s['keyword_score'], reverse=True)
    
    # Step 2: AI semantic matching for refinement
    if use_ai:
        ai_results = semantic_match_gemini(task, skills_sorted)
        
        if ai_results:
            # Merge AI scores with keyword scores
            ai_scores = {r['name']: r for r in ai_results}
            
            for skill in skills_sorted:
                if skill['name'] in ai_scores:
                    ai_data = ai_scores[skill['name']]
                    skill['ai_score'] = ai_data.get('score', 0)
                    skill['reason'] = ai_data.get('reason', '')
                    # Combined score: 40% keyword + 60% AI
                    skill['final_score'] = (
                        0.4 * skill['keyword_score'] + 
                        0.6 * skill['ai_score']
                    )
                else:
                    skill['ai_score'] = 0
                    skill['final_score'] = skill['keyword_score'] * 0.4
    else:
        for skill in skills_sorted:
            skill['final_score'] = skill['keyword_score']
    
    # Final sort by combined score
    return sorted(skills_sorted, key=lambda s: s.get('final_score', 0), reverse=True)


def main():
    parser = argparse.ArgumentParser(description='Match skills to task')
    parser.add_argument('task', help='Task description')
    parser.add_argument('--no-ai', action='store_true', help='Skip AI matching')
    parser.add_argument('--top', type=int, default=5, help='Number of results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    print(f"🔍 Matching skills for: {args.task}\n")
    
    results = match_skills(args.task, use_ai=not args.no_ai)
    top_results = results[:args.top]
    
    if args.json:
        output = [{
            "name": r['name'],
            "score": r.get('final_score', 0),
            "reason": r.get('reason', ''),
            "keywords": r.get('keywords', [])
        } for r in top_results]
        print(json.dumps(output, indent=2))
    else:
        print(f"📋 Top {args.top} matching skills:\n")
        for i, skill in enumerate(top_results, 1):
            score = skill.get('final_score', 0)
            reason = skill.get('reason', 'Keyword match')
            print(f"{i}. {skill['name']} (score: {score:.2f})")
            print(f"   {reason}")
            print()


if __name__ == "__main__":
    main()

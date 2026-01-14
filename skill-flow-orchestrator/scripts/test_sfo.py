#!/usr/bin/env python3
"""
Tests for SFO scripts.
"""

import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scan_skills import (
    parse_yaml_frontmatter,
    extract_keywords,
    extract_skill_dna
)
from match_skills import keyword_match, match_skills


class TestYAMLParsing:
    """Test YAML frontmatter parsing."""
    
    def test_valid_frontmatter(self):
        content = """---
name: test-skill
description: This is a test skill
version: 1.0.0
---

# Content here
"""
        result = parse_yaml_frontmatter(content)
        assert result['name'] == 'test-skill'
        assert result['description'] == 'This is a test skill'
        assert result['version'] == '1.0.0'
    
    def test_missing_frontmatter(self):
        content = "# Just markdown content"
        result = parse_yaml_frontmatter(content)
        assert result == {}
    
    def test_invalid_yaml(self):
        content = """---
name: [invalid: yaml: syntax
---
"""
        result = parse_yaml_frontmatter(content)
        assert result == {}


class TestKeywordExtraction:
    """Test keyword extraction from descriptions."""
    
    def test_action_keywords(self):
        text = "Build and deploy React applications with testing and validate results"
        keywords = extract_keywords(text)
        assert 'build' in keywords
        assert 'deploy' in keywords
        assert 'validate' in keywords
    
    def test_technology_keywords(self):
        text = "Use React and Node.js with MongoDB database"
        keywords = extract_keywords(text)
        assert 'react' in keywords
        assert 'node.js' in keywords
        assert 'mongodb' in keywords
    
    def test_empty_text(self):
        keywords = extract_keywords("")
        assert keywords == []


class TestKeywordMatch:
    """Test keyword matching logic."""
    
    def test_full_match(self):
        skill = {
            'name': 'react-deploy',
            'keywords': ['react', 'build', 'deploy'],
            'description': 'Build and deploy React apps'
        }
        task = "build and deploy a react app"
        score = keyword_match(task, skill)
        assert score > 0.5  # Should have high score with name + keyword matches
    
    def test_partial_match(self):
        skill = {
            'name': 'frontend-frameworks',
            'keywords': ['react', 'vue', 'angular'],
            'description': 'Frontend frameworks'
        }
        task = "build a react application"
        score = keyword_match(task, skill)
        assert 0 < score < 1
    
    def test_no_match(self):
        skill = {
            'name': 'backend-python',
            'keywords': ['python', 'django'],
            'description': 'Python backend development'
        }
        task = "build a rust cli tool"
        score = keyword_match(task, skill)
        assert score < 0.1  # Very low score for no matches
    
    def test_empty_keywords(self):
        skill = {'name': '', 'keywords': [], 'description': ''}
        task = "any task"
        score = keyword_match(task, skill)
        assert score == 0.0


class TestSkillDNAExtraction:
    """Test skill DNA extraction from SKILL.md files."""
    
    def test_extract_valid_skill(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "test-skill"
            skill_dir.mkdir()
            
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: test-skill
description: A skill to build and create React applications
version: 1.0.0
---

# Test Skill
""")
            
            # Create scripts directory
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "helper.py").touch()
            
            dna = extract_skill_dna(skill_dir)
            
            assert dna is not None
            assert dna['name'] == 'test-skill'
            assert 'build' in dna['keywords'] or 'create' in dna['keywords'] or 'react' in dna['keywords']
            assert 'helper.py' in dna['scripts']
    
    def test_missing_skill_md(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "empty-skill"
            skill_dir.mkdir()
            
            dna = extract_skill_dna(skill_dir)
            assert dna is None


def run_tests():
    """Run all tests."""
    import traceback
    
    test_classes = [
        TestYAMLParsing,
        TestKeywordExtraction,
        TestKeywordMatch,
        TestSkillDNAExtraction
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        print(f"\n📋 {test_class.__name__}")
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    getattr(instance, method_name)()
                    print(f"   ✅ {method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"   ❌ {method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"   ❌ {method_name}: {e}")
                    traceback.print_exc()
                    failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

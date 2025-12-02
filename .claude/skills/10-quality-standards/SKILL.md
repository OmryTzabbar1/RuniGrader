---
name: 10-quality-standards
description: Evaluates linting, CI/CD, code quality tools, and style guides. Use for Tier 2 quality standards assessment.
version: 2.0.0
---

# Skill 10: Quality Standards

You are an autonomous agent that evaluates code quality tools and practices.

**Your Mission:** Find and assess linting configs, CI/CD pipelines, code quality tools, and style guides.

**Scoring:** 10 points maximum
- Linting Configuration: 3 points
- CI/CD Pipeline: 3 points
- Code Style Guide: 2 points
- Pre-commit Hooks: 2 points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery

1. **Run helper script:**
```bash
python .claude/skills/10-quality-standards/find_quality_tools.py <repo_path>
```

2. **Manual search:**
```bash
# Find linting configs
find . -name ".pylintrc" -o -name ".eslintrc*" -o -name ".flake8" -o -name "pyproject.toml"

# Find CI/CD
find . -path "*/.github/workflows/*.yml" | head -10
find . -name ".gitlab-ci.yml" -o -name ".travis.yml"

# Find style guides
find . -name "CONTRIBUTING.md" -o -name "*style*.md"

# Find pre-commit hooks
find . -name ".pre-commit-config.yaml"
```

### Phase 2: Linting Configuration (3 points)

**Scoring:**
- Has linting config for project languages: 3.0 points
- Basic linting: 1.5 points
- No linting: 0 points

### Phase 3: CI/CD Pipeline (3 points)

**Scoring:**
- Has CI/CD with quality checks: 3.0 points
- Has CI/CD but minimal checks: 1.5 points
- No CI/CD: 0 points

### Phase 4: Code Style Guide (2 points)

**Scoring:**
- Has CONTRIBUTING.md or style guide: 2.0 points
- Basic style notes: 1.0 point
- No style guide: 0 points

### Phase 5: Pre-commit Hooks (2 points)

**Scoring:**
- Has .pre-commit-config.yaml: 2.0 points
- No pre-commit hooks: 0 points

---

## Important: Be Thorough!

❌ **DON'T** only check root for linting configs
✅ **DO** check subdirectories and standard config locations

❌ **DON'T** assume no CI means no quality tools
✅ **DO** check for local quality scripts

**Success = Finding all quality tools that exist!**

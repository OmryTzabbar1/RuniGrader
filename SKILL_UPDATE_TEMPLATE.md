# Skill Update Template for Skills 4-10

All helper scripts have been created. Each SKILL.md file needs to follow this structure:

---

## Common Structure for All Skills

```markdown
---
name: <skill-name>
description: <What it evaluates>. Use for Tier 2 <skill-name> assessment.
version: 2.0.0
---

# Skill X: <Title>

You are an autonomous agent that thoroughly evaluates <topic>.

**Your Mission:** Find and assess <artifacts>, no matter where they're located in the repository.

**Scoring:** 10 points maximum
- <Component 1>: X points
- <Component 2>: Y points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery (Find ALL <artifacts>)

**DO NOT assume standard locations!**

1. **Run the helper script first:**
```bash
python .claude/skills/<skill-dir>/<script-name>.py <repo_path>
```

This will:
- [List what the script does]
- [Key features]
- [What it searches for]

2. **Manual search if needed:**
```bash
# [Provide 3-5 fallback bash commands]
find . -name "<pattern>" | head -10
grep -ri "<keyword>" . --include="*.md" | head -10
```

3. **Read files you find:**
```bash
# Use Read tool
Read <file_path>
```

### Phase 2: [Main Assessment Component] (X points)

**Required Elements:**
1. [Element 1]
2. [Element 2]
3. [Element 3]

**Scoring Logic:**
```
Start with X points

Found <artifact>:
- Has <element1>: +0 (baseline)
- Missing <critical_element>: -Y (deduction)

Quality bonuses:
- <Quality indicator>: +Z bonus

No <artifact> found: 0 points
```

**Read and Analyze:**
```bash
Read <artifact_path>
```

Check for:
- [Specific criteria to verify]

### Phase 3: [Secondary Component] (Y points)

[Similar structure to Phase 2]

---

## Scoring Summary

```
Total: 10 points maximum

<Component 1>: 0-X points
  - [Breakdown]

<Component 2>: 0-Y points
  - [Breakdown]

Total: Sum of components (max 10.0)
```

---

## Output Format

```json
{
  "skill": "<skill-name>",
  "score": 7.5,
  "max_score": 10.0,
  "passed": true,
  "files_found": {
    "<artifact_type>": ["path1", "path2"]
  },
  "<component>_analysis": {
    "score": 3.5,
    "present": true,
    "details": {}
  },
  "recommendations": []
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** only check root directory
✅ **DO** search entire repository recursively

❌ **DON'T** assume standard file names
✅ **DO** check for variations and alternatives

❌ **DON'T** give 0 if files are in unexpected locations
✅ **DO** use helper script and manual search

❌ **DON'T** just grep without verification
✅ **DO** read actual files to verify content

---

## Example Execution

```bash
# Step 1: Run helper script
python .claude/skills/<skill-dir>/<script>.py /path/to/repo

# Step 2: Read found files
Read <file1>
Read <file2>

# Step 3: Calculate score
# Step 4: Generate JSON output
```

---

## Tips for Accurate Assessment

1. **Always run helper script first**
2. **Read files, don't just grep**
3. **Check file sizes**
4. **Give partial credit**
5. **Verify quality, not just presence**

**Success = Finding what exists, even if it's not where you expect it!**
```

---

## Specific Updates Needed for Each Skill

### Skill 4: Testing Quality

**Helper Script:** `analyze_tests.py`

**Key Sections:**
- Phase 1: Find test files (test_*.py, *.test.js, *Test.java)
- Phase 2: Test Coverage Assessment (3 points)
  - Number of test files
  - Total test count
  - Has assertions and mocks
- Phase 3: Coverage Configuration (2 points)
  - pytest.ini, .coveragerc, jest.config.js
- Phase 4: CI Testing (2 points)
  - Tests run in CI/CD pipeline
- Phase 5: Test Quality (3 points)
  - Edge cases, meaningful tests, good coverage

**Manual Fallbacks:**
```bash
find . -name "test_*.py" -o -name "*_test.py" -o -name "*.test.js"
grep -r "def test_\|it(\|describe(" . --include="*.py" --include="*.js"
find . -name "pytest.ini" -o -name ".coveragerc" -o -name "jest.config.js"
```

---

### Skill 5: Research & Analysis

**Helper Script:** `find_research.py`

**Key Sections:**
- Phase 1: Find Jupyter notebooks (.ipynb)
- Phase 2: Notebook Quality (4 points)
  - Multiple notebooks
  - Has visualizations (matplotlib, seaborn, plotly)
  - Has analysis (pandas, numpy, scipy)
- Phase 3: Data Files (2 points)
  - CSV, JSON, Excel files
  - Data processing evidence
- Phase 4: Analysis Documentation (2 points)
  - Markdown cells explaining analysis
  - Results interpretation
- Phase 5: Reproducibility (2 points)
  - Requirements listed
  - Clear execution order

**Manual Fallbacks:**
```bash
find . -name "*.ipynb"
grep -l "matplotlib\|seaborn\|plotly" *.ipynb
find . -name "*.csv" -o -name "*.json" -o -name "*.xlsx"
```

---

### Skill 6: UI/UX

**Helper Script:** `find_ui_docs.py`

**Key Sections:**
- Phase 1: Find screenshots and images
- Phase 2: Visual Documentation (3 points)
  - Screenshots in README
  - UI mockups/wireframes
  - Interface images
- Phase 3: UI Documentation (3 points)
  - User guide
  - Interface documentation
  - Interaction flows
- Phase 4: Design Documentation (2 points)
  - Design decisions
  - UX considerations
- Phase 5: Accessibility (2 points)
  - Accessibility notes
  - Responsive design docs

**Manual Fallbacks:**
```bash
find . -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.svg"
grep -i "!\[.*\](.*\.(png|jpg))" README.md
find . -name "*ui*.md" -o -name "*interface*.md" -o -name "*design*.md"
```

---

### Skill 7: Version Management

**Helper Script:** `analyze_git_history.py`

**Key Sections:**
- Phase 1: Git Commit Analysis
- Phase 2: Commit Quality (2 points)
  - Commit count >10
  - Meaningful commit messages
- Phase 3: PROMPT_BOOK.md (5 points) **CRITICAL**
  - Exists and comprehensive
  - Documents AI interactions
  - Shows iteration history
- Phase 4: Branching Strategy (1 point)
  - Multiple branches
  - Branch naming conventions
- Phase 5: Version Tags (2 points)
  - Release tags
  - Semantic versioning

**Manual Fallbacks:**
```bash
git log --oneline | wc -l
git log --oneline | head -20
find . -iname "prompt*book*" -o -iname "prompt*log*"
git branch -a
git tag
```

---

### Skill 8: Costs & Pricing

**Helper Script:** `find_cost_analysis.py`

**Key Sections:**
- Phase 1: Find cost documentation
- Phase 2: Cost Analysis Document (5 points)
  - Cost breakdown
  - Budget estimates
  - Cost optimization notes
- Phase 3: Usage Tracking (3 points)
  - API usage logs
  - Cost monitoring
  - Budget tracking
- Phase 4: Cost Optimization (2 points)
  - Optimization strategies
  - Cost-saving measures

**Manual Fallbacks:**
```bash
find . -iname "*cost*" -o -iname "*budget*" -o -iname "*pricing*"
grep -ri "cost\|budget\|pricing\|\$" . --include="*.md" | head -20
```

---

### Skill 9: Extensibility

**Helper Script:** `analyze_extensibility.py`

**Key Sections:**
- Phase 1: Plugin/Extension System
- Phase 2: Plugin Architecture (3 points)
  - Plugin directory
  - Extension mechanism
  - Plugin documentation
- Phase 3: Interfaces/Abstractions (3 points)
  - Abstract classes
  - Interfaces
  - Dependency injection
- Phase 4: Modular Structure (2 points)
  - Files <200 lines average
  - Clear module separation
- Phase 5: Extension Documentation (2 points)
  - How to extend
  - Plugin examples

**Manual Fallbacks:**
```bash
find . -type d -name "plugin*" -o -name "extension*"
grep -r "@abstractmethod\|abstract class\|interface" . --include="*.py" --include="*.java"
```

---

### Skill 10: Quality Standards

**Helper Script:** `find_quality_tools.py`

**Key Sections:**
- Phase 1: Linting Configuration
- Phase 2: Linting Tools (3 points)
  - .pylintrc, .eslintrc, etc.
  - Configured and active
- Phase 3: CI/CD Pipeline (3 points)
  - GitHub Actions, GitLab CI, etc.
  - Automated quality checks
- Phase 4: Code Style Guide (2 points)
  - CONTRIBUTING.md
  - Style documentation
- Phase 5: Pre-commit Hooks (2 points)
  - .pre-commit-config.yaml
  - Automated formatting

**Manual Fallbacks:**
```bash
find . -name ".pylintrc" -o -name ".eslintrc*" -o -name ".flake8"
find . -path "*/.github/workflows/*.yml"
find . -name "CONTRIBUTING.md" -o -name "*style*.md"
find . -name ".pre-commit-config.yaml"
```

---

## Next Steps

1. **Apply this template to each SKILL.md file (skills 4-10)**
2. **Customize the scoring logic for each skill**
3. **Add skill-specific examples and criteria**
4. **Test each skill on a sample repository**
5. **Update the tier2-orchestrator to use improved skills**

---

## Summary

✅ **Completed:**
- Skills 1-3: Fully updated with scripts and SKILL.md
- Scripts 4-10: All helper scripts created

⏳ **Remaining:**
- Update SKILL.md files for skills 4-10 using this template
- Each takes ~15 minutes to customize properly
- Total remaining time: ~2 hours

**Key Principle:** Every skill now has:
1. Helper script for comprehensive discovery
2. Manual fallback commands
3. File reading and verification
4. Partial credit scoring
5. Thorough "Be Thorough!" section

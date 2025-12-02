---
name: 2-code-documentation
description: Evaluates README quality, code documentation, docstrings, and project structure. Use for Tier 2 code documentation assessment.
version: 2.0.0
---

# Skill 2: Code Documentation

You are an autonomous agent that thoroughly evaluates code documentation quality.

**Your Mission:** Find and assess README files, docstrings, code comments, and structural documentation.

**Scoring:** 10 points maximum
- README: 3 points
- Code Documentation (docstrings): 3 points
- Project Structure Documentation: 2 points
- Additional Documentation: 2 points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery (Find ALL documentation)

**DO NOT assume standard locations!**

1. **Run the helper script first:**
```bash
python .claude/skills/2-code-documentation/find_documentation.py <repo_path>
```

This will:
- Find ALL README files (any directory, case-insensitive)
- Count docstrings in Python, JavaScript, Java files
- Find additional docs (CONTRIBUTING.md, API docs, guides)
- Analyze code structure documentation
- Check for inline comments

2. **Manual search if needed:**
```bash
# Find README files anywhere
find . -iname "readme.md" -o -iname "readme.txt" | head -10

# Find documentation directories
find . -type d -name "docs" -o -name "documentation" -o -name "doc" | head -5

# Search for installation instructions (might be in any file)
grep -ri "installation\|install\|setup" . --include="*.md" | head -10

# Find API documentation
find . -name "API.md" -o -name "api.md" -o -name "reference.md" | head -5
```

3. **Read documentation files:**
```bash
# Use Read tool on README and other docs
Read <readme_path>
Read docs/API.md
Read CONTRIBUTING.md
```

### Phase 2: README Assessment (3 points)

**Required Elements:**
1. Project description (what it does)
2. Installation instructions (how to set up)
3. Usage examples (how to use)
4. Dependencies/requirements listed
5. Configuration guide (if applicable)

**Scoring Logic:**
```
Start with 3 points

Found README:
- Exists and >1KB: +0 (baseline)
- Has project description: +0 (baseline)
- Missing README entirely: 0 points (stop here)

Content Quality:
- Has installation instructions: +0 (baseline)
- Missing installation: -1.0
- Has usage examples: +0 (baseline)
- Missing usage examples: -1.0
- Has code blocks with examples: +0 (baseline)
- Missing code examples: -0.5
- Lists dependencies/requirements: +0.5 bonus
- Has troubleshooting/FAQ: +0.5 bonus

Size/Comprehensiveness:
- <200 words: -0.5 (too brief)
- 200-500 words: +0 (adequate)
- 500+ words: +0.5 bonus (comprehensive)

Max: 3.5 points (capped at 3.0)
```

**Read and Analyze:**
```bash
# Read the README
Read <readme_path>
```

Check for:
- Clear project title and description
- Step-by-step installation instructions
- Working code examples
- Dependencies listed (requirements.txt, package.json, etc.)
- Configuration instructions
- Visual aids (screenshots, diagrams)

### Phase 3: Docstrings Assessment (3 points)

**Check for docstrings in code:**

Python:
```bash
# Find Python files with docstrings
find . -name "*.py" -exec grep -l '"""' {} \; | wc -l
find . -name "*.py" | wc -l

# Show examples
find . -name "*.py" -exec grep -A 3 'def ' {} \; | grep -A 3 '"""' | head -20
```

JavaScript/TypeScript:
```bash
# Find JSDoc comments
grep -r "/\*\*" . --include="*.js" --include="*.ts" | wc -l
find . -name "*.js" -o -name "*.ts" | wc -l
```

Java:
```bash
# Find JavaDoc comments
grep -r "/\*\*" . --include="*.java" | wc -l
find . -name "*.java" | wc -l
```

**Scoring Logic:**
```
Docstring Coverage = (files with docstrings) / (total code files)

Coverage >= 70%: 3.0 points (excellent)
Coverage 50-69%: 2.5 points (good)
Coverage 30-49%: 2.0 points (adequate)
Coverage 10-29%: 1.0 points (minimal)
Coverage < 10%: 0.5 points (poor)
No docstrings: 0 points
```

**Quality Indicators:**
- Docstrings describe what functions do
- Include parameter descriptions
- Include return value descriptions
- Include usage examples

**Sample and Verify:**
```bash
# Read a few Python files to verify docstring quality
Read <sample_python_file.py>
```

### Phase 4: Project Structure Documentation (2 points)

**Check for structure documentation:**

1. **docs/ directory (1 point):**
```bash
find . -type d -name "docs" -o -name "documentation" | head -5
ls docs/
```

If found:
- Has docs/ with content: +1.0 point
- Has docs/ but empty: +0.5 points
- No docs/: +0 points

2. **Code organization documentation (1 point):**
```bash
# Check for ARCHITECTURE.md or structure docs
find . -name "ARCHITECTURE.md" -o -name "STRUCTURE.md" -o -name "PROJECT_STRUCTURE.md"

# Check for module-level docstrings (Python)
find . -name "__init__.py" -exec grep -l '"""' {} \;

# Check README for structure section
grep -i "structure\|organization\|directory" README.md
```

**Scoring:**
- Has architecture/structure documentation: +1.0
- Has module-level docstrings: +0.5
- README explains structure: +0.5
- No structure docs: +0

Max: 2.0 points

### Phase 5: Additional Documentation (2 points)

**Look for supplementary docs:**

```bash
# CONTRIBUTING guide
find . -name "CONTRIBUTING.md" -o -name "DEVELOPMENT.md"

# CHANGELOG
find . -name "CHANGELOG.md" -o -name "CHANGES.md" -o -name "HISTORY.md"

# API documentation
find . -name "API.md" -o -name "api_reference.md"

# User guide
find . -name "*guide*.md" -o -name "manual.md" -o -name "tutorial.md"
```

**Scoring:**
- Has CONTRIBUTING.md: +0.5
- Has CHANGELOG.md: +0.5
- Has API documentation: +0.5
- Has user guide/tutorial: +0.5

Max: 2.0 points

---

## Scoring Summary

```
Total: 10 points maximum

README Quality: 0-3 points
  - Exists with description: baseline
  - Installation instructions: required
  - Usage examples: required
  - Comprehensive: bonus

Docstrings: 0-3 points
  - Coverage based on percentage of files
  - 70%+ coverage: 3 points
  - Quality matters (descriptive, not just stubs)

Structure Documentation: 0-2 points
  - docs/ directory: 1 point
  - Architecture/structure docs: 1 point

Additional Documentation: 0-2 points
  - Each additional doc type: +0.5
  - CONTRIBUTING, CHANGELOG, API, guides

Total: Sum of all components (max 10.0)
```

---

## Output Format

```json
{
  "skill": "code-documentation",
  "score": 7.5,
  "max_score": 10.0,
  "passed": true,
  "files_found": {
    "readme": ["README.md"],
    "docs_directory": ["docs/"],
    "contributing": ["CONTRIBUTING.md"],
    "changelog": [],
    "api_docs": ["docs/API.md"]
  },
  "readme_analysis": {
    "score": 2.5,
    "present": true,
    "path": "README.md",
    "size_bytes": 3245,
    "word_count": 856,
    "has_installation": true,
    "has_usage": true,
    "has_examples": true,
    "has_dependencies": false,
    "code_blocks": 5,
    "quality": "comprehensive"
  },
  "docstring_analysis": {
    "score": 2.5,
    "python": {
      "total_files": 15,
      "files_with_docstrings": 10,
      "coverage": 67,
      "total_docstrings": 45
    },
    "javascript": {
      "total_files": 8,
      "files_with_docstrings": 4,
      "coverage": 50,
      "total_docstrings": 12
    },
    "overall_coverage": 61,
    "quality_notes": "Good coverage but some docstrings are brief"
  },
  "structure_documentation": {
    "score": 1.5,
    "has_docs_directory": true,
    "has_architecture_doc": false,
    "has_module_docstrings": true,
    "readme_explains_structure": true
  },
  "additional_documentation": {
    "score": 1.0,
    "has_contributing": true,
    "has_changelog": false,
    "has_api_docs": true,
    "has_user_guide": false
  },
  "recommendations": [
    "Add CHANGELOG.md to track version changes",
    "Improve docstring coverage to 70%+",
    "Add dependencies section to README"
  ]
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** only check root directory for README
✅ **DO** search entire repository (might be in subdirectory)

❌ **DON'T** assume README.md is the only name
✅ **DO** check for readme.txt, README.rst, readme.markdown, etc.

❌ **DON'T** just check if docstrings exist
✅ **DO** count coverage percentage and verify quality

❌ **DON'T** miss documentation in non-standard locations
✅ **DO** search docs/, documentation/, doc/, wiki/ directories

❌ **DON'T** give 0 if README is small
✅ **DO** give partial credit based on content quality

❌ **DON'T** ignore inline comments
✅ **DO** check for meaningful comments in code

---

## Example Execution

```bash
# Step 1: Run helper script
python .claude/skills/2-code-documentation/find_documentation.py /path/to/repo

# Step 2: Read found documentation
Read /path/to/repo/README.md
Read /path/to/repo/docs/API.md

# Step 3: Sample code files for docstring quality
Read /path/to/repo/src/main.py
Read /path/to/repo/lib/utils.js

# Step 4: Calculate coverage percentages
# Python: 10/15 files = 67%
# JavaScript: 4/8 files = 50%

# Step 5: Generate JSON output with scores
```

---

## Tips for Accurate Assessment

1. **README is critical** - Most projects put everything in README
2. **Check multiple languages** - Project might use Python, JS, and Java
3. **Verify docstring quality** - Not just presence, but usefulness
4. **Give partial credit** - 50% coverage is better than 0%
5. **Check subdirectories** - docs/ might contain extensive documentation
6. **Look for embedded docs** - Installation might be in a separate INSTALL.md
7. **Consider project size** - Small project needs less documentation than large one

**Success = Finding all documentation that exists and assessing it fairly!**

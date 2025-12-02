---
name: 7-version-management
description: Evaluates Git practices and Prompt documentation (any filename accepted). Use for Tier 2 version management assessment.
version: 2.1.0
---

# Skill 7: Version Management

You are an autonomous agent that thoroughly evaluates version control practices and AI prompt documentation.

**Your Mission:** Find and assess Git history, prompt documentation (any filename), and version management practices.

**Scoring:** 10 points maximum
- **Prompt Documentation: 5 points (CRITICAL - this is an AI course!)**
- Git Commit History: 2 points
- Commit Message Quality: 2 points
- Branching Strategy: 1 point

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery

1. **Run the helper script:**
```bash
python .claude/skills/7-version-management/analyze_git_history.py <repo_path>
```

2. **Manual search:**
```bash
# Find ANY prompt documentation (CRITICAL!)
find . -iname "*prompt*" | grep -i "\\.md$\|\\.txt$"
find . -name "PROMPT*.md" -o -name "prompt*.md" -o -name "*prompts*.md"

# Check git history
git log --oneline | wc -l
git log --oneline | head -20
git branch -a
```

### Phase 2: Prompt Documentation Assessment (5 points) **CRITICAL!**

**This is an AI/LLM course - Prompt documentation is MANDATORY (ANY filename accepted)**

```bash
# Search exhaustively for ANY prompt documentation
find . -iname "*prompt*" | grep -i "\\.md$"
find . -iname "*ai*.md" | grep -i "prompt\|chat\|conversation"
grep -ri "prompt engineering\|ai prompts\|claude\|chatgpt" . --include="*.md" | head -10
```

**Scoring:**
```
Prompt Documentation Score:

Found and Comprehensive (5.0 points):
- ANY prompt documentation file exists (PROMPT_BOOK.md, PROMPTS.md, prompt_log.md, ai_prompts.md, etc.)
- Documents AI interactions and iterations
- Shows prompt evolution
- Includes results/learnings
- Well-organized chronologically

Found but Basic (3.0 points):
- Prompt documentation exists
- Has some prompt documentation
- Missing details or organization

Mentioned in README (1.0 point):
- README has section about prompts used
- Minimal documentation

Not Found (0 points):
- No prompt documentation anywhere
- This is a FAIL for an AI course project
```

**IMPORTANT:** Accept ANY filename as long as it contains prompt documentation:
- ✓ PROMPT_BOOK.md
- ✓ PROMPTS.md
- ✓ prompt_log.md
- ✓ ai_prompts.md
- ✓ prompt_library.md
- ✓ docs/prompts/README.md
- ✓ Any markdown file with prompt content

**READ the prompt documentation:**
```bash
Read <prompt_doc_path>
```

Verify:
- Documents prompts used with Claude/ChatGPT/LLMs
- Shows iteration and refinement
- Includes what worked and what didn't
- Organized by feature or chronologically

### Phase 3: Git Commit History (2 points)

```bash
# Count commits
git log --oneline | wc -l

# Check commit frequency
git log --oneline --all | head -30
```

**Scoring:**
- 20+ commits: 2.0 points
- 10-19 commits: 1.5 points
- 5-9 commits: 1.0 point
- <5 commits: 0.5 points

### Phase 4: Commit Message Quality (2 points)

```bash
# Sample commit messages
git log --oneline | head -20
```

**Scoring:**
- Meaningful messages (not just "fix", "update"): 2.0 points
- Some meaningful, some generic: 1.0 point
- All generic/poor: 0 points

### Phase 5: Branching Strategy (1 point)

```bash
git branch -a
```

**Scoring:**
- Multiple branches with purpose: 1.0 point
- Single branch only: 0 points

---

## Scoring Summary

```
Total: 10 points maximum

Prompt Documentation: 0-5 points (CRITICAL!)
  - This is an AI course - prompt documentation is MANDATORY
  - ANY filename accepted (PROMPT_BOOK.md, PROMPTS.md, prompt_log.md, etc.)
  - Comprehensive documentation: 5 points
  - Basic documentation: 3 points
  - No documentation: 0 points (major failure)

Git Commit History: 0-2 points
  - Based on commit count

Commit Message Quality: 0-2 points
  - Meaningful vs generic messages

Branching Strategy: 0-1 point
  - Multiple branches: 1 point

Total: Sum of components (max 10.0)
```

---

## Important: Be Thorough!

**CRITICAL for Prompt Documentation:**

❌ **DON'T** only check root directory
✅ **DO** search ENTIRE repository recursively

❌ **DON'T** assume it's named exactly "PROMPT_BOOK.md"
✅ **DO** check for: prompt_book.md, PromptBook.md, PROMPTS.md, prompt_log.md, AI_PROMPTS.md

❌ **DON'T** give 0 if file is in docs/ or other subdirectory
✅ **DO** search everywhere: root, docs/, documentation/, logs/, prompts/

❌ **DON'T** miss prompt documentation embedded in README
✅ **DO** check README for prompt sections

**This is an AI course - prompt documentation is NOT optional!**

---

## Example Execution

```bash
# CRITICAL: Find ANY prompt documentation
python .claude/skills/7-version-management/analyze_git_history.py /path/to/repo
find /path/to/repo -iname "*prompt*" | grep -i "\.md$"
find /path/to/repo -iname "*prompt*book*" -o -iname "*prompts*"

# If found, READ IT (any filename works!)
Read /path/to/repo/PROMPT_BOOK.md
Read /path/to/repo/docs/PROMPTS.md
Read /path/to/repo/prompt_log.md
Read /path/to/repo/docs/prompts/README.md

# Check git history
cd /path/to/repo
git log --oneline | wc -l
git log --oneline | head -20

# Calculate score
# Prompt Docs: 5.0 (comprehensive, found PROMPTS.md)
# Commit history: 2.0 (25+ commits)
# Commit quality: 1.5 (mostly meaningful)
# Branching: 1.0 (multiple branches)
# Total: 9.5/10
```

---

## Tips

1. **Prompt documentation is worth HALF the points** - search exhaustively!
2. **ANY filename is acceptable** - PROMPT_BOOK.md, PROMPTS.md, prompt_log.md, ai_prompts.md, etc.
3. **Case-insensitive search** - might be prompt_book.md, PromptBook.md, PROMPTS.md
4. **Check subdirectories** - docs/, documentation/, prompts/, logs/
5. **Read the file** - verify it actually documents AI prompts
6. **Give credit for embedded docs** - README section about prompts counts

**Success = Finding prompt documentation no matter what it's named or where it is!**

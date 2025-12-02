---
name: 1-project-planning
description: Evaluates Product Requirements Document (PRD) and Architecture Documentation quality. Use when assessing project planning for Tier 2 students.
version: 2.0.0
---

# Skill 1: Project Documents and Planning

You are an autonomous agent that thoroughly evaluates project planning documentation quality.

**Your Mission:** Find and assess PRD and Architecture documents, no matter where they're located in the repository.

**Scoring:** 10 points maximum
- PRD: 5 points
- Architecture: 5 points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery (Find ALL planning documents)

**DO NOT assume standard locations!** Students put files in unexpected places.

1. **Run the helper script first:**
```bash
python .claude/skills/1-project-planning/find_planning_docs.py <repo_path>
```

This will search the ENTIRE repository for:
- PRD files (prd.md, requirements.md, product_requirements.md, etc.)
- Architecture files (architecture.md, design.md, planning.md, etc.)
- All diagram files (.png, .jpg, .svg, .puml)
- Check file contents for required sections

2. **Manually search if script finds nothing:**
```bash
# Find any markdown files that might contain planning docs
find . -type f -name "*.md" ! -path "*/node_modules/*" ! -path "*/.git/*" | head -20

# Search for PRD content in ANY file
grep -ri "product requirements\|functional requirements\|problem statement" . --include="*.md" --include="*.txt" | head -10

# Search for architecture content
grep -ri "architecture\|c4 model\|system design\|component diagram" . --include="*.md" | head -10

# Find README files (sometimes planning is embedded there)
find . -name "README.md" -o -name "readme.md" | head -5
```

3. **Read potential files:**
   - If you find a README.md, READ IT - planning might be embedded
   - If you find docs/ directory, READ files in it
   - If you find a PLANNING.md, READ IT - might contain both PRD and architecture
   - Look for subdirectories like: docs/, documentation/, plans/, design/

### Phase 2: PRD Assessment (5 points)

**Required Sections (case-insensitive search):**
1. Problem Statement (what problem are we solving?)
2. Functional Requirements (features and capabilities)
3. Non-Functional Requirements (performance, security, scalability)
4. Success Metrics (how do we measure success?)
5. Technical Constraints (limitations and boundaries)
6. User Stories (who uses it and how?)

**Scoring Logic:**
```
Start with 5 points

Found PRD file:
- Has Problem Statement: +0 (baseline)
- Has Functional Requirements: +0 (baseline)
- Missing Problem Statement: -1.5
- Missing Functional Requirements: -2.0 (CRITICAL)
- Missing Non-Functional Requirements: -1.0
- Missing Success Metrics: -1.0
- Missing Technical Constraints: -0.5
- Missing User Stories: -0.5

Quality bonuses:
- PRD is comprehensive (>1000 words): +0.5
- Requirements are prioritized (P0, P1, P2): +0.5
- Success metrics are measurable: +0.5

No PRD found at all: 0 points
```

**Read the PRD file(s) you found:**
```bash
# Use Read tool on the PRD file
Read <prd_file_path>
```

Analyze the content:
- Are sections present and substantial (not just headers)?
- Are requirements detailed or just bullet points?
- Are success metrics specific numbers or vague?
- Is it comprehensive (>500 words minimum)?

### Phase 3: Architecture Assessment (5 points)

**Required Elements:**
1. Architecture document (any .md file with architecture content)
2. C4 Model diagrams OR equivalent system diagrams
   - Context Level (how system fits in environment)
   - Container Level (high-level tech choices)
   - Component Level (internal structure)
3. Technology stack documentation (why these technologies?)
4. Design decisions rationale

**Scoring Logic:**
```
Start with 5 points

Found Architecture documentation:
- Has architecture content: +0 (baseline)
- Missing architecture doc: -5 (0 points total)

Diagrams:
- Has Context-level diagram (or equivalent): +0 (baseline)
- Has Container-level diagram (or equivalent): +0 (baseline)
- Has Component-level diagram: +0.5 bonus
- Missing Context diagram: -1.5
- Missing Container diagram: -1.5
- No diagrams at all: -2.0

Content:
- Technology stack documented: +0 (baseline)
- Missing tech stack: -1.0
- Has design rationale (WHY choices made): +0.5 bonus
- Has ADRs (Architecture Decision Records): +0.5 bonus

Max score: 5.0 (with bonuses)
```

**Diagram Detection:**

Look for diagrams in multiple ways:
1. Embedded diagrams (mermaid, plantuml):
```bash
grep -r "```mermaid\|```plantuml\|@startuml" . --include="*.md"
```

2. Image files referenced:
```bash
# Find diagram images
find . -name "*diagram*.png" -o -name "*architecture*.png" -o -name "*design*.png" -o -name "*.svg"

# Check if README references images
grep -i "!\[.*\](.*\.png)" README.md docs/*.md
```

3. External diagram tools:
```bash
find . -name "*.puml" -o -name "*.plantuml" -o -name "*.drawio"
```

**Read the Architecture file(s) you found:**
```bash
# Use Read tool
Read <architecture_file_path>
```

Check for:
- System overview and context
- Component breakdown
- Technology choices with justification
- Data flow or interaction patterns

---

## Output Format

Return a JSON object:

```json
{
  "skill": "project-planning",
  "score": 8.5,
  "max_score": 10.0,
  "passed": true,
  "files_found": {
    "prd": ["docs/PRD.md", "README.md (contains requirements)"],
    "architecture": ["docs/PLANNING.md"],
    "diagrams": ["docs/architecture.png", "docs/component-diagram.svg"]
  },
  "prd_analysis": {
    "score": 4.5,
    "present": true,
    "file": "docs/PRD.md",
    "size_bytes": 4523,
    "word_count": 1205,
    "found_sections": [
      "Problem Statement",
      "Functional Requirements",
      "Non-Functional Requirements",
      "Success Metrics"
    ],
    "missing_sections": [
      "Technical Constraints",
      "User Stories"
    ],
    "quality_notes": [
      "Comprehensive document with good detail",
      "Requirements are numbered but not prioritized",
      "Success metrics are specific and measurable"
    ]
  },
  "architecture_analysis": {
    "score": 4.0,
    "present": true,
    "file": "docs/PLANNING.md",
    "size_bytes": 3421,
    "has_c4_context": true,
    "has_c4_container": true,
    "has_c4_component": false,
    "has_diagrams": true,
    "diagram_types": ["mermaid", "png images"],
    "has_tech_stack": true,
    "has_design_rationale": false,
    "quality_notes": [
      "Good high-level diagrams",
      "Technology stack documented",
      "Missing component-level detail",
      "No explanation of WHY technologies were chosen"
    ]
  },
  "recommendations": [
    "Add 'Technical Constraints' section to PRD",
    "Add Component-level C4 diagram",
    "Document rationale for technology choices",
    "Add user stories to clarify use cases"
  ]
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** only check root directory for PRD.md
✅ **DO** search entire repository recursively

❌ **DON'T** assume files are named exactly "PRD.md"
✅ **DO** search for variations: requirements.md, product_requirements.md, etc.

❌ **DON'T** give 0 if file is in unexpected location
✅ **DO** use helper script and manual search to find it

❌ **DON'T** just grep for section names
✅ **DO** read the actual file content to verify sections exist and are substantial

❌ **DON'T** miss embedded planning in README.md
✅ **DO** check README for requirements and architecture sections

❌ **DON'T** ignore docs/, documentation/, or design/ directories
✅ **DO** explore all reasonable locations

---

## Example Execution

```bash
# Student repository is in: /path/to/repo

# Step 1: Run helper script
python .claude/skills/1-project-planning/find_planning_docs.py /path/to/repo

# Step 2: Based on results, read found files
Read /path/to/repo/docs/PRD.md
Read /path/to/repo/README.md
Read /path/to/repo/docs/architecture.md

# Step 3: Check for diagrams
ls /path/to/repo/docs/*.png
grep -r "```mermaid" /path/to/repo/docs/

# Step 4: Calculate score based on findings
# Step 5: Generate JSON output
```

---

## Tips for Accurate Assessment

1. **Always run the helper script first** - it does comprehensive recursive search
2. **Read files, don't just grep** - verify content is substantial, not just headers
3. **Check file sizes** - a 500-byte PRD.md is probably just a stub
4. **Look for embedded content** - README might contain everything
5. **Search case-insensitively** - "problem statement" = "Problem Statement" = "PROBLEM STATEMENT"
6. **Count words** - comprehensive PRD should be 1000+ words
7. **Verify diagrams actually exist** - don't trust references, check files
8. **Give partial credit** - if 4/6 sections present, give proportional points

**Success = Finding what exists, even if it's not where you expect it!**

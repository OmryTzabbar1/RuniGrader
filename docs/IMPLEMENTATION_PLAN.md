# Implementation Plan: Two-Tier Grading System with 10 Assessment Skills

**Version:** 1.0
**Date:** 2025-12-01
**Project:** Runi - Student Assignment Grading System

---

## Executive Summary

This system grades student assignments using a **two-tier approach** based on self-assessed grades:

- **Tier 1 (Self-Grade < 80)**: Simple grading - count TRUE criteria from markdown (0-22) → Final Grade
- **Tier 2 (Self-Grade ≥ 80)**: Rigorous assessment using 10 specialized skills (each scored out of 10)

---

## 10 Assessment Skills Created

All skills are located in: `C:\Users\Guest1\CoOp\Runi\.claude\skills\`

### Skill Breakdown

| # | Skill Name | Category | Points | Key Focus |
|---|------------|----------|--------|-----------|
| 1 | project-planning | Documents | 10 | PRD & Architecture docs |
| 2 | code-documentation | Code Quality | 10 | README, structure, docstrings |
| 3 | config-security | Security | 10 | Config management, no secrets |
| 4 | testing-quality | Testing | 10 | Unit tests, coverage, edge cases |
| 5 | research-analysis | Research | 10 | Parameter studies, notebooks, charts |
| 6 | ui-ux | UX | 10 | Interface quality, documentation |
| 7 | version-management | Git & AI | 10 | Git practices, prompt book |
| 8 | costs-pricing | Economics | 10 | Cost analysis, budget tracking |
| 9 | extensibility | Architecture | 10 | Extension points, maintainability |
| 10 | quality-standards | Standards | 10 | ISO/IEC 25010 compliance |

**Total Possible**: 100 points from skills

---

## Grading Flow

```
┌─────────────────────────────────────┐
│ Input: Student Submission           │
│ - GitHub repo URL                   │
│ - Self-grade (60-100)               │
│ - Assessment markdown (22 criteria) │
└─────────────────────────────────────┘
              │
              ▼
     ┌────────────────┐
     │ Parse Markdown │
     │ Count TRUE/22  │
     └────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Check Self-Grade     │
    │ < 80 or ≥ 80?        │
    └──────────────────────┘
         │            │
    < 80 │            │ ≥ 80
         ▼            ▼
  ┌────────────┐  ┌─────────────────┐
  │ TIER 1     │  │ TIER 2          │
  │ Simple     │  │ Rigorous        │
  │            │  │                 │
  │ Final =    │  │ Run 10 Skills   │
  │ (met/22)×  │  │ Each scored     │
  │  100       │  │ out of 10       │
  └────────────┘  └─────────────────┘
         │                │
         └────────┬───────┘
                  ▼
        ┌─────────────────┐
        │ Update Excel    │
        │ Generate PDF    │
        └─────────────────┘
```

---

## Tier 1: Simple Grading (Self-Grade < 80)

### Process

1. **Input**: Assessment markdown file
2. **Parse**: Count TRUE criteria (out of 22)
3. **Calculate**: `final_grade = (requirements_met / 22) × 100`
4. **Output**:
   - Update Excel: Add final grade
   - Generate PDF: Simple report with grade

### Example

```
Student: 63688
Self-Grade: 75
Requirements Met: 10/22

Final Grade = (10/22) × 100 = 45.45%

PDF Contents:
- Student Info
- Requirements Met: 10/22
- Final Grade: 45.45%
- Brief feedback
```

---

## Tier 2: Rigorous Assessment (Self-Grade ≥ 80)

### Process

1. **Clone Repository**: Download student's GitHub repo
2. **Run 10 Skills**: Each skill assesses different aspect (10 points each)
3. **Aggregate Scores**: Total out of 100 points
4. **Calculate Final Grade**: Convert to percentage
5. **Output**:
   - Update Excel: Add final grade + skill breakdown
   - Generate PDF: Comprehensive report with all details

### Skill Execution

```python
def grade_rigorous(repo_path: str, self_grade: int) -> Dict:
    """Run all 10 skills and aggregate scores."""

    scores = {}

    # Skill 1: Project Planning
    scores['planning'] = run_skill('1-project-planning', repo_path)

    # Skill 2: Code Documentation
    scores['documentation'] = run_skill('2-code-documentation', repo_path)

    # Skill 3: Configuration & Security
    scores['security'] = run_skill('3-config-security', repo_path)

    # Skill 4: Testing & Quality
    scores['testing'] = run_skill('4-testing-quality', repo_path)

    # Skill 5: Research & Analysis
    scores['research'] = run_skill('5-research-analysis', repo_path)

    # Skill 6: UI/UX
    scores['ux'] = run_skill('6-ui-ux', repo_path)

    # Skill 7: Version Management
    scores['version'] = run_skill('7-version-management', repo_path)

    # Skill 8: Costs & Pricing
    scores['costs'] = run_skill('8-costs-pricing', repo_path)

    # Skill 9: Extensibility
    scores['extensibility'] = run_skill('9-extensibility', repo_path)

    # Skill 10: Quality Standards
    scores['standards'] = run_skill('10-quality-standards', repo_path)

    total_score = sum(scores.values())  # Out of 100
    final_grade = total_score  # Already percentage

    return {
        'skill_scores': scores,
        'total_score': total_score,
        'final_grade': final_grade
    }
```

### Example

```
Student: 63698
Self-Grade: 100
Requirements Met: 22/22

Skill Scores:
1. Planning: 9/10
2. Documentation: 8.5/10
3. Security: 10/10
4. Testing: 8/10
5. Research: 7.5/10
6. UI/UX: 7/10
7. Version Mgmt: 9/10
8. Costs: 6/10
9. Extensibility: 8/10
10. Quality: 7.5/10

Total: 80.5/100
Final Grade: 80.5%

PDF Contents:
- Student Info
- Overall Score: 80.5/100
- Skill-by-skill breakdown with recommendations
- Detailed feedback from each skill
- Comprehensive improvement suggestions
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (Days 1-3)

**Files to Create:**
- `src/core/parser.py` - Parse markdown assessments
- `src/core/tier_router.py` - Determine tier based on self-grade
- `src/graders/simple_grader.py` - Tier 1 grading logic
- `src/graders/rigorous_grader.py` - Tier 2 skill orchestrator

### Phase 2: Skill Integration (Days 4-6)

**Tasks:**
- Create skill runner/executor
- Test each skill individually
- Create skill result aggregator
- Handle skill failures gracefully

### Phase 3: Excel & PDF Generation (Days 7-9)

**Files to Create:**
- `src/output/excel_writer.py` - Update Excel with grades
- `src/pdf/simple_pdf.py` - Generate Tier 1 PDFs
- `src/pdf/rigorous_pdf.py` - Generate Tier 2 PDFs with skill details

### Phase 4: CLI & Orchestration (Days 10-11)

**Files to Create:**
- `cli.py` - Main CLI interface
- `src/orchestrator.py` - Full pipeline orchestration

### Phase 5: Testing & Validation (Days 12-14)

**Tasks:**
- Test with students from both tiers
- Verify Excel updates work
- Check PDF generation quality
- Run pilot with 5-10 students

---

## CLI Commands

### Grade Single Student

```bash
python cli.py grade-student \
  --student-id 63698 \
  --self-grade 95 \
  --repo-url https://github.com/student/repo \
  --output-dir ./reports
```

### Batch Grade from CSV

```bash
python cli.py batch-grade \
  --self-grades-csv self_grades.csv \
  --input-dir WorkSubmissions03/ \
  --output-dir ./reports
```

**CSV Format:**
```csv
student_id,self_grade,github_url
63687,85,https://github.com/student1/repo
63688,75,https://github.com/student2/repo
63698,100,https://github.com/student3/repo
```

---

## Skill Output Format

Each skill returns a standardized JSON:

```json
{
  "score": 8.5,
  "max_score": 10,
  "passed": true,
  "breakdown": {
    "component1": {"score": 4.5, "max": 5},
    "component2": {"score": 4.0, "max": 5}
  },
  "recommendations": [
    "Specific improvement suggestion 1",
    "Specific improvement suggestion 2"
  ]
}
```

---

## Final Grade Calculation

### Option 1: Skills Only (Recommended for Tier 2)

```python
# For self_grade >= 80, skills are comprehensive enough
final_grade = total_skill_score  # Out of 100
```

### Option 2: Weighted Combination

```python
# Combine skills with TRUE/FALSE criteria
skill_percentage = (total_skill_score / 100) * 100
criteria_percentage = (requirements_met / 22) * 100

# 80% skills + 20% criteria (skills weighted higher for high self-grade)
final_grade = (skill_percentage * 0.8) + (criteria_percentage * 0.2)
```

### Option 3: Both Must Pass

```python
# Must score well on both
skill_percentage = (total_skill_score / 100) * 100
criteria_percentage = (requirements_met / 22) * 100

# Capped by lower score
final_grade = min(skill_percentage, criteria_percentage)
```

**Recommended**: Option 1 for simplicity (skills comprehensively assess all 22 requirements)

---

## Directory Structure

```
Runi/
├── .claude/
│   └── skills/                    # 10 assessment skills
│       ├── 1-project-planning/
│       ├── 2-code-documentation/
│       ├── 3-config-security/
│       ├── 4-testing-quality/
│       ├── 5-research-analysis/
│       ├── 6-ui-ux/
│       ├── 7-version-management/
│       ├── 8-costs-pricing/
│       ├── 9-extensibility/
│       └── 10-quality-standards/
├── src/
│   ├── core/
│   │   ├── parser.py              # Parse markdown
│   │   └── tier_router.py         # Tier determination
│   ├── graders/
│   │   ├── simple_grader.py       # Tier 1 logic
│   │   └── rigorous_grader.py     # Tier 2 orchestrator
│   ├── skills/
│   │   └── skill_runner.py        # Execute skills
│   ├── output/
│   │   └── excel_writer.py        # Update Excel
│   └── pdf/
│       ├── simple_pdf.py          # Tier 1 PDFs
│       └── rigorous_pdf.py        # Tier 2 PDFs
├── cli.py                         # Main CLI
├── docs/
│   ├── PRD.md
│   ├── CLAUDE.md
│   ├── PLANNING.md
│   ├── TASKS.md
│   └── IMPLEMENTATION_PLAN.md     # This file
└── requirements.txt
```

---

## Next Steps

1. **Decide on Final Grade Formula**: Choose Option 1, 2, or 3 above
2. **Start Implementation**: Begin with Phase 1 (Core Infrastructure)
3. **Test Skills Individually**: Verify each skill works on sample repos
4. **Integrate**: Build full pipeline
5. **Pilot**: Test with 5-10 real student submissions

---

## Questions to Answer

1. **Formula Choice**: Which final grade calculation (Option 1/2/3)?
2. **Passing Threshold**: What's minimum % to pass for each tier?
   - Tier 1: 60%? 70%?
   - Tier 2: 70%? 75%?
3. **Self-Grade Source**: Confirmed - CSV file with (student_id, self_grade)?
4. **PDF Format**: Should Tier 1 PDFs be simpler or match student format?

---

## Conclusion

All 10 skills are now created and ready for integration. Each skill is self-contained, documented, and provides structured output for aggregation.

Next: Begin implementation of core infrastructure and skill runner.

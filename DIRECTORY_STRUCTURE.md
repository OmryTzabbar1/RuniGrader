# Runi Project - Directory Structure

**Last Updated:** 2025-12-01

---

## Main Directory Layout

```
Runi/
├── .claude/                          # Claude Code configuration
│   ├── commands/                     # Slash commands
│   │   ├── git-repo-assessment.md   # Repository assessment command
│   │   └── SubmissionRequirements.txt
│   └── skills/                       # Assessment skills
│       ├── 1-project-planning/
│       ├── 2-code-documentation/
│       ├── 3-config-security/
│       ├── 4-testing-quality/
│       ├── 5-research-analysis/
│       ├── 6-ui-ux/
│       ├── 7-version-management/
│       ├── 8-costs-pricing/
│       ├── 9-extensibility/
│       ├── 10-quality-standards/
│       ├── tier2-orchestrator/       # ⭐ NEW: Runs all 10 skills
│       ├── batch-repo-assessment/
│       └── grade-extractor/
│
├── docs/                             # 📚 Documentation
│   ├── PRD.md                        # Product requirements
│   ├── CLAUDE.md                     # Development guidelines
│   ├── PLANNING.md                   # Technical architecture
│   ├── TASKS.md                      # Task tracking
│   ├── IMPLEMENTATION_PLAN.md        # Two-tier system plan
│   ├── IMPLEMENTATION_SUMMARY.md     # Skills summary
│   ├── GRADING_WORKFLOW.md          # User grading workflow
│   ├── CLAUDE_GRADING_PROCESS.md    # Claude's process
│   ├── CRITICAL_INDIVIDUAL_ASSESSMENT.md  # ⚠️ Important rules
│   └── grading_formula_description.md
│
├── WorkSubmissions01/                # 📁 Assignment 1 submissions
│   ├── Participant_38950_assignsubmission_file/
│   │   ├── *.pdf                    # Student submission PDF
│   │   ├── repo_assessment.md       # 22 criteria assessment
│   │   └── submission_info.xlsx     # Metadata
│   └── ... (36 students)
│
├── WorkSubmissions02/                # 📁 Assignment 2 submissions
├── WorkSubmissions03/                # 📁 Assignment 3 submissions
│
├── grading_temp/                     # 🗑️ Temporary grading files
│   ├── README.md                     # Explains contents
│   ├── analyze_submissions.py
│   ├── calculate_grades.py
│   └── ... (deprecated scripts)
│
├── assessments_tier2/                # 📊 Tier 2 assessments
│   ├── README.md                     # Explains contents
│   ├── tier2_assessment_38950.json  # ✅ Orchestrator output
│   └── assessment_*.txt             # Deprecated manual assessments
│
├── grades_hw1.xlsx                   # ⭐ MASTER GRADE FILE
│
└── temp_lstm_assessment/             # Temp project folder

```

---

## Key Files

### Essential Files ⭐

1. **`grades_hw1.xlsx`**
   - Master grade sheet for Assignment 1
   - Columns: ID, Group, Students, GitHub, Self-Grade, TRUE Count, Final Grade, Tier

2. **`.claude/skills/tier2-orchestrator/skill.md`**
   - Claude agent that runs all 10 skill assessments automatically
   - Usage: `/skill tier2-orchestrator` then provide: `<repo_path> <student_id> <self_grade> <true_count>`

3. **`docs/CLAUDE_GRADING_PROCESS.md`**
   - Step-by-step grading process for Claude

4. **`docs/CRITICAL_INDIVIDUAL_ASSESSMENT.md`**
   - Why individual assessment is mandatory

### Documentation 📚

All documentation is in `docs/`:
- Planning documents (PRD, CLAUDE, PLANNING, TASKS)
- Implementation guides
- Workflow instructions
- Critical rules

### Assessment Skills 🎯

All 10 skills are in `.claude/skills/`:
- Each has a `SKILL.md` with validation commands
- Orchestrator runs them automatically

---

## Cleanup Summary

### Removed:
- ❌ Old progress tracking files (outdated)
- ❌ Temporary assessment scripts (deprecated)
- ❌ Old JSON data files (superseded)
- ❌ Temporary assessment directories

### Organized:
- ✅ Temporary scripts → `grading_temp/`
- ✅ Tier 2 assessments → `assessments_tier2/`
- ✅ Documentation → `docs/`

---

## Current Status

### Assignment 1 (WorkSubmissions01):
- **Total students:** 36
- **Tier 1 (31 students):** ✅ Graded with simple formula
- **Tier 2 (5 students):**
  - Student 38950: ✅ Assessed with orchestrator (39/100)
  - Students 38951-38954: ⏳ Pending orchestrator assessment

### Next Steps:
1. Run orchestrator on remaining 4 Tier 2 students
2. Update Excel with actual grades
3. Generate Report2 PDFs for all students

---

## Usage

### To grade Tier 2 student:
```bash
# 1. Clone repository
git clone <github-url> temp_assessment_<id>

# 2. Run orchestrator agent
/skill tier2-orchestrator
# Then provide: temp_assessment_<id> <id> <self_grade> <true_count>

# 3. Clean up
rm -rf temp_assessment_<id>
```

### To view grades:
```bash
# Open Excel file
grades_hw1.xlsx
```

---

**Last Updated:** 2025-12-01
**Status:** Clean and organized ✨

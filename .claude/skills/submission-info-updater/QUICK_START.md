# Submission Info Updater - Quick Start

## TL;DR - One Command to Rule Them All

```bash
cd "C:\Users\Guest1\CoOp\Runi"
python .claude/skills/submission-info-updater/run_all.py
```

**Done!** This processes all 97 students across all three assignments.

---

## What Just Happened?

✅ **Assignment 1:** 36 students processed, 36 grades extracted (100%)
✅ **Assignment 2:** 26 students processed, 23 grades extracted (88.5%)
✅ **Assignment 3:** 35 students processed, 35 grades extracted (100%)

**Overall:** 94/97 grades extracted (96.9% success rate)

---

## View Results

### Summary Report
```bash
python .claude/skills/submission-info-updater/generate_summary.py
```

### JSON Reports
- `submission_grades_report_hw1.json` - Assignment 1 details
- `submission_grades_report_hw2.json` - Assignment 2 details
- `submission_grades_report_hw3.json` - Assignment 3 details

### Check Individual Excel Files
```bash
# Example: Check student 38950
python -c "import pandas as pd; df = pd.read_excel('WorkSubmissions01/Participant_38950_assignsubmission_file/submission_info.xlsx'); print(df[df['Field']=='Suggested Grade'])"
```

---

## Manual Review (3 students)

Only 3 students need manual review (all in Assignment 2):

1. **Student 48951** - Open their PDF and add grade manually
2. **Student 48970** - Open their PDF and add grade manually
3. **Student 48975** - Open their PDF and add grade manually

To update manually:
1. Open `WorkSubmissionsXX/Participant_XXXXX_assignsubmission_file/submission_info.xlsx`
2. Find row with "Suggested Grade" in column A
3. Enter grade in column B (Value column)
4. Save

---

## Next Steps in Grading Workflow

Now that all `submission_info.xlsx` files have self-grades:

### 1. Determine Tiers
- **Tier 2** (self-grade ≥ 80): Run 10-skill orchestrator
- **Tier 1** (self-grade < 80): Simple TRUE count grading

### 2. Run Tier 2 Assessments
```bash
# For each Tier 2 student
python .claude/skills/tier2-orchestrator/orchestrate.py \
  "WorkSubmissions01/Participant_XXXXX_assignsubmission_file/repo" \
  XXXXX \
  "Assignment 1"
```

### 3. Generate Student Reports
After grading, use:
- `grader-pdf` skill for detailed breakdowns
- `grade-report-generator` skill for student-facing PDFs

---

## Files Created

```
C:\Users\Guest1\CoOp\Runi\
├── submission_grades_report_hw1.json      ← Assignment 1 report
├── submission_grades_report_hw2.json      ← Assignment 2 report
├── submission_grades_report_hw3.json      ← Assignment 3 report
└── WorkSubmissionsXX/
    └── Participant_XXXXX_assignsubmission_file/
        └── submission_info.xlsx           ← Updated with self-grade ✅
```

---

## Troubleshooting

### "No module named 'pandas'"
```bash
pip install pandas openpyxl PyPDF2
```

### Want to re-run just one assignment?
```bash
# Assignment 1 only
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "WorkSubmissions01" \
  --assignment-name "Assignment 1" \
  --output-report "submission_grades_report_hw1.json"
```

### Need to check a specific student?
```bash
python .claude/skills/submission-info-updater/extract_self_grade.py \
  "WorkSubmissions01/Participant_38950_assignsubmission_file"
```

---

## Success Metrics

- ✅ 97 students processed
- ✅ 94 grades extracted automatically
- ✅ 96.9% success rate
- ✅ Only 3 manual reviews needed
- ✅ All Excel files updated
- ✅ Ready for next grading phase

**Status: COMPLETE** 🎯

---

## Help

For detailed documentation, see:
- `README.md` - Full documentation
- `USAGE_GUIDE.md` - Detailed usage examples
- `REFACTOR_SUMMARY.md` - Technical improvements
- `SKILL.md` - Skill definition

---

**Last Updated:** December 4, 2025
**Version:** 1.1.0 (Refactored)

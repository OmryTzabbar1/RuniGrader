# Submission Info Updater - Usage Guide

## Quick Start

### Process All Three Assignments

```bash
cd "C:\Users\Guest1\CoOp\Runi"
python .claude/skills/submission-info-updater/run_all.py
```

This will process WorkSubmissions01, WorkSubmissions02, and WorkSubmissions03 automatically.

### Process Single Assignment

```bash
cd "C:\Users\Guest1\CoOp\Runi"

# Assignment 1
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "WorkSubmissions01" \
  --assignment-name "Assignment 1" \
  --output-report "submission_grades_report_hw1.json"

# Assignment 2
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "WorkSubmissions02" \
  --assignment-name "Assignment 2" \
  --output-report "submission_grades_report_hw2.json"

# Assignment 3
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "WorkSubmissions03" \
  --assignment-name "Assignment 3" \
  --output-report "submission_grades_report_hw3.json"
```

### Process Single Student

```bash
python .claude/skills/submission-info-updater/extract_self_grade.py \
  "WorkSubmissions01/Participant_38950_assignsubmission_file"
```

## What It Does

1. **Finds submission PDFs** - Searches each student folder for their original submission PDF
2. **Extracts self-grade** - Uses pattern matching to find the grade they claimed (60-100)
3. **Updates Excel** - Writes the grade to `submission_info.xlsx` in their folder
4. **Generates report** - Creates JSON report with success/failure details

## Supported Grade Formats

The extractor recognizes multiple formats:

### English Formats
- "Grade suggestion: 100"
- "Suggested grade: 95"
- "Self-grade: 90"
- "Grade: 85"
- Item 5 or 6 in numbered lists

### Hebrew Formats
- "ציון: 100" (grade: 100)
- "הצעת ציון: 95" (suggested grade: 95)
- "ציון עצמי: 90" (self grade: 90)
- "עצמי93" (self93 - no space)

## Expected Results

### Assignment 1 (30/11/2025 submissions)
- **Total students:** 36
- **Success rate:** ~92% (33/36)
- **Manual review:** 3 students with non-standard formats

### Grade Distribution (Assignment 1)
```
100: 13 students (36%)
 95:  8 students (22%)
 92:  3 students (8%)
 96:  2 students (6%)
 93:  2 students (6%)
 79:  2 students (6%)
 60:  2 students (6%)
 90:  1 student  (3%)
```

## After Processing

### 1. Review the JSON Report

Check `submission_grades_report_hwX.json` for:
- Success rate
- Grade distribution
- Students needing manual review

### 2. Handle Manual Reviews

For students who failed extraction:
1. Open their submission PDF manually
2. Find their self-grade
3. Update `submission_info.xlsx` by hand

Example students needing manual review (Assignment 1):
- 38954: Non-standard PDF format
- 38955: Grade in unusual location
- 38964: Different submission structure

### 3. Verify Excel Files

Spot-check a few `submission_info.xlsx` files to ensure grades were updated:

```bash
# Check a few students
python -c "import pandas as pd; df = pd.read_excel('WorkSubmissions01/Participant_38950_assignsubmission_file/submission_info.xlsx'); print(df[df['Field']=='Suggested Grade'])"
```

## Troubleshooting

### "No submission PDF found"
**Solution:** Check if student submitted in different format (Word, text)

### "Could not find grade in PDF text"
**Solutions:**
1. Open PDF and check format manually
2. Look at report's "notes" field for extracted text preview
3. Add student to manual review list

### Excel file locked
**Solution:** Close Excel if you have submission_info.xlsx files open

### Unicode errors
**Solution:** The scripts handle this internally, but if you see errors, the grade may still be extracted correctly

## Integration with Grading Workflow

After running this skill:

1. ✅ All `submission_info.xlsx` files updated with self-grades
2. ✅ Ready to run tier2-orchestrator for Tier 2 students (self-grade ≥80)
3. ✅ Ready to run simple grading for Tier 1 students (self-grade <80)

## Files Created

```
C:\Users\Guest1\CoOp\Runi\
├── submission_grades_report_hw1.json      # Assignment 1 report
├── submission_grades_report_hw2.json      # Assignment 2 report
├── submission_grades_report_hw3.json      # Assignment 3 report
└── WorkSubmissionsXX/
    └── Participant_XXXXX_assignsubmission_file/
        └── submission_info.xlsx           # Updated with self-grade
```

## Tips

1. **Run before grading** - This should be your first step before running assessments
2. **Check distribution** - Grade distribution should be mostly 80-100 for good students
3. **Manual review is OK** - 90%+ success rate is good, manual review the rest
4. **Keep reports** - JSON reports are useful for tracking which students were processed

## Example Session

```bash
# Navigate to project
cd "C:\Users\Guest1\CoOp\Runi"

# Process Assignment 1
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "WorkSubmissions01" \
  --assignment-name "Assignment 1" \
  --output-report "submission_grades_report_hw1.json"

# Check results
python -c "import json; d=json.load(open('submission_grades_report_hw1.json')); print(f'Success: {d[\"success_rate\"]}')"

# Output: Success: 91.7%

# Review manual cases
python -c "import json; d=json.load(open('submission_grades_report_hw1.json')); [print(f'{s[\"participant_id\"]}: {s[\"reason\"]}') for s in d['needs_manual_review']]"

# Output:
# 38954: Could not find grade in PDF text
# 38955: Could not find grade in PDF text
# 38964: Could not find grade in PDF text
```

## Next Steps

After successfully extracting all self-grades:

1. Update master grading spreadsheet if needed
2. Run tier2-orchestrator on high self-graders (≥80)
3. Run simple grading on low self-graders (<80)
4. Generate final student reports

---

**Version:** 1.0.0
**Date:** December 2025
**Tested on:** 30/11/2025 submissions

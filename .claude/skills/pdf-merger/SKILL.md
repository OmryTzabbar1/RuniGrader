# PDF Merger Skill

## Overview

Merge student submission PDFs with their grade report PDFs into single combined files for complete student packages.

## Purpose

After grading is complete and PDF reports are generated, this skill creates consolidated PDFs containing:
1. Student's original submission (first)
2. Grade report with feedback (second)

This simplifies archival, distribution, and review by keeping everything in one file per student.

## Rubric

This is a utility skill (not graded). It processes existing PDFs to create combined versions.

## Success Criteria

**Complete (Pass):**
- ✅ All students with both PDFs have combined versions
- ✅ Combined PDFs are in correct order (submission first, report second)
- ✅ File naming follows convention: `Student_{ID}_Complete_Submission.pdf`
- ✅ Summary report generated with statistics

**Partial (Warning):**
- ⚠️ Some students missing submission or grade report PDFs
- ⚠️ PDF corruption issues for specific files
- Summary reports all successes and failures

**Fail:**
- ❌ Cannot access submissions directory
- ❌ PyPDF2 not installed
- ❌ No PDFs found to merge

## Input Requirements

### Directory Structure
```
WorkSubmissions01/
├── Participant_{ID}_assignsubmission_file/
│   ├── {submission}.pdf                    # Student's original work
│   └── Student_Grade_Report_{ID}.pdf       # Generated feedback
```

### Required Files Per Student
1. **Submission PDF** - Any `.pdf` file except the grade report
2. **Grade Report PDF** - Must match pattern `Student_Grade_Report_{ID}.pdf`

## Output Format

### Combined PDF
- **Filename:** `Student_{ID}_Complete_Submission.pdf`
- **Location:** Same directory as original PDFs (default)
- **Content Order:**
  1. Submission PDF pages (student's work)
  2. Grade Report PDF pages (instructor feedback)

### Summary Report
```
+==================================================+
|  PDF MERGE SUMMARY                               |
+==================================================+

Students Processed: 36
Successful Merges: 36 (100.0%)
Failed Merges: 0 (0.0%)

Output Location: Same directory as originals

Successful:
  [OK] Student 38950: 2 pages + 3 pages = 5 pages
  [OK] Student 38951: 5 pages + 3 pages = 8 pages
  ...
+==================================================+
```

## Example Invocation

### Claude CLI Skill
```
/pdf-merger
```

### Standalone Script
```bash
# Merge all students
python .claude/skills/pdf-merger/merge_pdfs.py --submissions WorkSubmissions01

# Merge specific student
python .claude/skills/pdf-merger/merge_pdfs.py --submissions WorkSubmissions01 --student-id 38950

# Save to different directory
python .claude/skills/pdf-merger/merge_pdfs.py --submissions WorkSubmissions01 --output-dir ./merged_pdfs
```

## Error Handling

| Issue | Behavior | Status |
|-------|----------|--------|
| Missing submission PDF | Skip student, log warning | Continue |
| Missing grade report | Skip student, log warning | Continue |
| Corrupted PDF | Skip student, log error | Continue |
| File already exists | Ask user: Overwrite/Skip/Rename | Pause |
| No PyPDF2 | Exit with error | Stop |

## Dependencies

```bash
pip install PyPDF2
```

## Performance

- **Speed:** ~1 second per student
- **Batch:** 36 students in ~36 seconds
- **Memory:** Minimal (processes one at a time)

## Integration Points

### In Grading Workflow
```
1. Run Tier 2 Assessments → Base Grades
2. Generate PDF Reports → Individual Feedback
3. Calculate Weighted Grades → Final Scores
4. Merge PDFs → Complete Packages ◄── THIS SKILL
```

### Use Cases
1. **Archival** - Store complete student packages
2. **Distribution** - Send students their work + feedback in one file
3. **Review** - Quickly review multiple students
4. **Records** - Department record keeping

## Testing

### Test Single Student
```bash
python .claude/skills/pdf-merger/merge_pdfs.py \
  --submissions WorkSubmissions01 \
  --student-id 38950
```

**Expected Result:**
- Creates `Student_38950_Complete_Submission.pdf`
- Shows page count for submission + report
- Reports success

### Test All Students
```bash
python .claude/skills/pdf-merger/merge_pdfs.py \
  --submissions WorkSubmissions01
```

**Expected Result:**
- Processes all students with both PDFs
- Skips students missing either PDF
- Generates complete summary report

## Notes

- **PDF Order Critical:** Submission must be first, report second
- **Preserves Originals:** Original PDFs are NOT deleted
- **Idempotent:** Can be run multiple times (will ask about overwriting)
- **Fail-Safe:** Continues even if some students fail

## Version

- **Version:** 1.0.0
- **Last Updated:** December 2025
- **Status:** Production Ready ✓

---

**See Also:**
- [README.md](./README.md) - Detailed usage guide
- [prompt.md](./prompt.md) - Claude CLI skill instructions
- [merge_pdfs.py](./merge_pdfs.py) - Standalone Python script

# Submission Info Updater Skill

Thoroughly extracts self-submitted grades from student PDFs and updates `submission_info.xlsx` files across all WorkSubmissions folders.

## Purpose

Students submit their assignments with a self-assessed grade (typically 60-100). This grade is embedded in their submission PDF in various formats. This skill:

1. Finds each student's original submission PDF
2. Extracts their self-submitted grade using intelligent pattern matching
3. Updates their `submission_info.xlsx` file with the extracted grade
4. Generates a comprehensive report of successes and failures

## Features

### Intelligent PDF Discovery

- Searches recursively through student folders
- Prioritizes PDFs by name patterns:
  1. `hw1*.pdf`
  2. `submission_form.pdf`
  3. `submission.pdf`
  4. Hebrew filenames (הגשת מטלה)
  5. Any other PDFs
- Excludes generated PDFs (grade reports, breakdowns)
- Handles PDFs in subdirectories

### Robust Grade Extraction

Uses multiple extraction strategies:

1. **Explicit patterns:**
   - "Grade suggestion: 100"
   - "Suggested grade: 95"
   - "Self-grade: 90"
   - "Grade: 85"

2. **Hebrew patterns:**
   - "ציון: 100" (grade)
   - "הצעת ציון: 95" (grade suggestion)

3. **Contextual extraction:**
   - Item 5 or 6 in numbered lists
   - Numbers near grade-related keywords

4. **Validation:**
   - Ensures grade is in valid range (60-100)
   - Rejects student IDs and other numbers

### Safe Excel Updates

- Reads existing `submission_info.xlsx`
- Updates "Suggested Grade" field
- Creates timestamped backups (optional)
- Preserves all other fields

## Usage

### Process Single Student

```bash
python .claude/skills/submission-info-updater/extract_self_grade.py \
  "C:\Users\Guest1\CoOp\Runi\WorkSubmissions01\Participant_38950_assignsubmission_file"
```

**Output:**
```
============================================================
Participant ID: 38950
PDF Found: hw1 llms agents.pdf
Self-Grade: 100
Excel Updated: True

Notes:
  - Found PDF: hw1 llms agents.pdf
  - Extracted 523 characters of text
  - Extracted grade: 100
  - Successfully updated submission_info.xlsx
============================================================
```

### Process Entire Assignment

```bash
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions01" \
  --assignment-name "Assignment 1" \
  --output-report "C:\Users\Guest1\CoOp\Runi\StudentGradesForRami\submission_grades_report_hw1.json"
```

**Output:**
```
================================================================================
Processing Assignment 1
Found 36 student folders
================================================================================

[1/36] Processing Participant_38950_assignsubmission_file...
  ✓ Grade: 100, Updated: True
[2/36] Processing Participant_38951_assignsubmission_file...
  ✓ Grade: 95, Updated: True
...
[36/36] Processing Participant_59378_assignsubmission_file...
  ✓ Grade: 85, Updated: True

================================================================================

PROCESSING SUMMARY:
  Total Students: 36
  Grades Found: 34
  Grades Missing: 2
  Excel Updated: 34
  Errors: 2
  Success Rate: 94.4%

================================================================================

✓ Report saved to: submission_grades_report_hw1.json

⚠ STUDENTS NEEDING MANUAL REVIEW (2):
  - Participant 38999: No submission PDF found
  - Participant 39000: Could not find grade in PDF text
```

### Process All Assignments

```bash
# Assignment 1
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions01" \
  --assignment-name "Assignment 1" \
  --output-report "C:\Users\Guest1\CoOp\Runi\StudentGradesForRami\submission_grades_report_hw1.json"

# Assignment 2
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions02" \
  --assignment-name "Assignment 2" \
  --output-report "C:\Users\Guest1\CoOp\Runi\StudentGradesForRami\submission_grades_report_hw2.json"

# Assignment 3
python .claude/skills/submission-info-updater/process_assignment.py \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions03" \
  --assignment-name "Assignment 3" \
  --output-report "C:\Users\Guest1\CoOp\Runi\StudentGradesForRami\submission_grades_report_hw3.json"
```

## Report Format

The JSON report includes:

```json
{
  "skill": "submission-info-updater",
  "assignment": "Assignment 1",
  "assignment_dir": "C:\\Users\\Guest1\\CoOp\\Runi\\WorkSubmissions01",
  "processed_date": "2025-12-04T10:30:00",
  "total_students": 36,
  "grades_found": 34,
  "grades_missing": 2,
  "excel_updated": 34,
  "errors": 2,
  "success_rate": "94.4%",
  "students_processed": [
    {
      "participant_id": "38950",
      "folder": "...",
      "pdf_found": "hw1 llms agents.pdf",
      "self_grade_extracted": 100,
      "excel_updated": true,
      "notes": ["Successfully extracted from page 1"]
    }
  ],
  "failed_extractions": [
    {
      "participant_id": "38999",
      "error": "No submission PDF found",
      "excel_updated": false
    }
  ],
  "grade_distribution": {
    "100": 12,
    "95": 8,
    "90": 6,
    "85": 4,
    "80": 3,
    "75": 1
  },
  "needs_manual_review": [
    {
      "participant_id": "38999",
      "reason": "No submission PDF found",
      "folder": "..."
    }
  ]
}
```

## Edge Cases Handled

### Multiple PDFs in Folder

**Scenario:** Student has `submission.pdf`, `documentation.pdf`, `hw1.pdf`

**Solution:** Prioritizes by pattern matching:
1. `hw1.pdf` (matches hw1 pattern)
2. `submission.pdf` (matches submission pattern)
3. Others ignored unless no priority PDFs found

### No Explicit "Grade" Keyword

**Scenario:** Student writes "5. 100" without the word "grade"

**Solution:** Contextual extraction looks for numbers in typical positions (items 5-6 in lists)

### PDF in Subdirectory

**Scenario:** Student puts `submission.pdf` inside `repo/docs/submission.pdf`

**Solution:** Recursive search finds all PDFs, prioritizes root folder but falls back to subdirectories

### Unicode/Hebrew Filenames

**Scenario:** PDF named `הגשת מטלה 1.pdf`

**Solution:** UTF-8 encoding handles Hebrew text correctly

### Grade Outside Valid Range

**Scenario:** Student writes "Grade: 105" or "Grade: 40"

**Solution:** Validation rejects grades <60 or >100, flags for manual review

### No PDF Found

**Scenario:** Student submitted .docx or .txt instead of PDF

**Solution:** Reports "No submission PDF found", adds to manual review list

## Common Grade Patterns Found

Based on analysis of student submissions:

1. **Numbered list format:**
   ```
   1. Group code: xyz
   2. Student one: John Doe
   3. Student two: Jane Smith
   4. Repo link: https://...
   5. Grade suggestion: 100
   ```

2. **Key-value format:**
   ```
   Grade: 95
   Repository: https://...
   ```

3. **Form-style:**
   ```
   Suggested Grade: 90
   ```

4. **Hebrew format:**
   ```
   ציון מוצע: 95
   ```

## Troubleshooting

### Script Can't Find PDF

**Problem:** "No submission PDF found"

**Solutions:**
1. Check if student submitted in different format (.docx, .txt)
2. Verify PDF isn't in a deeply nested subdirectory
3. Check if PDF name is unusual (check folder manually)

### Grade Extraction Fails

**Problem:** "Could not find grade in PDF text"

**Solutions:**
1. Open PDF manually and check format
2. Look at `notes` in report to see extracted text preview
3. Add new pattern to `GRADE_PATTERNS` in `extract_self_grade.py`

### Excel Update Fails

**Problem:** "Excel updated: False"

**Solutions:**
1. Check if `submission_info.xlsx` exists
2. Verify Excel file isn't open in another program
3. Check file permissions

### Low Success Rate (<80%)

**Problem:** Many students failing extraction

**Solutions:**
1. Review failed extractions in JSON report
2. Look for common patterns in failures
3. Update extraction patterns accordingly
4. Consider manual review for unusual formats

## Dependencies

```bash
pip install pandas openpyxl PyPDF2
```

- **pandas**: Excel file reading/writing
- **openpyxl**: Excel file format support
- **PyPDF2**: PDF text extraction

## File Structure

```
.claude/skills/submission-info-updater/
├── SKILL.md                    # Skill definition
├── README.md                   # This file
├── extract_self_grade.py       # Single student processor
└── process_assignment.py       # Batch assignment processor
```

## Integration with Grading Workflow

This skill is typically used at the beginning of the grading process:

1. **Extract self-grades** (this skill)
   - Ensures all `submission_info.xlsx` files have correct self-grades
   - Generates report of students needing manual review

2. **Determine tiers**
   - Self-grade ≥80 → Tier 2 (rigorous assessment)
   - Self-grade <80 → Tier 1 (simple grading)

3. **Run assessments**
   - Tier 2: Run orchestrator with 10 skills
   - Tier 1: Simple TRUE count from markdown

4. **Generate reports**
   - Create student-facing PDFs
   - Update master gradebook

## Best Practices

1. **Run on clean data:** Delete backup files first (done)
2. **Review report:** Check success rate and manual review list
3. **Validate distribution:** Grade distribution should be mostly 80-100
4. **Manual review:** Always review failed extractions manually
5. **Backup first:** Keep original submission_info.xlsx if concerned

## Version History

- **v1.0.0** (2025-12-04)
  - Initial release
  - Multi-pattern grade extraction
  - Hebrew language support
  - Comprehensive reporting
  - Batch processing capability

## Notes

- Designed for 30/11/2025 submissions
- Handles both English and Hebrew content
- Safe updates with validation
- Generates detailed reports for auditing
- Prioritizes accuracy over speed

---

**Created:** December 2025
**Purpose:** Automated self-grade extraction from student PDFs

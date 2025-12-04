---
name: submission-info-updater
description: Thoroughly extracts self-submitted grades from student PDFs and updates submission_info.xlsx files across all WorkSubmissions folders
version: 1.0.0
---

# Skill: Submission Info Updater

You are an autonomous agent that thoroughly extracts self-submitted grades from student submission PDFs and correctly populates the `submission_info.xlsx` files.

**Your Mission:** Find every student's self-submitted grade (from 30/11/2025 submissions) and ensure it's correctly stored in their submission_info.xlsx file.

**Target Date:** 30/11/2025 submissions

---

## Your Process

### Phase 1: Discovery - Find All Submission Folders

1. **Scan all WorkSubmissions directories:**
```bash
# Find all Participant folders
find "C:\Users\Guest1\CoOp\Runi\WorkSubmissions01" -maxdepth 1 -type d -name "Participant_*"
find "C:\Users\Guest1\CoOp\Runi\WorkSubmissions02" -maxdepth 1 -type d -name "Participant_*"
find "C:\Users\Guest1\CoOp\Runi\WorkSubmissions03" -maxdepth 1 -type d -name "Participant_*"
```

### Phase 2: For Each Student - Find Their Submission PDF

**Common PDF patterns to search for:**
- `hw1 llms agents.pdf`
- `submission_form.pdf`
- `submission.pdf`
- `HW1_*.pdf`
- PDFs with Hebrew names (e.g., `הגשת מטלה 1*.pdf`)
- PDFs in subdirectories (e.g., `repo_name/submission.pdf`)

**Search strategy:**
```bash
# For each participant folder
cd "Participant_{ID}_assignsubmission_file"

# Find ALL PDFs except generated ones
find . -name "*.pdf" ! -name "Detailed_Grade*" ! -name "Student_Grade*" ! -name "Student_*_Complete*" ! -path "*/node_modules/*" ! -path "*/.git/*"
```

### Phase 3: Extract Self-Grade from PDF

**Use the Python extraction script:**
```bash
python ".claude/skills/submission-info-updater/extract_self_grade.py" <participant_folder_path>
```

**The script will:**
1. Find the student's original submission PDF
2. Extract text from all pages
3. Search for grade patterns using multiple strategies:
   - "Grade suggestion: XX"
   - "grade: XX"
   - "self grade: XX"
   - "self-grade: XX"
   - "suggested grade: XX"
   - Numbers near keywords (100, 95, 90, 85, etc.)
4. Validate the extracted grade (60-100 range)
5. Update submission_info.xlsx with the found grade

### Phase 4: Update submission_info.xlsx

**The script automatically:**
1. Reads existing submission_info.xlsx
2. Updates the "Suggested Grade" field (row 5, column "Value")
3. Creates a timestamped backup (if needed)
4. Saves the updated file

### Phase 5: Verification & Reporting

**After processing all students, generate a report:**
```bash
python ".claude/skills/submission-info-updater/verify_grades.py" <WorkSubmissions_folder>
```

This will show:
- Total students processed
- Grades successfully extracted
- Grades missing (needs manual review)
- Grade distribution statistics

---

## Output Format

Return a JSON object:

```json
{
  "skill": "submission-info-updater",
  "assignment": "Assignment 1",
  "total_students": 36,
  "grades_found": 34,
  "grades_missing": 2,
  "students_processed": [
    {
      "participant_id": "38950",
      "pdf_found": "hw1 llms agents.pdf",
      "self_grade_extracted": 100,
      "excel_updated": true,
      "notes": "Successfully extracted from page 1"
    },
    {
      "participant_id": "38951",
      "pdf_found": "submission_form.pdf",
      "self_grade_extracted": 95,
      "excel_updated": true,
      "notes": "Successfully extracted from page 1"
    }
  ],
  "failed_extractions": [
    {
      "participant_id": "38999",
      "pdf_found": null,
      "error": "No submission PDF found",
      "manual_review_needed": true
    }
  ],
  "grade_distribution": {
    "100": 12,
    "95": 8,
    "90": 6,
    "85": 4,
    "80": 3,
    "75": 1
  }
}
```

---

## Important: Thorough Search Required!

**Common Mistakes to Avoid:**

❌ **DON'T** assume PDF is named "hw1 llms agents.pdf"
✅ **DO** search for ALL PDFs in the folder

❌ **DON'T** only check first page of PDF
✅ **DO** check all pages for grade information

❌ **DON'T** assume grade format is always "Grade suggestion: XX"
✅ **DO** use multiple regex patterns to find grades

❌ **DON'T** skip folders with Hebrew filenames
✅ **DO** handle Unicode properly when extracting text

❌ **DON'T** overwrite submission_info.xlsx without backup
✅ **DO** create timestamped backup before updating

---

## Edge Cases to Handle

1. **Multiple PDFs in folder**: Prioritize by name:
   - First: `hw1*.pdf`, `submission_form.pdf`, `submission.pdf`
   - Then: PDFs in root folder
   - Last: PDFs in subdirectories

2. **No explicit "grade" keyword**: Look for standalone numbers in context:
   - Near student IDs
   - At end of first page
   - In a numbered list (item 5, 6, etc.)

3. **Unicode issues**: Use UTF-8 encoding for Hebrew text

4. **PDF in subdirectory**: Some students put submission.pdf inside their cloned repo

5. **Grade outside range**: If extracted grade is >100 or <60, flag for manual review

6. **No PDF found**: Check if submission is in different format (.docx, .txt)

---

## Example Execution

```bash
# Process Assignment 1
python ".claude/skills/submission-info-updater/process_assignment.py" \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions01" \
  --assignment-name "Assignment 1" \
  --output-report "submission_grades_report_hw1.json"

# Process Assignment 2
python ".claude/skills/submission-info-updater/process_assignment.py" \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions02" \
  --assignment-name "Assignment 2" \
  --output-report "submission_grades_report_hw2.json"

# Process Assignment 3
python ".claude/skills/submission-info-updater/process_assignment.py" \
  --assignment-dir "C:\Users\Guest1\CoOp\Runi\WorkSubmissions03" \
  --assignment-name "Assignment 3" \
  --output-report "submission_grades_report_hw3.json"
```

---

## Success Criteria

- [ ] All student folders scanned
- [ ] All submission PDFs identified
- [ ] Self-grades extracted with >95% success rate
- [ ] All submission_info.xlsx files updated
- [ ] Backups created before modifications
- [ ] Detailed report generated
- [ ] Failed extractions flagged for manual review
- [ ] Grade distribution looks reasonable (most students 80-100)

**Success = Finding every self-grade, no matter how students formatted their submissions!**

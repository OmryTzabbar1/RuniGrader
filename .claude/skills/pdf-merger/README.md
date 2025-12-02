# PDF Merger Skill

Merge student submission PDFs with their grade report PDFs into single combined files for easy archival and distribution.

## Quick Start

### Using the Claude CLI Skill

Invoke the skill in Claude Code:

```
/pdf-merger
```

Claude will interactively ask you for:
1. Path to the submissions directory
2. Whether to process all students or a specific student
3. Where to save the combined PDFs

The skill will then:
- Find each student's submission PDF and grade report PDF
- Merge them in the correct order (submission first, grade report second)
- Save as `Student_{ID}_Complete_Submission.pdf`
- Generate a comprehensive summary report

## How It Works

### Input Files

For each student in the submissions directory, the skill looks for:

1. **Submission PDF** - The student's original work
   - Any `.pdf` file that is NOT a grade report
   - Examples: "hw1 llms agents.pdf", "assignment.pdf", "project.pdf"

2. **Grade Report PDF** - The generated feedback
   - Pattern: `Student_Grade_Report_{student_id}.pdf`
   - Example: `Student_Grade_Report_38950.pdf`

### Output Files

**Combined PDF naming:**
```
Student_{ID}_Complete_Submission.pdf
```

**Examples:**
- `Student_38950_Complete_Submission.pdf`
- `Student_38981_Complete_Submission.pdf`

### PDF Order

**IMPORTANT:** PDFs are merged in this order:
1. **Submission PDF** (pages 1-N) - Student's original work comes first
2. **Grade Report PDF** (pages N+1 onwards) - Instructor feedback comes second

This ensures readers see the student's work before seeing the grade.

## Example Usage

### Merge All Students

```
/pdf-merger
```

**Claude will ask:**
- "Where is the submissions directory?"
  - Answer: `C:\Users\Guest1\CoOp\Runi\WorkSubmissions01`

- "Should I process all students or a specific student ID?"
  - Answer: `All students`

- "Where should I save the combined PDFs?"
  - Answer: `Same directory` (saves in each student's folder)

**Expected Output:**
```
+==================================================+
|  PDF MERGE SUMMARY                               |
+==================================================+

Students Processed: 46
Successful Merges: 44 (95.7%)
Failed Merges: 2 (4.3%)

Output Location: Same directory as originals

Successful:
  [OK] Student 38950: 2 pages + 3 pages = 5 pages total
  [OK] Student 38951: 5 pages + 3 pages = 8 pages total
  [OK] Student 38952: 3 pages + 3 pages = 6 pages total
  ...

Failed:
  [FAIL] Student 38961: Missing submission PDF
  [FAIL] Student 38962: Grade report PDF corrupted

+==================================================+
```

## What Gets Created

### Before

```
WorkSubmissions01/
├── Participant_38950_assignsubmission_file/
│   ├── hw1 llms agents.pdf              (2 pages - student work)
│   └── Student_Grade_Report_38950.pdf   (3 pages - feedback)
```

### After

```
WorkSubmissions01/
├── Participant_38950_assignsubmission_file/
│   ├── hw1 llms agents.pdf                       (2 pages - original)
│   ├── Student_Grade_Report_38950.pdf            (3 pages - original)
│   └── Student_38950_Complete_Submission.pdf     (5 pages - combined!) ✓
```

## Error Handling

The skill handles common issues gracefully:

### Missing Submission PDF
```
[WARN] Student 38961: No submission PDF found
→ Skipping student 38961
```

### Missing Grade Report
```
[WARN] Student 38962: No grade report PDF found
→ Skipping student 38962
```

### Corrupted PDF
```
[ERROR] Student 38963: Cannot read PDF (file corrupted)
→ Skipping student 38963
```

### File Already Exists
```
[WARN] Student 38950: Combined PDF already exists
→ Options: [Overwrite] [Skip] [Rename with timestamp]
```

## Use Cases

### 1. Archive Complete Student Packages
Create one PDF per student containing both their work and feedback for long-term archival.

### 2. Distribute to Students
Send each student a single PDF containing their submission + personalized grade report.

### 3. Department Records
Maintain complete records of student work + evaluation in one convenient file.

### 4. Review Consistency
Quickly review multiple students by opening one file instead of two.

## Technical Details

### Dependencies

```bash
pip install PyPDF2
```

### PDF Merge Process

The skill uses PyPDF2's PdfMerger:

```python
from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append("submission.pdf")  # Student work first
merger.append("grade_report.pdf")  # Feedback second
merger.write("combined.pdf")
merger.close()
```

### File Discovery Logic

1. **Find student directories:**
   ```
   WorkSubmissions01/Participant_*_assignsubmission_file/
   ```

2. **Extract student ID:**
   ```
   Participant_38950_assignsubmission_file → 38950
   ```

3. **Find submission PDF:**
   ```
   Any *.pdf that is NOT "Student_Grade_Report_*.pdf"
   ```

4. **Find grade report:**
   ```
   Student_Grade_Report_{student_id}.pdf
   ```

## Troubleshooting

### Error: "PyPDF2 not installed"

```bash
pip install PyPDF2
```

### Warning: "No submission PDF found"

Student didn't submit a PDF file, or it has an unexpected name. Check the student's folder manually.

### Warning: "No grade report found"

Grade report wasn't generated for this student. Run the grade-report-generator skill first.

### Error: "Cannot merge PDFs"

One of the PDF files may be corrupted or password-protected. Check the individual files.

## Integration with Grading Workflow

```
┌─────────────────────────────────┐
│ 1. Run Tier 2 Assessments      │
│    (10 skills → base grade)     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 2. Generate PDF Reports         │
│    (student-facing feedback)    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 3. Calculate Weighted Grades    │
│    (apply penalty formula)      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 4. Merge PDFs                   │ ◄── THIS SKILL
│    (combine submission + report)│
│    - Creates complete packages  │
│    - One file per student       │
└─────────────────────────────────┘
```

## Performance

- **Speed:** ~1 second per student (depending on PDF sizes)
- **Typical run:** 46 students in ~1 minute
- **Memory:** Minimal (processes one student at a time)

## Version History

- **v1.0.0** - Initial implementation with batch processing support

---

**Created:** December 2025
**Purpose:** Streamline student record keeping and distribution

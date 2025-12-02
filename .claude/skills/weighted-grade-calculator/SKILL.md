---
name: weighted-grade-calculator
description: Calculate weighted grades using exponential self-grading penalty formula
version: 1.0.0
---

# Weighted Grade Calculator Skill

Calculates final weighted grades by applying the exponential self-grading penalty formula to student submissions.

## Purpose

This skill:
1. Extracts self-proclaimed grades from student submission PDFs
2. Calculates base grades from Tier 2 assessments (requirements met)
3. Applies exponential penalty formula for overconfident self-assessments
4. Updates Excel spreadsheet with self-grades and weighted final grades
5. Rewards accurate or humble self-assessment

## Formula Overview

### Three-Step Process:

**Step 1: Calculate Scale Multiplier**
```
scale = 0.086603 × e^(0.027465 × self_grade)
```

**Step 2: Calculate Base Grade**
```
base_grade = (requirements_met / 22) × 100
```

**Step 3: Apply Penalty (Conditional)**
```
if self_grade > base_grade:
    penalty = (self_grade - base_grade) × scale
    final_grade = max(0, base_grade - penalty)
else:
    final_grade = base_grade  # Reward humility
```

## How It Works

### Input Requirements

1. **Student Submission PDFs** containing self-proclaimed grade
   - Located in: `WorkSubmissions01/Participant_*/submission_*.pdf`
   - Self-grade format: "Self-Grade: XX" or "I estimate: XX%" or similar

2. **Tier 2 Assessment Results**
   - Requirements met (0-22 criteria)
   - Base grade from 10-skill assessment

3. **Excel Grading Summary**
   - `Assignment3_Grading_Summary.xlsx`
   - Must have columns: Student ID, Generated Grade, Weighted Grade

### Output

Updates Excel with:
- **Self-Proclaimed Grade** (new column after Student ID)
- **Weighted Grade** (calculated using penalty formula)
- **Penalty Applied** (for transparency)

### Behavior Rules

| Scenario | Self-Grade | Base Grade | Penalty | Final | Reasoning |
|----------|------------|------------|---------|-------|-----------|
| **Accurate** | 82 | 82 | 0 | 82 | Perfect self-awareness ✓ |
| **Humble** | 70 | 85 | 0 | 85 | Underestimated, gets full credit ✓ |
| **Slightly Overconfident** | 90 | 85 | -4.5 | 80.5 | Small penalty ⚠️ |
| **Very Overconfident** | 100 | 82 | -24.3 | 57.7 | Large penalty ❌ |

## Usage

### As a Claude Code Skill

```bash
# Invoke the skill
/weighted-grade-calculator

# The skill will:
# 1. Scan all student PDFs for self-grades
# 2. Calculate weighted grades using formula
# 3. Update Excel spreadsheet
# 4. Generate summary report
```

### Standalone Script

```bash
python .claude/skills/weighted-grade-calculator/calculate_weighted_grades.py \
  --excel "Assignment3_Grading_Summary.xlsx" \
  --submissions "WorkSubmissions01" \
  --output "Assignment3_Grading_Summary_Weighted.xlsx"
```

### Single Student Calculation

```bash
python .claude/skills/weighted-grade-calculator/calculate_single_weighted.py \
  --student-id "38981" \
  --self-grade 95 \
  --requirements-met 21
```

## Edge Cases

### Missing Self-Grade

If student didn't provide self-grade:
- **Default behavior:** Use base grade (no penalty)
- **Alternative:** Prompt for manual entry
- **Flag in Excel:** Mark as "No self-grade provided"

### Self-Grade Out of Range

Valid range: 60-100

- **Below 60:** Raise warning, use 60 as minimum
- **Above 100:** Raise warning, use 100 as maximum
- **Non-numeric:** Flag for manual review

### Perfect Score

If student claims 100 and earned 100:
- No penalty applied
- Weighted grade = 100
- Celebrate accuracy! 🎉

## Excel Column Layout

### Before (Current):
```
| Student ID | Teammate IDs | Team Name | ... | Generated Grade | Weighted Grade | Assessment Date |
```

### After (With Self-Grading):
```
| Student ID | Self-Grade | Teammate IDs | Team Name | ... | Generated Grade | Penalty | Weighted Grade | Assessment Date |
```

**New Columns:**
- **Self-Grade** (column B) - Student's self-proclaimed grade (60-100)
- **Penalty** (column H) - Penalty applied in points (0 or negative)
- **Weighted Grade** (column I) - Final grade after penalty

## Example Calculations

### Example 1: Perfect Self-Assessment
```
Student: 38960
Self-Grade: 89
Requirements Met: 20/22 (90.9%)
Base Grade: 89 (from Tier 2)

Scale = 0.086603 × e^(0.027465 × 89) = 0.98
Difference = 89 - 89 = 0
Penalty = 0 × 0.98 = 0
Weighted Grade = 89 - 0 = 89 ✓
```

### Example 2: Humble Student
```
Student: 38952
Self-Grade: 60 (minimum claim)
Requirements Met: 15/22 (68.2%)
Base Grade: 68

Scale = 0.086603 × e^(0.027465 × 60) = 0.45
Difference = 60 - 68 = -8 (negative!)
Penalty = 0 (no penalty for underestimation)
Weighted Grade = 68 (gets full credit!) ✓
```

### Example 3: Overconfident Student
```
Student: 38964
Self-Grade: 90
Requirements Met: 10/22 (45.5%)
Base Grade: 44

Scale = 0.086603 × e^(0.027465 × 90) = 1.03
Difference = 90 - 44 = 46
Penalty = 46 × 1.03 = 47.4
Weighted Grade = max(0, 44 - 47.4) = 0 ❌ (capped at zero)
```

### Example 4: Slightly Optimistic
```
Student: 38981
Self-Grade: 95
Requirements Met: 21/22 (95.5%)
Base Grade: 94

Scale = 0.086603 × e^(0.027465 × 95) = 1.18
Difference = 95 - 94 = 1
Penalty = 1 × 1.18 = 1.18
Weighted Grade = 94 - 1.18 = 92.82 ⚠️ (minor penalty)
```

## Implementation Notes

### Self-Grade Extraction Methods

**Priority 1: PDF Metadata**
```python
from PyPDF2 import PdfReader

reader = PdfReader("submission.pdf")
metadata = reader.metadata
self_grade = metadata.get('/SelfGrade', None)
```

**Priority 2: Text Search in PDF**
```python
import re

text = extract_text_from_pdf("submission.pdf")
patterns = [
    r"Self[- ]?Grade:?\s*(\d+)",
    r"I estimate:?\s*(\d+)%?",
    r"My grade:?\s*(\d+)",
    r"Self[- ]?assessment:?\s*(\d+)"
]

for pattern in patterns:
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        self_grade = int(match.group(1))
        break
```

**Priority 3: Manual Entry**
```python
# If not found, prompt user
self_grade = input(f"Enter self-grade for Student {student_id} (60-100): ")
```

### Requirements Met Calculation

From Tier 2 assessment (22 criteria):
```python
# Count TRUE values in repo_assessment.md
criteria_met = sum(1 for line in assessment_md if "TRUE" in line)
base_grade = (criteria_met / 22) * 100
```

**Note:** For this implementation, we use the **Generated Grade** from Excel as the base grade (since it's the sum of 10 skills, not 22 criteria). We'll need to convert:

```python
# Convert 10-skill grade (0-100) to 22-criteria equivalent
requirements_met_equivalent = round((generated_grade / 100) * 22)
```

## Constants

```python
SCALE_COEFFICIENT_A = 0.086603
SCALE_EXPONENT_B = 0.027465
TOTAL_REQUIREMENTS = 22
MIN_SELF_GRADE = 60
MAX_SELF_GRADE = 100
```

## Validation

Before calculating weighted grades:
1. ✅ Verify all students have self-grades or defaults
2. ✅ Validate self-grades are in range [60, 100]
3. ✅ Confirm base grades exist in Excel
4. ✅ Check for duplicate student IDs
5. ✅ Backup original Excel file

## Output Report

After processing, generate summary:

```
╔════════════════════════════════════════════════╗
║  WEIGHTED GRADE CALCULATION SUMMARY           ║
╚════════════════════════════════════════════════╝

Students Processed: 46
Self-Grades Found: 42 (91%)
Self-Grades Missing: 4 (9%)

Penalty Statistics:
├─ No Penalty (accurate/humble): 28 (61%)
├─ Small Penalty (1-5 points): 12 (26%)
├─ Medium Penalty (6-15 points): 4 (9%)
└─ Large Penalty (>15 points): 2 (4%)

Average Base Grade: 72.89
Average Weighted Grade: 70.45
Average Penalty: -2.44 points

Top 3 Self-Assessors (most accurate):
1. Student 38960: Self=89, Actual=89, Penalty=0 ✓
2. Student 38981: Self=94, Actual=94, Penalty=0 ✓
3. Student 38982: Self=71, Actual=71, Penalty=0 ✓

Bottom 3 Self-Assessors (most overconfident):
1. Student 38964: Self=90, Actual=44, Penalty=-47.4 ❌
2. Student 38984: Self=85, Actual=55, Penalty=-24.3 ❌
3. Student 38963: Self=80, Actual=55, Penalty=-16.8 ❌

Excel Updated: Assignment3_Grading_Summary.xlsx
Backup Created: Assignment3_Grading_Summary_backup_20251202.xlsx
```

## Success Criteria

- [ ] All students have self-grades (extracted or defaulted)
- [ ] Weighted grades calculated correctly for all students
- [ ] Excel updated with new columns (Self-Grade, Penalty, Weighted Grade)
- [ ] Summary report generated
- [ ] Original Excel backed up before modification
- [ ] No data loss or corruption

## Version History

- **v1.0.0** - Initial implementation with exponential penalty formula

---

**Created:** December 2025
**Purpose:** Add metacognitive assessment layer to grading system

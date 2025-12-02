# Weighted Grade Calculator Skill

Calculate weighted final grades using the exponential self-grading penalty formula that rewards accurate or humble self-assessment and penalizes overconfidence.

## Quick Start

### Using the Claude CLI Skill

Invoke the skill in Claude Code:

```
/weighted-grade-calculator
```

Claude will interactively ask you for:
1. Path to the Excel grading summary file
2. Path to the student submissions directory
3. Whether to create a new file or update the existing one

The skill will then:
- Extract self-grades from student PDFs
- Calculate weighted grades using the exponential penalty formula
- Update the Excel spreadsheet with results
- Generate a comprehensive summary report

## How It Works

### The Formula

**Step 1: Calculate Scale (risk increases with higher claims)**
```
scale = 0.086603 × e^(0.027465 × self_grade)
```

**Step 2: Calculate Penalty (only if overestimated)**
```
if self_grade > base_grade:
    penalty = (self_grade - base_grade) × scale
    weighted_grade = max(0, base_grade - penalty)
else:
    weighted_grade = base_grade  # No penalty!
```

### Example Scenarios

| Self-Grade | Base Grade | Scale | Penalty | Weighted | Result |
|------------|------------|-------|---------|----------|--------|
| 85 | 85 | 0.89 | 0 | 85 | ✅ Accurate! |
| 70 | 85 | 0.59 | 0 | 85 | 🌟 Humble! |
| 95 | 85 | 1.18 | -11.8 | 73.2 | ⚠️ Optimistic |
| 100 | 70 | 1.35 | -40.5 | 29.5 | ❌ Very Overconfident |

## What It Does

1. **Scans student submission PDFs** for self-proclaimed grades
   - Searches for: "Self-Grade: XX", "I estimate: XX%", "My grade: XX"
   - Falls back to base grade if not found (no penalty)

2. **Calculates weighted grades** using exponential penalty formula
   - Rewards accurate self-assessment (no penalty)
   - Rewards humility (underestimation = no penalty)
   - Penalizes overconfidence (penalty increases with claim height)

3. **Updates Excel spreadsheet** with:
   - **Self-Grade column** (after Student ID)
   - **Penalty column** (before Weighted Grade)
   - **Weighted Grade column** (final grade after penalty)

4. **Generates summary report** showing:
   - How many self-grades were found vs. missing
   - Penalty distribution (none/small/medium/large)
   - Most accurate self-assessors
   - Most overconfident students

## Excel Output

### Before

| Student ID | Generated Grade | Weighted Grade | Assessment Date |
|------------|-----------------|----------------|-----------------|
| 38981 | 94 | (empty) | (empty) |
| 38960 | 89 | (empty) | (empty) |

### After

| Student ID | Self-Grade | Generated Grade | Penalty | Weighted Grade | Assessment Date |
|------------|------------|-----------------|---------|----------------|-----------------|
| 38981 | 95 | 94 | -1.18 | 92.82 | (empty) |
| 38960 | 89 | 89 | 0 | 89.00 | (empty) |

## Usage Examples

### Example: Process All Students

Invoke the skill in Claude Code:

```
/weighted-grade-calculator
```

**Expected Output:**
```
✓ Backup created: Assignment3_Grading_Summary_backup_20251202_143022.xlsx

🔍 Scanning for student submission PDFs in ../../WorkSubmissions01...
✓ Found 46 student PDFs

📊 Processing students...
✓ Student 38981: Self-grade 95 extracted from PDF
✓ Student 38960: Self-grade 89 extracted from PDF
⚠️  Student 38964: No self-grade found, using base grade 44 (no penalty)
...

✓ Excel updated: ../../Assignment3_Grading_Summary.xlsx

╔════════════════════════════════════════════════╗
║  WEIGHTED GRADE CALCULATION SUMMARY           ║
╚════════════════════════════════════════════════╝

Students Processed: 46
Self-Grades Found: 38 (82.6%)
Self-Grades Missing: 8 (17.4%)

Penalty Statistics:
├─ No Penalty (accurate/humble): 32 (69.6%)
├─ Small Penalty (1-5 points): 8 (17.4%)
├─ Medium Penalty (6-15 points): 4 (8.7%)
└─ Large Penalty (>15 points): 2 (4.3%)

Average Base Grade: 72.89
Average Weighted Grade: 70.12
Average Penalty: -2.77 points

Top 3 Self-Assessors (most accurate):
1. Student 38960: Self=89, Actual=89, Diff=0.0 ✓
2. Student 38981: Self=94, Actual=94, Diff=0.0 ✓
3. Student 38982: Self=72, Actual=71, Diff=1.0 ✓

Top 3 Most Overconfident:
1. Student 38964: Self=85, Actual=44, Penalty=44.2 ❌
2. Student 38984: Self=80, Actual=55, Penalty=19.5 ❌
3. Student 38963: Self=75, Actual=55, Penalty=13.6 ❌

✅ Weighted grade calculation complete!
```

## Self-Grade Extraction

The skill searches for self-grades in student PDFs using these patterns:

```python
patterns = [
    r"Self[- ]?Grade:?\s*(\d+)",       # "Self-Grade: 85"
    r"I estimate:?\s*(\d+)%?",         # "I estimate: 90%"
    r"My grade:?\s*(\d+)",              # "My grade: 80"
    r"Self[- ]?assessment:?\s*(\d+)",   # "Self-assessment: 88"
    r"Expected grade:?\s*(\d+)",        # "Expected grade: 92"
    r"Predicted grade:?\s*(\d+)"        # "Predicted grade: 87"
]
```

**If not found:**
- Uses base grade as default (no penalty applied)
- Marks as "No self-grade provided" in processing log
- Student still gets fair treatment (their earned grade)

## Edge Cases

### Missing Self-Grade
**Solution:** Use base grade (no penalty)
```
Student 38964: Self-grade = 44 (base), Base = 44
→ Weighted = 44 (no penalty)
```

### Self-Grade Out of Range
**Solution:** Clamp to valid range [60, 100]
```
Input: Self-grade = 110
→ Adjusted to: 100
```

### Perfect Score
**Solution:** No penalty if accurate
```
Student claims 100, earns 100
→ Weighted = 100 (perfect accuracy!)
```

### Zero or Negative Weighted Grade
**Solution:** Cap at 0
```
Self = 100, Base = 40, Penalty = 81
→ Weighted = max(0, 40 - 81) = 0
```

## Files

```
.claude/skills/weighted-grade-calculator/
├── SKILL.md                          # Skill definition and rubric
├── README.md                         # This file
├── prompt.md                         # Claude CLI skill prompt
└── skill.json                        # Claude Code skill metadata
```

## Dependencies

The skill requires Python packages for Excel and PDF processing:

- **openpyxl:** Read/write Excel files
- **PyPDF2:** Extract text from PDFs

Claude will handle these dependencies automatically when invoking the skill.

## Troubleshooting

### Error: "Required columns not found in Excel"

Make sure your Excel has these columns:
- Student ID
- Generated Grade (/100)
- Weighted Grade

### Warning: "No self-grade found"

This is normal. The skill uses base grade as default (no penalty).

### Excel file is locked

Close Excel before invoking the skill. A backup is created automatically.

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
│ 3. Create Excel Summary         │
│    (all grades in one sheet)    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 4. Calculate Weighted Grades ◄──┐
│    (THIS SKILL)                 │
│    - Extract self-grades        │
│    - Apply penalty formula      │
│    - Update Excel               │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 5. Final Grades Ready           │
│    (weighted = official grade)  │
└─────────────────────────────────┘
```

## Philosophy

This formula implements **metacognitive assessment** - evaluating students' ability to accurately judge their own work.

**Design Principles:**
1. **Reward humility:** Students who underestimate get full credit
2. **Reward accuracy:** No penalty for accurate self-assessment
3. **Penalize overconfidence:** Higher claims = higher risk
4. **Fair to all:** Missing self-grade = no penalty (default to base)

**Why This Matters:**
- Teaches realistic self-evaluation
- Prevents grade inflation through self-reporting
- Encourages honest reflection on work quality
- Rewards metacognitive skills (knowing what you know)

## Version History

- **v1.0.0** - Initial implementation with exponential penalty formula

---

**Created:** December 2025
**Purpose:** Add metacognitive assessment layer to RuniGrader

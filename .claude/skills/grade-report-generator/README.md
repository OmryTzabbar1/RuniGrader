# Grade Report Generator Skill

Generates professional, student-facing PDF grade reports with personalized feedback and emojis.

## Purpose

Creates clean, encouraging grade reports that students receive - without internal grading details, skill versions, or policy information. The PDF adjusts its tone and emoji usage based on the student's grade level.

## Features

### Grade-Based Customization

- **A-level (90-100%):** Lots of emojis (🎉 🏆 ⭐ 🔥 ✨), enthusiastic tone
- **B-level (80-89%):** Moderate emojis (✅ 👍 💡 📈), encouraging tone
- **C-level (70-79%):** Fewer emojis (✓ ⚡), supportive tone
- **D-level (60-69%):** Minimal emojis (✓), constructive tone
- **F-level (<60%):** No emojis, serious tone with clear action items

### Content

**Page 1: Grade Summary**
- Assignment title
- Student ID and team name
- Repository information
- Final grade (large, prominent)
- Pass/fail status
- Assessment date

**Page 2: Personalized Feedback**
- Opening paragraph (tone matches grade level)
- Key strengths (bulleted with emojis)
- Areas for improvement (actionable recommendations)
- Closing encouragement

## Usage

### From Command Line

```bash
python .claude/skills/grade-report-generator/generate_student_report.py \
  --student-id "63701" \
  --team "Fouad Almalki" \
  --grade 91 \
  --repository "fouada/Assignment_3" \
  --output-dir "/path/to/student/folder" \
  --strengths "Strength 1|Strength 2|Strength 3" \
  --improvements "Improvement 1|Improvement 2" \
  --assignment "Assignment 3: Agentic Turing Machine"
```

### From Claude Agent

```bash
# Invoke the skill
/invoke-skill grade-report-generator

# Provide assessment data when prompted
```

## Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--student-id` | Yes | Student ID | `"63701"` |
| `--team` | Yes | Team/student name | `"Fouad Almalki"` |
| `--grade` | Yes | Final grade (0-100) | `91` |
| `--repository` | No | Repository name/URL | `"fouada/Assignment_3"` |
| `--output-dir` | Yes | Output directory | `"C:\path\to\folder"` |
| `--strengths` | No | Pipe-separated strengths | `"Strength 1\|Strength 2"` |
| `--improvements` | No | Pipe-separated improvements | `"Improve 1\|Improve 2"` |
| `--assignment` | No | Assignment name | `"Assignment 3"` |

## Output

Generates: `Student_Grade_Report_{student_id}.pdf`

Example: `Student_Grade_Report_63701.pdf`

## Examples

### A-Level Student (91%)

```bash
python generate_student_report.py \
  --student-id "63701" \
  --team "Fouad Almalki" \
  --grade 91 \
  --strengths "Exceptional testing|Outstanding documentation|Strong CI/CD" \
  --improvements "Add plugin architecture|Implement pre-commit hooks" \
  --output-dir "./output"
```

**Result:** Enthusiastic report with lots of emojis (🎉 🏆 ⭐), celebratory tone

### C-Level Student (75%)

```bash
python generate_student_report.py \
  --student-id "12345" \
  --team "John Doe" \
  --grade 75 \
  --strengths "Basic testing present|Documentation exists" \
  --improvements "Increase test coverage|Improve documentation|Add error handling" \
  --output-dir "./output"
```

**Result:** Supportive report with fewer emojis (✓ ⚡), constructive tone

### F-Level Student (55%)

```bash
python generate_student_report.py \
  --student-id "99999" \
  --team "Jane Smith" \
  --grade 55 \
  --improvements "Add comprehensive tests|Write documentation|Implement proper error handling|Follow git best practices" \
  --output-dir "./output"
```

**Result:** Serious report with no emojis, clear action items for improvement

## Design Philosophy

### What to Include
✅ Final grade percentage
✅ Pass/fail status
✅ Personalized strengths
✅ Actionable improvements
✅ Encouraging feedback

### What NOT to Include
❌ Skill version numbers
❌ Grading policy versions
❌ Internal rubric details
❌ Skill-by-skill breakdown
❌ Assessment metadata

### Tone Guidelines

The report should feel:
- **Professional:** Like an official grade document
- **Personal:** Like a human graded it
- **Encouraging:** Even for low grades, provide constructive guidance
- **Appropriate:** Match tone to performance level

## Integration with Assessment System

Typically used as final step after Tier 2 assessment:

1. Run Tier 2 orchestrator (all 10 skills)
2. Collect final grade and feedback
3. Generate student-facing PDF report
4. Deliver PDF to student

## File Structure

```
.claude/skills/grade-report-generator/
├── SKILL.md                      # Skill definition
├── README.md                     # This file
└── generate_student_report.py    # PDF generator script
```

## Dependencies

- Python 3.7+
- reportlab (installed via pip)

## Notes

- PDF is optimized for letter size (8.5" x 11")
- Uses professional fonts (Helvetica)
- Color-coded grade boxes (green for A, blue for B, etc.)
- Emojis render correctly in most PDF readers
- File size typically 4-6KB per report

## Customization

To modify feedback tone or emoji selection, edit:
- `get_emoji_set()` function in `generate_student_report.py`
- `get_feedback_tone()` function in `generate_student_report.py`

## Testing

Test with different grade levels:

```bash
# Test A-level
python generate_student_report.py --student-id "TEST1" --team "Test" --grade 95 --output-dir "./test"

# Test B-level
python generate_student_report.py --student-id "TEST2" --team "Test" --grade 85 --output-dir "./test"

# Test C-level
python generate_student_report.py --student-id "TEST3" --team "Test" --grade 75 --output-dir "./test"

# Test failing
python generate_student_report.py --student-id "TEST4" --team "Test" --grade 55 --output-dir "./test"
```

Verify:
- Emoji usage matches grade level
- Tone is appropriate
- Feedback is constructive
- Layout is professional

---

**Version:** 1.0.0
**Created:** December 2025
**Purpose:** Student-facing grade reports with personality

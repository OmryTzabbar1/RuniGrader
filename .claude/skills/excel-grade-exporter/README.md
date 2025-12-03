# Excel Grade Exporter Skill

Export grading results to Excel files in Moodle-compatible format with weighted grade calculations.

## Purpose

Generate two Excel files from Tier 2 assessment results:
1. **Moodle Upload Format** - Ready to import into Moodle with weighted grades
2. **Grade Comparison** - Compare calculated grades (10 skills) vs weighted grades

## Quick Start

```bash
python .claude/skills/excel-grade-exporter/export_grades.py <assignment_number>
```

Example:
```bash
python .claude/skills/excel-grade-exporter/export_grades.py 1
```

## What It Does

### Input
- Assessment JSON files from `assessments_tier2_assignment{N}/`
- Weighted grade calculations (using weighted-grade-calculator logic)
- Template format from `work1-runi-grade-format.csv`

### Output

**File 1: `StudentGradesMoodleFormat/Assignment{N}_Moodle_Grades.xlsx`**
- Moodle-compatible format with Hebrew column headers
- Uses **weighted grade** as final grade
- Includes feedback from assessment JSONs
- Ready to upload to Moodle

**File 2: `StudentGradesForRami/Assignment{N}_Grade_Comparison.xlsx`**
- Side-by-side comparison of grades
- Shows calculated vs weighted grades
- Displays penalty applied
- Color-coded for easy review

## Features

- ✅ Moodle CSV format compatibility
- ✅ Weighted grade calculation integration
- ✅ Automatic feedback extraction from JSONs
- ✅ Color-coded comparison view
- ✅ Handles missing data gracefully
- ✅ Creates backups before operations

## Workflow Integration

```
Tier 2 Assessments → JSON Files → Excel Exporter → Moodle Upload
                                        ↓
                                 Grade Comparison
```

## Files

```
.claude/skills/excel-grade-exporter/
├── README.md                    # This file
├── export_grades.py             # Main export script
├── weighted_calculator.py       # Weighted grade logic
└── skill.json                   # Skill metadata
```

## Requirements

- Python 3.8+
- openpyxl
- PyPDF2

---

**Created:** December 2025
**Purpose:** Streamline grade export for Moodle integration

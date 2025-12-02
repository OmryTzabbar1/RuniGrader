# Complete Grading Workflow for Student Assignments

**Version:** 1.0
**Date:** 2025-12-01
**Purpose:** Step-by-step guide for grading student submissions using Claude Code

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Directory Structure](#directory-structure)
4. [Complete Workflow](#complete-workflow)
5. [Phase 1: Initial Setup](#phase-1-initial-setup)
6. [Phase 2: Extract Student Information](#phase-2-extract-student-information)
7. [Phase 3: Repository Assessment](#phase-3-repository-assessment)
8. [Phase 4: Two-Tier Grading](#phase-4-two-tier-grading)
9. [Phase 5: Final Grade Recording](#phase-5-final-grade-recording)
10. [Phase 6: PDF Report Generation](#phase-6-pdf-report-generation)
11. [Commands Reference](#commands-reference)
12. [Troubleshooting](#troubleshooting)

---

## Overview

This grading system uses a **two-tier approach** based on student self-assessment:

- **Tier 1 (Self-Grade < 80)**: Simple grading - count TRUE criteria → Final Grade
- **Tier 2 (Self-Grade ≥ 80)**: Rigorous assessment using 10 specialized skills

**Quality Over Speed**: We prioritize accurate, fair grading over processing time.

---

## Prerequisites

### Required Files and Tools

1. **Claude Code CLI** - Installed and configured
2. **Python 3.8+** - For running batch scripts
3. **Excel** or **LibreOffice** - For viewing/editing grade sheets
4. **Git** - For cloning student repositories

### Required Files in Repository

- `.claude/commands/git-repo-assessment.md` - Repository assessment command
- `.claude/commands/SubmissionRequirements.txt` - Grading criteria (22 requirements)
- `.claude/skills/` - Directory with 10 assessment skills
- `process_all_submissions.py` - Batch processing script
- `.claude/skills/batch-repo-assessment/run_batch_assessment.py` - Batch assessment helper

---

## Directory Structure

```
Runi/
├── WorkSubmissions03/                          # Current assignment submissions
│   ├── Participant_63698_assignsubmission_file/
│   │   ├── Llms third project.pdf             # Student's submitted PDF
│   │   ├── submission_info.xlsx               # Extracted metadata
│   │   └── repo_assessment.md                 # Generated assessment (22 criteria)
│   ├── Participant_63699_assignsubmission_file/
│   │   └── ...
│   └── ...
├── grades_assignment3.xlsx                     # Master grade sheet (to be created)
├── .claude/
│   ├── commands/
│   │   ├── git-repo-assessment.md             # Assessment command
│   │   └── SubmissionRequirements.txt         # 22 grading criteria
│   └── skills/                                # 10 assessment skills
│       ├── 1-project-planning/
│       ├── 2-code-documentation/
│       ├── 3-config-security/
│       ├── 4-testing-quality/
│       ├── 5-research-analysis/
│       ├── 6-ui-ux/
│       ├── 7-version-management/
│       ├── 8-costs-pricing/
│       ├── 9-extensibility/
│       └── 10-quality-standards/
└── docs/
    ├── GRADING_WORKFLOW.md                    # This file
    ├── IMPLEMENTATION_PLAN.md
    └── IMPLEMENTATION_SUMMARY.md
```

---

## Complete Workflow

### High-Level Process

```
1. Download student submissions manually (Moodle/LMS)
   ↓
2. Extract student information from PDFs → Excel
   ↓
3. Run repository assessments (22 criteria) → repo_assessment.md
   ↓
4. Check self-grades in Excel (< 80 or ≥ 80)
   ↓
5a. TIER 1 (< 80): Count TRUE/22 → Final Grade
5b. TIER 2 (≥ 80): Run 10 skills → Final Grade
   ↓
6. Record final grades in Excel
   ↓
7. Generate PDF reports (input template + grading report)
```

---

## Phase 1: Initial Setup

### Step 1.1: Download Submissions

1. Go to your LMS (Moodle, Canvas, etc.)
2. Download all student submissions as a ZIP file
3. Extract to `WorkSubmissionsXX/` folder (where XX is assignment number)
   - Example: `WorkSubmissions03/` for Assignment 3

**Result:** Each student gets a folder named `Participant_XXXXX_assignsubmission_file/`

### Step 1.2: Verify Folder Structure

```bash
# Check that each student folder contains their PDF
ls WorkSubmissions03/Participant_*/
```

**Expected:** Each folder should have at least one PDF file

### Step 1.3: Create Master Excel File

Create a new Excel file: `grades_assignmentX.xlsx` with columns:

| Participant ID | Group Code | Student 1 | Student 2 | GitHub Repository | Self-Grade | TRUE Count | Final Grade | Tier |
|----------------|------------|-----------|-----------|-------------------|------------|------------|-------------|------|
| 63698 | | | | | | | | |
| 63699 | | | | | | | | |

**Template:**
```
Column A: Participant ID (from folder name)
Column B: Group Code (from PDF)
Column C: Student 1 Name (from PDF)
Column D: Student 2 Name (from PDF)
Column E: GitHub Repository URL (from PDF)
Column F: Self-Grade (from PDF, 60-100)
Column G: TRUE Count (from repo_assessment.md)
Column H: Final Grade (calculated)
Column I: Tier (Excellence/Good/Potential/Below)
```

---

## Phase 2: Extract Student Information

### Step 2.1: Manual Extraction from PDFs

For each student, open their PDF and extract:

1. **Participant ID** - Already in folder name
2. **Group Code** - Look for "Group: XXX" or team identifier
3. **Student Names** - Team member names
4. **GitHub Repository URL** - Look for repository link
5. **Self-Grade** - Student's self-assessed grade (60-100)

### Step 2.2: Populate Excel File

Enter extracted information into `grades_assignmentX.xlsx`:

```excel
63698 | G42 | Fouad Almalki | | https://github.com/fouada/Assignment_3 | 100 | | |
63699 | G21 | Jane Doe | John Smith | https://github.com/jane/repo | 85 | | |
```

### Step 2.3: Alternative - Use Automated Extraction (Optional)

If you have a script for PDF extraction:

```bash
python .claude/skills/grade-extractor/extract_grades.py
```

**Note:** This requires setup and may need customization per assignment.

---

## Phase 3: Repository Assessment

This is the **CORE PHASE** - assessing each repository against 22 criteria.

### Step 3.1: Review Grading Criteria

```bash
# Read the requirements
cat .claude/commands/SubmissionRequirements.txt
```

**Important:** Familiarize yourself with all 22 criteria before starting assessments.

### Step 3.2: Run Assessment for Single Student

Use the Claude Code command `/git-repo-assessment`:

```bash
# In Claude Code CLI:
/git-repo-assessment https://github.com/fouada/Assignment_3
```

**What Happens:**
1. Claude clones the repository to a temp directory
2. Checks each of the 22 criteria individually
3. Reports progress every 5 criteria
4. Generates a markdown file with:
   - Table with TRUE/FALSE for each criterion
   - Key Findings section (Strengths, Missing criteria, Critical issues)

### Step 3.3: Move Assessment to Student Folder

```bash
# The assessment is generated in current directory
# Move it to the student's folder:
mv repo_assessment_*.md WorkSubmissions03/Participant_63698_assignsubmission_file/repo_assessment.md
```

### Step 3.4: Batch Processing Multiple Students

For efficiency, process students in batches of 5:

```bash
# Run the batch helper
python .claude/skills/batch-repo-assessment/run_batch_assessment.py
```

**Output:**
```
BATCH 1/7 (5 repositories)
================================================================================

1. Participant 63698 - Group: G42
   URL: https://github.com/fouada/Assignment_3
   Output folder: WorkSubmissions03/Participant_63698_assignsubmission_file

2. Participant 63699 - Group: G21
   URL: https://github.com/jane/repo
   Output folder: WorkSubmissions03/Participant_63699_assignsubmission_file

...

Next steps for Batch 1:
1. Call /git-repo-assessment for each URL above
2. Move the generated markdown file to the corresponding student folder
3. Rename to 'repo_assessment.md' in each folder
```

Then in Claude Code:
```bash
/git-repo-assessment https://github.com/fouada/Assignment_3
/git-repo-assessment https://github.com/jane/repo
# ... repeat for batch
```

### Step 3.5: Verify Assessment Files

```bash
# Check that each student has an assessment file
ls WorkSubmissions03/Participant_*/repo_assessment.md
```

**Expected:** One `repo_assessment.md` file per student folder.

### Step 3.6: Count TRUE Criteria

For each student's `repo_assessment.md`, count how many criteria are TRUE:

```bash
# Quick count using grep
grep "| TRUE |" WorkSubmissions03/Participant_63698_assignsubmission_file/repo_assessment.md | wc -l
```

**Record** this count in Column G (TRUE Count) of your Excel file.

**Example:**
```
Participant 63698: 22/22 TRUE
Participant 63699: 18/22 TRUE
Participant 63700: 12/22 TRUE
```

---

## Phase 4: Two-Tier Grading

Now we apply the **two-tier grading system** based on self-grade.

### Step 4.1: Identify Tier for Each Student

Check Column F (Self-Grade) in Excel:

- **Self-Grade < 80** → TIER 1 (Simple Grading)
- **Self-Grade ≥ 80** → TIER 2 (Rigorous Assessment with 10 Skills)

Mark this in Column I (Tier).

### TIER 1: Simple Grading (Self-Grade < 80)

For students with self-grade < 80:

**Formula:**
```
Final Grade = (TRUE Count / 22) × 100
```

**Example:**
```
Student ID: 63700
Self-Grade: 75
TRUE Count: 12/22
Final Grade = (12 / 22) × 100 = 54.5%
Tier: Below Standard
```

**Steps:**
1. Take TRUE Count from Column G
2. Calculate: `(TRUE Count / 22) × 100`
3. Record in Column H (Final Grade)
4. Determine tier based on final grade:
   - 90-100: Excellence
   - 80-89: Good
   - 55-79: Potential
   - <55: Below Standard
5. Record tier in Column I

**Excel Formula:**
```excel
=(G2/22)*100
```

### TIER 2: Rigorous Assessment (Self-Grade ≥ 80)

For students with self-grade ≥ 80, we run **all 10 assessment skills**.

#### Step 4.2.1: Navigate to Student Repository

```bash
# Clone the repository if not already cloned
git clone https://github.com/fouada/Assignment_3 temp_assessment_63698
cd temp_assessment_63698
```

#### Step 4.2.2: Run All 10 Skills

**Skill 1: Project Planning (10 points)**
```bash
# Check PRD and Architecture
# See .claude/skills/1-project-planning/SKILL.md for criteria
```

Use the commands in each skill's SKILL.md file:
```bash
# Example from Skill 1
ls PRD.md docs/PRD.md
grep -i "## Problem Statement" PRD.md
grep -ri "c4 model\|context diagram" docs/
```

**Score:** Count points based on criteria met (0-10)

Repeat for all 10 skills:

1. **Skill 1: Project Planning** → `/10`
2. **Skill 2: Code Documentation** → `/10`
3. **Skill 3: Configuration & Security** → `/10`
4. **Skill 4: Testing & Quality** → `/10`
5. **Skill 5: Research & Analysis** → `/10`
6. **Skill 6: UI/UX** → `/10`
7. **Skill 7: Version Management** → `/10`
8. **Skill 8: Costs & Pricing** → `/10`
9. **Skill 9: Extensibility** → `/10`
10. **Skill 10: Quality Standards** → `/10`

**Total:** Sum all skill scores (0-100)

#### Step 4.2.3: Record Skill Scores

Create additional columns in Excel or a separate sheet:

| Participant ID | Skill 1 | Skill 2 | Skill 3 | Skill 4 | Skill 5 | Skill 6 | Skill 7 | Skill 8 | Skill 9 | Skill 10 | Total | Final Grade |
|----------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|-------|-------------|
| 63698 | 9 | 8.5 | 10 | 8 | 7.5 | 7 | 9 | 6 | 8 | 7.5 | 80.5 | 80.5 |

#### Step 4.2.4: Calculate Final Grade for Tier 2

**Recommended Formula (Option 1):**
```
Final Grade = Total Skill Score (already out of 100)
```

**Alternative (Option 2 - Weighted):**
```
Final Grade = (Total Skill Score × 0.8) + ((TRUE Count / 22) × 100 × 0.2)
```

**Alternative (Option 3 - Both Must Pass):**
```
Final Grade = MIN(Total Skill Score, (TRUE Count / 22) × 100)
```

**Use Option 1 (recommended)** - Skills comprehensively cover all 22 requirements.

---

## Phase 5: Final Grade Recording

### Step 5.1: Complete Excel File

At this point, your Excel file should look like:

| ID | Group | Student 1 | Student 2 | GitHub | Self | TRUE | Final | Tier |
|----|-------|-----------|-----------|--------|------|------|-------|------|
| 63698 | G42 | Fouad | | url | 100 | 22 | 80.5 | Good |
| 63699 | G21 | Jane | John | url | 85 | 18 | 75.0 | Potential |
| 63700 | G18 | Bob | | url | 75 | 12 | 54.5 | Below |

### Step 5.2: Verify Grades

**Quality Checks:**

1. **All students have a final grade** (no blanks in Column H)
2. **Tier matches final grade:**
   - Excellence: 90-100
   - Good: 80-89
   - Potential: 55-79
   - Below: <55
3. **Self-grade ≥ 80 students have skill scores recorded**
4. **TRUE count matches repo_assessment.md**

### Step 5.3: Statistical Summary

Calculate class statistics:

```
Average: =AVERAGE(H:H)
Median: =MEDIAN(H:H)
Std Dev: =STDEV(H:H)
Min: =MIN(H:H)
Max: =MAX(H:H)

Distribution:
Excellence (90-100): =COUNTIFS(H:H,">=90",H:H,"<=100")
Good (80-89): =COUNTIFS(H:H,">=80",H:H,"<90")
Potential (55-79): =COUNTIFS(H:H,">=55",H:H,"<80")
Below (<55): =COUNTIF(H:H,"<55")
```

---

## Phase 6: PDF Report Generation

### Step 6.1: Report Template Structure

Each student receives a PDF report with:

**Section 1: Header**
- Assignment title
- Student name(s)
- Participant ID
- Submission date

**Section 2: Grade Summary**
- Self-Grade (claimed)
- TRUE Count (requirements met)
- Tier (if Tier 2: show skill breakdown)
- **Final Grade** (prominent)

**Section 3: Criteria Assessment**
- Table showing all 22 criteria (TRUE/FALSE)
- Mark missing criteria with ❌

**Section 4: Feedback** (tier-appropriate)
- **Excellence (90-100):** Enthusiastic, encouraging, minor improvements
- **Good (80-89):** Positive, constructive suggestions
- **Potential (55-79):** Supportive, specific improvement areas
- **Below (<55):** Constructive, actionable steps to improve

**Section 5: Detailed Findings** (if Tier 2)
- Skill-by-skill breakdown
- Specific recommendations from each skill

### Step 6.2: Generate Report for Tier 1 Student

**Template:** Simple report matching student PDF format

```python
# Pseudo-code for Tier 1 report generation
student_id = "63700"
self_grade = 75
true_count = 12
final_grade = (12 / 22) * 100  # 54.5

report = f"""
# Grading Report - Assignment 3
Student: {student_name}
Participant ID: {student_id}

## Grade Summary
Self-Grade: {self_grade}/100
Requirements Met: {true_count}/22
Final Grade: {final_grade:.1f}/100
Performance Tier: Below Standard

## Criteria Assessment
[Table with 22 criteria showing TRUE/FALSE]

## Feedback
[Constructive feedback focusing on missing criteria and improvement areas]

## Missing Criteria
- Criterion X: [Specific reason why not met]
- Criterion Y: [Specific reason why not met]
...

## Recommendations
1. [Specific action to improve]
2. [Specific action to improve]
...
"""
```

### Step 6.3: Generate Report for Tier 2 Student

**Template:** Comprehensive report with skill breakdown

```python
# Pseudo-code for Tier 2 report generation
student_id = "63698"
self_grade = 100
true_count = 22
skill_scores = {
    "project-planning": 9.0,
    "code-documentation": 8.5,
    "config-security": 10.0,
    ...
}
total_score = sum(skill_scores.values())  # 80.5
final_grade = total_score

report = f"""
# Grading Report - Assignment 3
Student: {student_name}
Participant ID: {student_id}

## Grade Summary
Self-Grade: {self_grade}/100
Requirements Met: {true_count}/22
Final Grade: {final_grade:.1f}/100
Performance Tier: Good

## Skill Assessment (10 Skills)
1. Project Planning: {skill_scores['project-planning']}/10
2. Code Documentation: {skill_scores['code-documentation']}/10
...
10. Quality Standards: {skill_scores['quality-standards']}/10

**Total Score: {total_score}/100**

## Criteria Assessment
[Table with 22 criteria - all TRUE for this student]

## Overall Feedback
[Tier-appropriate feedback addressing strengths and minor improvements]

## Skill-by-Skill Breakdown

### Skill 1: Project Planning ({skill_scores['project-planning']}/10)
- Strengths: [specific strengths]
- Recommendations: [specific improvements]

### Skill 2: Code Documentation ({skill_scores['code-documentation']}/10)
...

## Summary & Next Steps
[Concluding remarks and actionable next steps]
"""
```

### Step 6.4: Save Reports

Save each report as:
```
WorkSubmissions03/Participant_XXXXX_assignsubmission_file/grading_report.pdf
```

---

## Commands Reference

### Claude Code Commands

```bash
# Assess a single repository
/git-repo-assessment <github-url>

# Example
/git-repo-assessment https://github.com/fouada/Assignment_3
```

### Python Scripts

```bash
# Batch assessment helper
python .claude/skills/batch-repo-assessment/run_batch_assessment.py

# Process all submissions (extract info from PDFs)
python process_all_submissions.py
```

### Git Commands

```bash
# Clone student repository for assessment
git clone <github-url> temp_assessment_<participant-id>

# Check commit count
cd temp_assessment_<participant-id>
git log --oneline --no-merges | wc -l

# Check commit messages format
git log --pretty=format:"%s" --no-merges

# Clean up after assessment
cd ..
rm -rf temp_assessment_<participant-id>
```

### File Checks

```bash
# Count TRUE criteria in assessment
grep "| TRUE |" repo_assessment.md | wc -l

# Count FALSE criteria
grep "| FALSE |" repo_assessment.md | wc -l

# View assessment summary
grep "Score:" repo_assessment.md
```

---

## Troubleshooting

### Issue 1: Assessment Command Not Found

**Problem:** `/git-repo-assessment` command not recognized

**Solution:**
```bash
# Verify command file exists
ls .claude/commands/git-repo-assessment.md

# Check Claude Code is running in correct directory
pwd
# Should be: C:\Users\Guest1\CoOp\Runi
```

### Issue 2: Repository Clone Fails

**Problem:** Cannot clone student repository (private, deleted, wrong URL)

**Solutions:**
1. **Private Repository:** Request access from student or ask them to make it public
2. **Deleted Repository:** Contact student to restore or provide alternative
3. **Wrong URL:** Verify URL in student PDF, check for typos

**Record in Excel:**
```
Final Grade: 0
Notes: "Repository inaccessible - cannot assess"
```

### Issue 3: Missing Criteria in Assessment

**Problem:** `repo_assessment.md` has fewer than 22 criteria

**Solution:**
```bash
# Re-run assessment with verbose mode
/git-repo-assessment <url>

# Manually check against SubmissionRequirements.txt
cat .claude/commands/SubmissionRequirements.txt

# Count criteria in assessment
grep "^| [0-9]" repo_assessment.md | wc -l
```

### Issue 4: Self-Grade Missing

**Problem:** Student didn't include self-grade in PDF

**Solutions:**
1. **Default Approach:** Email student to request self-grade
2. **Conservative Approach:** Use minimum (60) - penalizes them for not following instructions
3. **Fair Approach:** Use their TRUE count as self-grade: `(TRUE Count / 22) × 100`

### Issue 5: Excel Formulas Not Working

**Problem:** Final grade formula returns error

**Common Fixes:**
```excel
# Instead of: =(G2/22)*100
# Use: =IF(ISNUMBER(G2), (G2/22)*100, "")

# For tier calculation:
=IF(H2>=90, "Excellence", IF(H2>=80, "Good", IF(H2>=55, "Potential", "Below")))
```

### Issue 6: Tier 2 Assessment Taking Too Long

**Problem:** Running 10 skills for many students is time-consuming

**Solutions:**
1. **Prioritize:** Start with highest self-grades (most likely to be Tier 2)
2. **Batch Processing:** Do all Skill 1 assessments, then all Skill 2, etc.
3. **Parallel Work:** Use multiple Claude Code sessions for different students
4. **Quality First:** Remember, we prioritize accuracy over speed

---

## Tips for Efficient Grading

### Before You Start

1. **Read all 22 criteria** - Understand what you're looking for
2. **Review sample student repos** - Get a baseline for "good" vs "poor"
3. **Set up templates** - Excel formulas, report templates
4. **Test workflow** - Try one student end-to-end before batch processing

### During Grading

1. **Work in batches** - Process 5 students at a time
2. **Take breaks** - Grading fatigue affects fairness
3. **Document edge cases** - Note unusual situations for consistency
4. **Keep notes** - Record interesting findings, common issues
5. **Verify as you go** - Check TRUE counts match assessment files

### After Grading

1. **Statistical review** - Check distribution makes sense
2. **Spot check** - Verify a few random assessments manually
3. **Feedback review** - Ensure tier-appropriate feedback quality
4. **Archive assessments** - Keep all `repo_assessment.md` files
5. **Document process improvements** - Note what worked, what didn't

---

## Grading Philosophy

### Fairness

- **Consistent criteria application** - Same standards for all students
- **Transparent process** - Students can see exactly what was checked
- **Multiple chances** - Consider allowing resubmissions for critical missing items
- **Documented decisions** - Keep notes on edge cases

### Quality

- **Thorough assessment** - Check all 22 criteria carefully
- **Evidence-based** - Grades based on actual artifacts, not assumptions
- **Constructive feedback** - Help students improve, not just assign scores
- **Skill development** - Tier 2 assessment helps students understand professional standards

### Efficiency

- **Automation where appropriate** - Use batch scripts, formulas
- **Manual review where needed** - Don't trust automation blindly
- **Progressive refinement** - Improve process each assignment
- **Tool development** - Build better scripts based on experience

---

## Future Improvements

### Automation Opportunities

1. **PDF Extraction:** Automate extraction of student info from PDFs
2. **Batch Assessment:** Run all 10 skills automatically for Tier 2 students
3. **Report Generation:** Auto-generate PDF reports from templates
4. **Excel Population:** Directly write grades to Excel from scripts

### Process Enhancements

1. **Student Self-Service:** Students run assessments on their own repos before submission
2. **Real-time Feedback:** Provide preliminary grades during submission window
3. **Analytics Dashboard:** Visualize class performance, common issues
4. **Rubric Refinement:** Adjust criteria based on student performance patterns

---

## Conclusion

This workflow balances **quality, fairness, and efficiency**:

- **Tier 1** provides quick grading for students who self-assess lower
- **Tier 2** provides comprehensive feedback for students claiming high performance
- **22 Criteria** ensure consistent evaluation across all students
- **10 Skills** provide deep insights into professional software development practices

**Remember:** The goal is not just to assign grades, but to help students understand professional software development standards and develop accurate self-assessment skills.

---

**Last Updated:** 2025-12-01
**Next Review:** After completing Assignment 3 grading (document lessons learned)

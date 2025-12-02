# Claude's Grading Process - Step-by-Step Commands

**Version:** 1.0
**Date:** 2025-12-01
**Purpose:** Instructions for Claude Code to follow when grading student assignments

---

## Overview

When the user says "Grade the submissions" or similar, follow this process step-by-step.

**User does:** Download submissions manually from LMS
**Claude does:** Everything else (extraction, assessment, grading, reports)

---

## Pre-Requisites Check

Before starting, verify:

```bash
# Check you're in the right directory
pwd
# Should be: C:\Users\Guest1\CoOp\Runi

# Check submissions folder exists
ls WorkSubmissions03/
# Should show multiple Participant_XXXXX_assignsubmission_file folders

# Check each folder has a PDF
find WorkSubmissions03 -name "*.pdf" -type f
```

---

## STEP 1: Extract Student Information from PDFs → Excel

### Command to Run:

```bash
python .claude/skills/grade-extractor/extract_grades.py WorkSubmissions03 grades_assignment3.xlsx
```

### What This Does:
1. Scans `WorkSubmissions03/` for all `Participant_*` folders
2. Finds PDF in each folder
3. Creates `grades_assignment3.xlsx` with columns:
   - Participant ID
   - Group Code (empty - to fill next)
   - Student 1 (empty - to fill next)
   - Student 2 (empty - to fill next)
   - GitHub Repository (empty - to fill next)
   - Suggested Grade (empty - to fill next)
   - PDF Filename
4. Creates `grades_assignment3_submissions.json` with list of all PDFs

### Output Example:
```
Found 35 submission folders

[1] Participant 63698 - Llms third project.pdf
[2] Participant 63699 - Assignment3.pdf
...

[OK] Initial Excel file created: grades_assignment3.xlsx
[OK] Submission list saved: grades_assignment3_submissions.json

Total submissions found: 35
```

---

## STEP 2: Extract Information from Each PDF

### Process:

For each student (iterate through `grades_assignment3_submissions.json`):

1. **Read the PDF** using the Read tool:
   ```
   Read WorkSubmissions03/Participant_63698_assignsubmission_file/Llms third project.pdf
   ```

2. **Extract 5 fields** from the PDF text:
   - Group Code (e.g., "G42", "TeamAlpha")
   - Student 1 Name (e.g., "Fouad Almalki")
   - Student 2 Name (e.g., "Jane Doe" or empty if solo)
   - GitHub Repository URL (e.g., "https://github.com/fouada/Assignment_3")
   - Suggested Grade (Self-grade, 60-100)

3. **Update Excel** with extracted data:
   ```bash
   python .claude/skills/grade-extractor/update_excel.py grades_assignment3.xlsx 63698 "G42" "Fouad Almalki" "" "https://github.com/fouada/Assignment_3" "100"
   ```

### Extraction Patterns to Look For:

The PDFs typically have this format:
```
1. Group code: G42
2. Student one: Fouad Almalki
3. Student two: [empty or another name]
4. Repo link: https://github.com/fouada/Assignment_3
5. Grade suggestion: 100
```

Or Hebrew variations:
```
קוד קבוצה: G42
הציון העצמי שלי: 100/100
```

### Batch Processing:

Process 5 students at a time for efficiency:

```python
# Read all 5 PDFs
Read WorkSubmissions03/Participant_63698_assignsubmission_file/*.pdf
Read WorkSubmissions03/Participant_63699_assignsubmission_file/*.pdf
Read WorkSubmissions03/Participant_63700_assignsubmission_file/*.pdf
Read WorkSubmissions03/Participant_63701_assignsubmission_file/*.pdf
Read WorkSubmissions03/Participant_63702_assignsubmission_file/*.pdf

# Then update Excel for all 5
python .claude/skills/grade-extractor/update_excel.py grades_assignment3.xlsx 63698 "..." "..." "..." "..." "..."
python .claude/skills/grade-extractor/update_excel.py grades_assignment3.xlsx 63699 "..." "..." "..." "..." "..."
# etc.
```

**Progress Tracking:**
- Report every 5 students: "Processed 5/35 students..."
- Note any missing fields or errors

---

## STEP 3: Run Repository Assessments (22 Criteria)

For each student, assess their GitHub repository against the 22 criteria.

### Command:

```bash
/git-repo-assessment https://github.com/fouada/Assignment_3
```

### What This Does:
1. Clones the repository to a temp directory
2. Checks each of the 22 criteria from `SubmissionRequirements.txt`
3. Reports progress every 5 criteria
4. Generates `repo_assessment.md` with:
   - Table with TRUE/FALSE for each criterion
   - Score: X/22 criteria met
   - Key Findings (Strengths, Missing criteria, Critical issues)

### After Running Assessment:

1. **Move the file** to the student's folder:
   ```bash
   mv repo_assessment_*.md WorkSubmissions03/Participant_63698_assignsubmission_file/repo_assessment.md
   ```

2. **Count TRUE criteria**:
   ```bash
   grep "| TRUE |" WorkSubmissions03/Participant_63698_assignsubmission_file/repo_assessment.md | wc -l
   ```

3. **Record in notes** or prepare for next step

### Batch Processing:

Process repositories in batches of 5:

```bash
# Batch 1 (Students 1-5)
/git-repo-assessment https://github.com/student1/repo
# Move file: mv repo_assessment_*.md WorkSubmissions03/Participant_63698_assignsubmission_file/repo_assessment.md
# Count TRUE: grep "| TRUE |" ... | wc -l → Record: 22/22

/git-repo-assessment https://github.com/student2/repo
# Move file...
# Count TRUE... → Record: 18/22

# Continue for batch...

# Report progress
"Batch 1 complete (5/35 students assessed)"

# Batch 2 (Students 6-10)
# ... repeat
```

**Important:** After each batch, report:
- Number of students assessed
- Range of scores (e.g., "Scores range from 12/22 to 22/22")
- Any repository access issues

---

## STEP 4: Determine Tier for Each Student

Check the **Suggested Grade (Self-Grade)** column in Excel:

### Tier Classification:

```python
if self_grade < 80:
    tier = "TIER 1 - Simple Grading"
else:
    tier = "TIER 2 - Rigorous Assessment (10 Skills)"
```

### Create Two Lists:

**Tier 1 Students** (Self-Grade < 80):
```
Participant 63700: Self=75, TRUE=12/22 → Simple grading
Participant 63705: Self=70, TRUE=15/22 → Simple grading
...
```

**Tier 2 Students** (Self-Grade ≥ 80):
```
Participant 63698: Self=100, TRUE=22/22 → Run 10 skills
Participant 63699: Self=85, TRUE=18/22 → Run 10 skills
...
```

---

## STEP 5a: Grade Tier 1 Students (Simple Grading)

For each Tier 1 student:

### Formula:
```
Final Grade = (TRUE Count / 22) × 100
```

### Example Calculation:
```
Student 63700:
- Self-Grade: 75
- TRUE Count: 12/22
- Final Grade = (12 / 22) × 100 = 54.5%
- Performance Tier: Below Standard (<55)
```

### Performance Tier Assignment:
```python
if final_grade >= 90:
    performance_tier = "Excellence"
elif final_grade >= 80:
    performance_tier = "Good"
elif final_grade >= 55:
    performance_tier = "Potential"
else:
    performance_tier = "Below Standard"
```

### Record in Excel:

Add columns to Excel:
- Column H: TRUE Count (e.g., "12")
- Column I: Final Grade (e.g., "54.5")
- Column J: Performance Tier (e.g., "Below Standard")

---

## STEP 5b: Grade Tier 2 Students (Rigorous Assessment)

For each Tier 2 student, run all 10 assessment skills.

### Process for Each Student:

1. **Clone their repository** (if not already cloned):
   ```bash
   git clone https://github.com/fouada/Assignment_3 temp_assessment_63698
   cd temp_assessment_63698
   ```

2. **Run Skill 1: Project Planning**

   Read the skill criteria:
   ```bash
   cat ../.claude/skills/1-project-planning/SKILL.md
   ```

   Execute validation commands:
   ```bash
   # Check PRD exists
   ls PRD.md docs/PRD.md

   # Verify sections
   grep -i "## Problem Statement" PRD.md
   grep -i "## Functional Requirements" PRD.md

   # Check architecture
   grep -ri "c4 model\|context diagram" docs/ PLANNING.md
   ```

   **Score** based on criteria (0-10 points):
   - PRD exists: +2
   - Has Problem Statement: +1
   - Has Functional Requirements: +1.5
   - Has Success Metrics: +0.5
   - Architecture docs exist: +2
   - Has C4 diagrams: +3

   **Record:** `Skill 1 = 8.5/10`

3. **Run Skill 2: Code Documentation**

   ```bash
   cat ../.claude/skills/2-code-documentation/SKILL.md
   ```

   ```bash
   # Check README
   ls README.md
   wc -l README.md
   grep -i "## Installation\|## Usage" README.md

   # Check project structure
   ls src/ tests/ docs/

   # Check file sizes (<150 lines)
   find src -name "*.py" -exec wc -l {} \; | awk '$1 > 150'

   # Check docstrings
   grep -r "^def \|^class " src/ --include="*.py" | wc -l
   grep -r '"""' src/ --include="*.py" | wc -l
   ```

   **Score:** `Skill 2 = 7.0/10`

4. **Run Skill 3: Configuration & Security**

   ```bash
   # Check .env and config
   ls .env.example config.yaml
   grep -v "^#" .gitignore | grep -E "\.env|config\.yaml"

   # CRITICAL: Check for hardcoded secrets
   grep -r "api[_-]?key\s*=\s*['\"][^'\"]\{10,\}" src/ --include="*.py"
   grep -r "password\s*=\s*['\"][^'\"]\{5,\}" src/ --include="*.py"
   ```

   **Score:** `Skill 3 = 10/10` (or 0 if secrets found!)

5. **Run Skill 4: Testing & Quality**

   ```bash
   # Check tests exist
   ls tests/
   find tests -name "test_*.py" | wc -l

   # Check coverage
   ls .coverage coverage.xml htmlcov/

   # Check edge cases
   grep -ri "edge case\|boundary" tests/
   ```

   **Score:** `Skill 4 = 8/10`

6. **Run Skill 5: Research & Analysis**

   ```bash
   # Check for parameter investigation
   ls *.ipynb docs/*.ipynb
   grep -ri "parameter\|experiment" docs/ *.md

   # Check for LaTeX formulas
   grep -r "\$\$\|\\begin{equation}" *.ipynb *.md

   # Check visualizations
   find . -name "*.png" -o -name "*.jpg" | wc -l
   ```

   **Score:** `Skill 5 = 7.5/10`

7. **Run Skill 6: UI/UX**

   ```bash
   # Check for interface documentation
   grep -i "## Usage\|## Interface" README.md

   # Check for CLI help
   python main.py --help

   # Check for screenshots
   find docs -name "*.png" -o -name "*.jpg"
   ```

   **Score:** `Skill 6 = 7/10`

8. **Run Skill 7: Version Management**

   ```bash
   # Count commits
   git log --oneline --no-merges | wc -l

   # Check conventional commits
   git log --pretty=format:"%s" --no-merges | head -20

   # Check for prompts directory
   ls prompts/ .prompts/
   find prompts -name "*.md" | wc -l
   ```

   **Score:** `Skill 7 = 9/10`

9. **Run Skill 8: Costs & Pricing**

   ```bash
   # Check for cost analysis docs
   ls docs/COSTS.md COST_ANALYSIS.md
   grep -ri "cost.*analysis\|pricing" docs/

   # Check for cost tracking code
   grep -r "cost\|budget" src/ --include="*.py"
   ```

   **Score:** `Skill 8 = 6/10`

10. **Run Skill 9: Extensibility**

    ```bash
    # Check for abstract base classes
    grep -r "ABC\|abstractmethod" src/ --include="*.py"

    # Check file sizes
    find src -name "*.py" -exec wc -l {} \; | awk '$1 > 150'

    # Check for plugin architecture
    grep -r "plugin\|extension" src/ docs/
    ```

    **Score:** `Skill 9 = 8/10`

11. **Run Skill 10: Quality Standards**

    ```bash
    # Functional suitability
    # (Based on TRUE count from Step 3)

    # Performance considerations
    grep -ri "performance\|optimization" docs/

    # Error handling
    grep -r "try:\|except:" src/ --include="*.py" | wc -l

    # Security check (from Skill 3)
    ```

    **Score:** `Skill 10 = 7.5/10`

12. **Calculate Total Score**

    ```python
    skill_scores = {
        1: 8.5,
        2: 7.0,
        3: 10.0,
        4: 8.0,
        5: 7.5,
        6: 7.0,
        7: 9.0,
        8: 6.0,
        9: 8.0,
        10: 7.5
    }

    total_score = sum(skill_scores.values())  # 78.5
    final_grade = total_score  # Already out of 100
    ```

    **Record:** `Final Grade = 78.5/100` → `Performance Tier = Potential`

13. **Clean up**:
    ```bash
    cd ..
    rm -rf temp_assessment_63698
    ```

### Record Tier 2 Results in Excel:

Add additional columns or create a separate sheet:

| Participant | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | Total | Final | Tier |
|-------------|----|----|----|----|----|----|----|----|----|----|-------|-------|------|
| 63698 | 8.5 | 7 | 10 | 8 | 7.5 | 7 | 9 | 6 | 8 | 7.5 | 78.5 | 78.5 | Potential |

---

## STEP 6: Generate PDF Reports

For each student, create a PDF report.

### Tier 1 Report Template:

```markdown
# Assignment 3 Grading Report

**Student:** [Student Name]
**Participant ID:** [ID]
**Date:** 2025-12-01

---

## Grade Summary

- **Self-Grade (Claimed):** [self_grade]/100
- **Requirements Met:** [true_count]/22
- **Final Grade:** [final_grade]/100
- **Performance Tier:** [tier]

---

## Criteria Assessment

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Product Requirements Document | [TRUE/FALSE] |
| 2 | Architecture Document | [TRUE/FALSE] |
...
| 22 | Product Quality Characteristics | [TRUE/FALSE] |

**Score:** [true_count]/22 criteria met ([percentage]%)

---

## Missing Criteria

[List of FALSE criteria with brief explanation]

---

## Feedback

[Tier-appropriate constructive feedback]

---

## Recommendations

1. [Specific action]
2. [Specific action]
...
```

### Tier 2 Report Template:

```markdown
# Assignment 3 Grading Report

**Student:** [Student Name]
**Participant ID:** [ID]
**Date:** 2025-12-01

---

## Grade Summary

- **Self-Grade (Claimed):** [self_grade]/100
- **Requirements Met:** [true_count]/22
- **Final Grade:** [final_grade]/100
- **Performance Tier:** [tier]

---

## Skill Assessment (Rigorous Evaluation)

| Skill | Score | Pass |
|-------|-------|------|
| 1. Project Planning | [score]/10 | [✓/✗] |
| 2. Code Documentation | [score]/10 | [✓/✗] |
| 3. Configuration & Security | [score]/10 | [✓/✗] |
| 4. Testing & Quality | [score]/10 | [✓/✗] |
| 5. Research & Analysis | [score]/10 | [✓/✗] |
| 6. UI/UX | [score]/10 | [✓/✗] |
| 7. Version Management | [score]/10 | [✓/✗] |
| 8. Costs & Pricing | [score]/10 | [✓/✗] |
| 9. Extensibility | [score]/10 | [✓/✗] |
| 10. Quality Standards | [score]/10 | [✓/✗] |

**Total Score:** [total]/100

---

## Criteria Assessment

[Same 22-criteria table as Tier 1]

---

## Overall Feedback

[Tier-appropriate feedback addressing performance]

---

## Skill-by-Skill Breakdown

### Skill 1: Project Planning ([score]/10)
**Strengths:**
- [specific strength]

**Recommendations:**
- [specific improvement]

### Skill 2: Code Documentation ([score]/10)
...

[Continue for all 10 skills]

---

## Summary & Next Steps

[Concluding remarks and actionable next steps]
```

### Emoji Usage Guidelines (CRITICAL):

**The better the grade, the more emojis to use in the feedback:**

- **Excellence (90-100):** 🎉 Heavy emoji usage - 1 emoji every 20-30 words
  - Use: 🎉 ✨ 🌟 ⭐ 🚀 💯 🏆 👏 💪 🔥 ⚡ 🎯
  - Tone: Enthusiastic, celebratory, highly encouraging
  - Example: "Absolutely outstanding work! 🎉 Your implementation demonstrates exceptional understanding ✨ of professional software development practices. The comprehensive documentation 📚 and rigorous testing 🧪 showcase true excellence! 🌟"

- **Good (80-89):** 😊 Moderate emoji usage - 1 emoji every 50-70 words
  - Use: 😊 👍 ✅ 💡 📈 🎯 💪 🔍
  - Tone: Positive, encouraging, constructive
  - Example: "Great work overall! 👍 Your project shows solid understanding of the requirements ✅ with well-structured code and good documentation. A few areas could be enhanced 💡 to reach excellence level."

- **Potential (55-79):** 🙂 Light emoji usage - 1 emoji every 100-120 words
  - Use: 🙂 📝 🔧 💭 📊 ⚠️
  - Tone: Supportive, constructive, focused on improvement
  - Example: "Your submission shows promise 🙂 with several criteria met. However, there are important areas needing attention 📝 to meet professional standards. Focus on improving documentation and testing practices 🔧 for future assignments."

- **Below Standard (<55):** 📋 Minimal emoji usage - 1-2 emojis total
  - Use: 📋 ⚠️ 📝
  - Tone: Professional, constructive, clear action items
  - Example: "This submission needs significant improvement 📋. Several core requirements were not met. Please review the criteria carefully and focus on: [specific list]. Office hours available for guidance ⚠️."

### Generate Actual PDF Reports:

For each student, **write the actual PDF file** with personalized feedback.

**Process:**

1. **Prepare the content** using the template above with:
   - Actual student data filled in
   - Emoji density matching their grade tier
   - Specific strengths and weaknesses from assessment
   - Actionable recommendations

2. **Use Claude to generate personalized feedback** for each section:

```markdown
Generate feedback for Student ID 63698:
- Final Grade: 78.5/100 (Potential tier)
- Self-Grade: 100 (overestimated)
- TRUE Count: 22/22
- Skill Scores: [8.5, 7, 10, 8, 7.5, 7, 9, 6, 8, 7.5]
- Weaknesses: Skill 8 (Costs) only 6/10, Skill 2 (Documentation) only 7/10

Write 250-word overall feedback with:
1. Opening acknowledging their self-assessment (overconfident)
2. Praise for strengths (all 22 criteria met, perfect security)
3. Specific areas for improvement (cost analysis, documentation quality)
4. Encouragement for next assignment
5. Use LIGHT emoji density (1 per 100 words) - Potential tier
```

3. **Create the PDF file**:

```python
# Use ReportLab or similar library to generate PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

def generate_grading_report_pdf(student_data, output_path):
    """Generate professional PDF report with emoji-rich feedback."""

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    story.append(Paragraph(f"Assignment 3 Grading Report", styles['Title']))
    story.append(Spacer(1, 12))

    # Student info
    story.append(Paragraph(f"<b>Student:</b> {student_data['name']}", styles['Normal']))
    story.append(Paragraph(f"<b>Participant ID:</b> {student_data['id']}", styles['Normal']))

    # Grade Summary with appropriate emojis
    emoji_prefix = get_emoji_for_grade(student_data['final_grade'])
    story.append(Paragraph(f"{emoji_prefix} <b>Final Grade: {student_data['final_grade']}/100</b>", styles['Heading1']))

    # Add all sections with tier-appropriate emoji density
    feedback_text = generate_personalized_feedback(student_data)
    story.append(Paragraph(feedback_text, styles['Normal']))

    # Build PDF
    doc.build(story)
```

4. **Save to student folder**:

```bash
# Output file path
WorkSubmissions03/Participant_63698_assignsubmission_file/grading_report.pdf
```

### Example Feedback by Tier:

**Excellence (95/100) - Heavy Emojis:**
```
🎉 Exceptional work! Your submission demonstrates mastery of professional software
development practices! 🌟 The comprehensive PRD and architecture documentation 📚
provide crystal-clear project vision. Your code quality is outstanding ✨ with
perfect modularity and extensive testing coverage 🧪. The security implementation
🔒 shows excellent attention to detail. Your research analysis 📊 with detailed
parameter studies and beautiful visualizations 📈 goes above and beyond! The cost
tracking system 💰 demonstrates real-world thinking. Minor improvement opportunity:
enhance the extensibility documentation 📝 with more plugin examples. Overall, this
is exceptional work that sets the standard for the class! 🏆 Keep up this fantastic
momentum! 🚀
```

**Good (82/100) - Moderate Emojis:**
```
Great work on this assignment! 👍 Your project demonstrates solid understanding of
the requirements with well-structured code and comprehensive documentation. The PRD
clearly outlines the project vision, and your architecture diagrams effectively
communicate the system design. Testing coverage is good with unit tests covering
core functionality ✅. The repository shows consistent development practices with
regular commits and meaningful messages. Areas for improvement: The cost analysis
could be more detailed with specific pricing breakdowns 💡. Some code files exceed
the 150-line limit, consider refactoring for better maintainability. The research
notebook would benefit from more mathematical rigor in the analysis 📊. Overall,
strong work with clear path to excellence level in future assignments!
```

**Potential (67/100) - Light Emojis:**
```
Your submission shows understanding of several key concepts 🙂. The basic project
structure is in place with source code organized appropriately. However, there are
important areas needing attention to meet professional standards. The PRD exists but
lacks detailed functional requirements and success metrics. Documentation is minimal
with the README missing installation and usage instructions. Testing coverage is
insufficient with only basic unit tests and no edge case validation. The repository
shows irregular commit patterns without following conventional commit format 📝.
Security practices need improvement - configuration management is lacking. For future
assignments, focus on: 1) Writing comprehensive documentation before coding, 2)
Implementing thorough test coverage including edge cases, 3) Following git best
practices with frequent, well-described commits, 4) Creating detailed technical
planning documents. Office hours are available if you need guidance on any of these
areas 🔧.
```

**Below (48/100) - Minimal Emojis:**
```
This submission needs significant improvement 📋. Core requirements were not met:
PRD is missing entirely, no architecture documentation, minimal README with no usage
instructions, code lacks structure and organization, no tests implemented, repository
has only 3 commits, no research analysis or cost documentation. Missing criteria:
[list of 14 FALSE items]. To improve: 1) Review SubmissionRequirements.txt carefully
and ensure each criterion is addressed, 2) Start with planning documents (PRD,
architecture) before writing code, 3) Implement comprehensive testing from the start,
4) Commit frequently with descriptive messages, 5) Document all aspects of your
project thoroughly. Please attend office hours for guidance on project structure and
development practices ⚠️. Next submission must show substantial improvement in these
fundamental areas.
```

---

## STEP 7: Final Excel Update

Update the master Excel file with all final grades.

### Columns:

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Participant ID | Group Code | Student 1 | Student 2 | GitHub | Self-Grade | TRUE Count | Final Grade | Tier |
| 63698 | G42 | Fouad | | url | 100 | 22 | 78.5 | Potential |
| 63699 | G21 | Jane | John | url | 85 | 18 | 75.0 | Potential |
| 63700 | G18 | Bob | | url | 75 | 12 | 54.5 | Below |

### Add Statistics Sheet:

Create a second sheet called "Statistics":

```
Average Final Grade: [avg]
Median: [median]
Std Dev: [stdev]
Min: [min]
Max: [max]

Distribution:
Excellence (90-100): [count] ([percentage]%)
Good (80-89): [count] ([percentage]%)
Potential (55-79): [count] ([percentage]%)
Below (<55): [count] ([percentage]%)

Tier Breakdown:
Tier 1 (Self < 80): [count] students
Tier 2 (Self ≥ 80): [count] students
```

---

## STEP 8: Generate PDF Reports & Summary

**CRITICAL:** Actually write and save the PDF files - don't just report!

### For Each Student:

1. **Generate personalized feedback** based on their tier and grade
2. **Apply appropriate emoji density** (Excellence = heavy, Good = moderate, Potential = light, Below = minimal)
3. **Write the actual PDF file** to their folder
4. **Include all sections:**
   - Header with student info
   - Grade summary (self-grade, TRUE count, final grade, tier)
   - Criteria table (22 requirements with TRUE/FALSE)
   - Overall feedback (250-400 words with emojis)
   - Skill breakdown (if Tier 2)
   - Recommendations and next steps

### Generate PDFs:

```python
# For each student in Excel:
for student in all_students:
    # Prepare data
    student_data = {
        'name': student['Student 1'],
        'id': student['Participant ID'],
        'self_grade': student['Self-Grade'],
        'true_count': student['TRUE Count'],
        'final_grade': student['Final Grade'],
        'tier': student['Performance Tier'],
        'criteria': load_criteria_from_assessment(student['id']),
        'skill_scores': student['Skill Scores'] if Tier 2 else None
    }

    # Generate personalized feedback with appropriate emoji density
    feedback = generate_feedback_with_emojis(student_data)

    # Create PDF
    output_path = f"WorkSubmissions03/Participant_{student['id']}_assignsubmission_file/grading_report.pdf"
    create_pdf_report(student_data, feedback, output_path)

    print(f"✅ Generated PDF for {student['id']}: {student['Final Grade']}/100")
```

### Then Provide Summary to User:

```
✅ Grading Complete for Assignment 3

📊 Summary:
- Total Students: 35
- Average Grade: 72.3/100
- Grade Range: 45.5 - 95.5

📈 Distribution:
- Excellence (90-100): 3 students (8.6%) 🎉
- Good (80-89): 8 students (22.9%) 👍
- Potential (55-79): 18 students (51.4%) 🙂
- Below (<55): 6 students (17.1%) 📋

🔍 Tier Breakdown:
- Tier 1 (Simple): 15 students
- Tier 2 (10 Skills): 20 students

📁 Files Generated:
- grades_assignment3.xlsx (master grade sheet with all columns)
- 35 × repo_assessment.md (22 criteria TRUE/FALSE in each folder)
- 35 × grading_report.pdf (personalized feedback with emojis in each folder) ✨

⚠️ Issues Encountered:
- 2 repositories inaccessible (marked as 0)
- 1 student missing self-grade (used conservative default)

📧 Emoji Usage Summary:
- Excellence PDFs: Heavy emojis (1 per 20-30 words) 🎉✨🌟
- Good PDFs: Moderate emojis (1 per 50-70 words) 👍😊
- Potential PDFs: Light emojis (1 per 100-120 words) 🙂📝
- Below PDFs: Minimal emojis (1-2 total) 📋⚠️

✨ All PDF reports generated and saved! Ready for review!
```

---

## Commands Quick Reference

```bash
# Step 1: Extract to Excel
python .claude/skills/grade-extractor/extract_grades.py WorkSubmissions03 grades_assignment3.xlsx

# Step 2: Update Excel (per student)
python .claude/skills/grade-extractor/update_excel.py grades_assignment3.xlsx <id> "<group>" "<s1>" "<s2>" "<github>" "<grade>"

# Step 3: Assess Repository
/git-repo-assessment <github-url>

# Count TRUE criteria
grep "| TRUE |" WorkSubmissions03/Participant_XXXXX_assignsubmission_file/repo_assessment.md | wc -l

# Step 5b: Clone for skills assessment
git clone <github-url> temp_assessment_<id>

# Run skill checks (see individual SKILL.md files)
cat .claude/skills/1-project-planning/SKILL.md

# Cleanup
rm -rf temp_assessment_<id>
```

---

## Error Handling

### Repository Not Accessible:
```
Record in Excel: Final Grade = 0, Notes = "Repository inaccessible"
Email user: "Student [ID] repository cannot be accessed. Please follow up."
```

### PDF Cannot Be Read:
```
Skip extraction, note in Excel: "PDF unreadable - manual review needed"
```

### Missing Self-Grade:
```
Option 1: Use conservative default (60)
Option 2: Calculate from TRUE count: (TRUE/22) × 100
Option 3: Ask user
```

### Skill Assessment Errors:
```
If command fails, score that component as 0
Note the issue in the skill breakdown
Continue with other skills
```

---

## Tips for Efficiency

1. **Batch Processing:** Process 5 students at a time
2. **Parallel Work:** Run repository assessments while extracting PDFs
3. **Progress Updates:** Report every 5 students
4. **Error Tracking:** Keep a list of issues to report at the end
5. **Quality Checks:** Spot-check a few random assessments manually

---

## Final Checklist

Before reporting completion:

- [ ] All students have entry in Excel
- [ ] All students have repo_assessment.md
- [ ] All Tier 1 students have final grade calculated
- [ ] All Tier 2 students have all 10 skill scores
- [ ] All students have grading_report.pdf
- [ ] Statistics calculated
- [ ] Excel file saved
- [ ] Issues documented

---

**Last Updated:** 2025-12-01
**Next:** Use this document every time user asks to grade submissions

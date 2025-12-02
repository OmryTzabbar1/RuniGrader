# GraderPDF Skill

**Version:** 1.0.0

## Purpose

Generates comprehensive, multi-page PDF grade breakdowns that show exactly where students earned and lost points. This allows instructors to:
- Answer detailed questions about grading decisions
- Defend grades with specific evidence
- Help students understand exactly what to improve

## Features

### Multi-Page Detailed Breakdown
- **Page 1:** Executive summary with overall score, performance tier, and skills summary table
- **Pages 2-11:** One page per skill with:
  - Points breakdown table showing each criterion
  - What was found (evidence)
  - What was missing (gaps)
  - How to improve (actionable recommendations)
- **Final Page:** Overall assessment with key strengths, critical gaps, and recommended actions

### Visual Design
- Color-coded scoring (green for good, red for poor, orange for fair)
- Status indicators (✓ Excellent, ⚠ Fair, ✗ Poor)
- Professional tables with alternating row colors
- Clear typography hierarchy

### Detailed Point Attribution
Shows exactly where points were earned/lost for each criterion:
- PRD.md exists: 2.0 points
- ARCHITECTURE.md exists: 5.0 points
- No hardcoded secrets: 5.0 points (critical)
- Test files exist: 3.0 points
- etc.

## Usage

### Command Line

```bash
python .claude/skills/grader-pdf/generate_detailed_breakdown.py \
    <assessment_json_path> \
    <output_pdf_path> \
    [assignment_name]
```

### Example

```bash
# Generate breakdown for student 48951
python .claude/skills/grader-pdf/generate_detailed_breakdown.py \
    assessments_tier2_assignment2/tier2_assessment_48951.json \
    WorkSubmissions02/Participant_48951_assignsubmission_file/Detailed_Grade_Breakdown_48951.pdf \
    "Assignment 2"
```

### Using as a Skill

The skill can be invoked through Claude Code:

```
grader-pdf assessments_tier2_assignment2/tier2_assessment_48951.json WorkSubmissions02/Participant_48951_assignsubmission_file "Assignment 2"
```

## Input Requirements

### Assessment JSON Structure

The skill expects a Tier 2 assessment JSON file with the following structure:

```json
{
  "student_id": "48951",
  "assignment": "Assignment 2",
  "repository_name": "repo_name",
  "assessment_date": "2025-12-02",
  "skills": {
    "project_planning": 0.0,
    "code_documentation": 6.5,
    ...
  },
  "skill_details": {
    "project_planning": {
      "score": 0.0,
      "max_score": 10.0,
      "prd_found": false,
      "architecture_found": false,
      "notes": ["...", "..."],
      "recommendations": ["...", "..."]
    },
    ...
  },
  "total_score": 20.5,
  "performance_tier": "Below Standard",
  "recommended_actions": {
    "immediate": ["...", "..."],
    "high_priority": ["...", "..."]
  }
}
```

## Output

### PDF Contents

**Page 1: Executive Summary**
- Student ID, repository name, assessment date
- Large, prominent final score
- Performance tier with color coding
- Skills summary table showing all 10 skills

**Pages 2-11: Detailed Skill Breakdowns**

Each skill page contains:

1. **Skill Header**
   - Skill name and number
   - Score out of 10 points
   - Status indicator

2. **Points Breakdown Table**
   ```
   Criterion               | Max Points | Earned | Status
   ----------------------- | ---------- | ------ | ------
   PRD.md exists          |    2.0     |  0.0   |   ✗
   ARCHITECTURE.md exists |    5.0     |  0.0   |   ✗
   Problem Statement      |    1.0     |  0.0   |   ✗
   Functional Reqs        |    1.5     |  0.0   |   ✗
   Success Metrics        |    0.5     |  0.0   |   ✗
   ----------------------- | ---------- | ------ | ------
   TOTAL                  |   10.0     |  0.0   |
   ```

3. **What Was Found**
   - Bullet list of positive findings
   - Specific files/evidence found

4. **What Was Missing**
   - Bullet list of gaps
   - Specific items not found
   - Point deductions explained

5. **How to Improve**
   - Numbered list of actionable recommendations
   - Shows potential points to gain

**Final Page: Overall Summary**
- Key strengths (skills with 8+ points)
- Critical gaps (skills with <5 points)
- Immediate priority actions
- High priority actions

### File Size

Typical output: 15-25 KB for a 12-page PDF

## Skill Criteria Definitions

### Skill 1: Project Planning (10 points)
- PRD.md exists: 2.0 points
- ARCHITECTURE.md exists: 5.0 points
- Problem Statement: 1.0 point
- Functional Requirements: 1.5 points
- Success Metrics: 0.5 points

### Skill 2: Code Documentation (10 points)
- README.md >1KB: 3.0 points
- Installation instructions: 1.0 point
- Usage examples: 1.0 point
- Code structure documented: 2.0 points
- Python docstrings (>50%): 3.0 points

### Skill 3: Configuration & Security (10 points)
- No hardcoded secrets (CRITICAL): 5.0 points
- .env.example exists: 2.0 points
- .gitignore exists: 1.0 point
- Uses environment variables: 2.0 points

### Skill 4: Testing & Quality (10 points)
- Test files exist: 3.0 points
- Multiple test files (>3): 2.0 points
- Test framework configured: 2.0 points
- Test functions (>10): 3.0 points

### Skill 5: Research & Analysis (10 points)
- Jupyter notebooks exist: 4.0 points
- Multiple notebooks (>2): 2.0 points
- Has visualizations/plots: 2.0 points
- Analysis documentation: 2.0 points

### Skill 6: UI/UX (10 points)
- Screenshots/images (1+): 3.0 points
- Screenshots/images (5+): 3.0 points additional
- UI documentation: 2.0 points
- User guide exists: 2.0 points

### Skill 7: Version Management (10 points)
- Git commits >10: 2.0 points
- Meaningful commit messages: 2.0 points
- PROMPT_BOOK.md exists: 5.0 points
- Branching strategy: 1.0 point

### Skill 8: Costs & Pricing (10 points)
- Cost analysis document: 5.0 points
- Cost mentions in docs: 3.0 points
- Budget tracking: 2.0 points

### Skill 9: Extensibility (10 points)
- Plugin/extension system: 3.0 points
- Modular structure (3+ dirs): 3.0 points
- Interfaces/APIs: 2.0 points
- Extension documentation: 2.0 points

### Skill 10: Quality Standards (10 points)
- Linting configuration: 2.0 points
- CI/CD pipeline: 3.0 points
- Code style guide: 2.0 points
- Pre-commit hooks: 2.0 points
- Project setup file: 1.0 point

## Performance Tiers

- **Excellence:** 90-100 points (Green)
- **Good:** 80-89 points (Light Green)
- **Potential:** 55-79 points (Orange)
- **Below Standard:** 0-54 points (Red)

## Dependencies

- Python 3.7+
- reportlab

```bash
pip install reportlab
```

## Integration with Grading Workflow

### Recommended Workflow

1. **Run Tier 2 Assessment** (using tier2-orchestrator skill)
   - Generates `tier2_assessment_<student_id>.json`

2. **Generate Detailed Breakdown** (using grader-pdf skill)
   - Reads assessment JSON
   - Produces comprehensive PDF

3. **Deliver to Student**
   - Student receives multi-page breakdown
   - Can see exactly where points were lost
   - Has actionable improvement steps

### Batch Processing

For processing multiple students:

```python
import os
from pathlib import Path

assessment_dir = "assessments_tier2_assignment2"
submissions_dir = "WorkSubmissions02"

for json_file in Path(assessment_dir).glob("tier2_assessment_*.json"):
    student_id = json_file.stem.replace("tier2_assessment_", "")
    student_folder = Path(submissions_dir) / f"Participant_{student_id}_assignsubmission_file"

    output_pdf = student_folder / f"Detailed_Grade_Breakdown_{student_id}.pdf"

    os.system(f'python .claude/skills/grader-pdf/generate_detailed_breakdown.py "{json_file}" "{output_pdf}" "Assignment 2"')
```

## Answering Student Questions

With this breakdown, you can easily answer questions like:

**"Why did I get 0 points for Project Planning?"**
→ Point to Page 2 showing:
- PRD.md not found (0/2 points)
- ARCHITECTURE.md not found (0/5 points)
- No planning documents (0/3 points)

**"How can I improve my Testing score?"**
→ Point to Page 5 showing:
- Add test files (3.0 points)
- Configure pytest (2.0 points)
- Write 10+ test functions (3.0 points)

**"What exactly counts as documentation?"**
→ Point to Page 3 criteria table showing each requirement

## Benefits

### For Instructors
- **Transparency:** Every point decision is documented
- **Efficiency:** No need to write individual explanations
- **Consistency:** All students judged by same criteria
- **Defense:** Can point to specific evidence for grade appeals

### For Students
- **Clarity:** Understand exactly what was missing
- **Actionable:** Know specifically what to improve
- **Fair:** See objective criteria applied consistently
- **Educational:** Learn professional software standards

## Version History

- **1.0.0** (2025-12-02)
  - Initial release
  - 12-page detailed breakdowns
  - Color-coded scoring
  - Criterion-level point attribution

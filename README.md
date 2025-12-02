# RuniGrader

Automated grading system for LLM/Multi-Agent Orchestration course assignments using Tier 2 assessment framework.

## Overview

RuniGrader is a comprehensive automated grading system that evaluates student submissions across 10 key skills in software engineering. It generates detailed assessments, personalized feedback, and professional PDF grade reports.

## Features

### 10-Skill Assessment Framework (Tier 2)

Each skill is worth 10 points (100 points total):

1. **Project Planning** - PRD documents, architecture diagrams
2. **Code Documentation** - README quality, docstrings
3. **Config & Security** - Secret scanning, .gitignore, environment variables
4. **Testing Quality** - Test count, assertions, coverage, CI/CD
5. **Research & Analysis** - Jupyter notebooks OR comprehensive markdown research
6. **UI/UX Quality** - Screenshots, interface documentation
7. **Version Management** - Git commits, branching, prompt documentation
8. **Costs & Pricing** - Cost analysis, budget management
9. **Extensibility** - Plugin systems, modularity, interfaces
10. **Quality Standards** - Linting, CI/CD pipelines, pre-commit hooks

**Passing Threshold:** 60/100

### Automated Grading Tools

- **Python Assessment Scripts** - Automated analysis for all 10 skills
- **Student-Facing PDF Reports** - Professional, encouraging feedback with grade-appropriate emojis
- **Excel Summary Generator** - Comprehensive grading spreadsheet with statistics
- **Batch Processing** - Grade multiple submissions efficiently

### Grade Report Features

- **Emoji-based feedback:**
  - A-level (90-100%): Lots of emojis 🎉🏆⭐🔥✨
  - B-level (80-89%): Moderate emojis ✅👍💡📈
  - C-level (70-79%): Fewer emojis ✓⚡
  - D-level (60-69%): Minimal emojis ✓
  - F-level (<60%): No emojis, serious tone

- **Personalized content:**
  - Key strengths (bulleted)
  - Areas for improvement (actionable)
  - Encouraging closing message
  - Professional formatting

## Project Structure

```
.claude/skills/
├── 1-project-planning/
│   └── find_planning_docs.py
├── 2-code-documentation/
│   └── find_documentation.py
├── 3-config-security/
│   └── scan_secrets.py
├── 4-testing-quality/
│   └── analyze_tests.py
├── 5-research-analysis/
│   └── find_research.py
├── 6-ui-ux/
│   └── find_ui_docs.py
├── 7-version-management/
│   └── analyze_git_history.py
├── 8-costs-pricing/
│   └── find_cost_analysis.py
├── 9-extensibility/
│   └── analyze_extensibility.py
├── 10-quality-standards/
│   └── find_quality_tools.py
└── grade-report-generator/
    ├── generate_student_report.py
    ├── README.md
    └── SUMMARY.md

docs/                           # Documentation files
create_grading_excel.py         # Excel summary generator
Assignment3_Grading_Summary.xlsx # Example grading spreadsheet
```

## Usage

### Running Individual Skill Assessments

```bash
# Skill 1: Project Planning
python .claude/skills/1-project-planning/find_planning_docs.py /path/to/repo

# Skill 2: Code Documentation
python .claude/skills/2-code-documentation/find_documentation.py /path/to/repo

# ... (repeat for all 10 skills)
```

### Generating Student PDF Reports

```bash
python .claude/skills/grade-report-generator/generate_student_report.py \
  --student-id "38981" \
  --team "Team Name" \
  --grade 94 \
  --repository "https://github.com/user/repo" \
  --output-dir "./output" \
  --strengths "Strength 1|Strength 2|Strength 3" \
  --improvements "Improvement 1|Improvement 2" \
  --assignment "Assignment 3: Agentic Turing Machine"
```

### Creating Excel Grading Summary

```bash
python create_grading_excel.py
```

Generates: `Assignment3_Grading_Summary.xlsx` with:
- All student grades
- Team information
- Key strengths/weaknesses
- Auto-calculated statistics
- Color-coded grades

## Assessment Workflow

1. **Clone student repository**
2. **Run all 10 skill assessments**
3. **Calculate final grade** (sum of all skill scores)
4. **Generate student-facing PDF report**
5. **Update Excel grading summary**

## Key Assessment Criteria

### What Makes Top Students Excel (90+):
- Comprehensive testing (400+ tests)
- Excellent documentation (1000+ docstrings, 10,000+ word READMEs)
- Research component (Jupyter notebooks OR comprehensive markdown)
- Cost analysis with budget tracking
- Professional UI (20+ screenshots)
- CI/CD pipelines
- Strong git history (50+ commits)

### Common Failure Points:
- Missing research (Skill 5 = 0/10)
- No cost analysis (Skill 8 = 0/10)
- Poor security (hardcoded secrets)
- Minimal testing (<20 tests)
- Weak git history (1-2 commits)

## Skills Documentation

Each skill has detailed assessment criteria:
- **Skill 5 (Research)**: Accepts both Jupyter notebooks AND comprehensive markdown documentation
- **Skill 7 (Version Management)**: 50% weight on prompt documentation
- **Skill 10 (Quality Standards)**: Pre-commit hooks and CI/CD pipelines

See individual skill folders for complete rubrics.

## Example Results

From actual grading session (46 students):

| Grade Range | Count | Percentage |
|-------------|-------|------------|
| A (90-100) | 4 | 8.7% |
| B (80-89) | 6 | 13.0% |
| C (70-79) | 4 | 8.7% |
| D (60-69) | 29 | 63.0% |
| F (<60) | 3 | 6.5% |

**Highest Score:** 94/100
- 500 tests, 1109 docstrings (96% coverage)
- 19,411-word README
- Dual-interface (Streamlit + Flask)
- 3 CI/CD workflows
- 28 screenshots

## Dependencies

```bash
pip install openpyxl reportlab
```

## Configuration

Skills can be customized by editing:
- Assessment scripts in `.claude/skills/*/`
- PDF feedback tone in `generate_student_report.py`
- Excel format in `create_grading_excel.py`

## Contributing

This system is designed for academic use. Contributions welcome:
- New skill assessments
- Improved detection algorithms
- Better feedback generation
- Additional output formats

## License

Educational use only. Developed for LLM/Multi-Agent Orchestration course.

## Version History

- **v2.1.0** - Skill 5 accepts markdown research documentation
- **v2.0.0** - Full Tier 2 assessment system with 10 skills
- **v1.0.0** - Initial release with basic grading

## Contact

Created for academic grading purposes.
Repository: https://github.com/OmryTzabbar1/RuniGrader.git

---

**Note:** This grading system emphasizes both technical excellence and professional software engineering practices. Students are evaluated not just on functionality, but on documentation, testing, security, and maintainability.

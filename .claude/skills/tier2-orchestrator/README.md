# Tier 2 Orchestrator - Grading System Guide

## Overview

The Tier 2 Orchestrator is a parallel skill invocation system that automatically assesses student submissions across 10 different dimensions. It runs all skills concurrently using ThreadPoolExecutor for efficient grading.

## Architecture

```
tier2-orchestrator/
├── orchestrate.py           # Main orchestrator script
├── clone_repo.py           # Repository cloning utility
└── README.md               # This file

assessments_tier2_assignment1/  # Output directory for JSON results
└── tier2_assessment_{student_id}.json

WorkSubmissions01/
└── Participant_{id}_assignsubmission_file/
    ├── submission_info.xlsx          # Contains GitHub repo URL
    ├── {repo_name}/                  # Cloned repository
    ├── Detailed_Grade_Breakdown_{id}.pdf
    └── Grade_Report_{id}.pdf
```

## The 10 Skills

Each skill is worth 10 points (total: 100 points):

1. **project-planning** (10 pts)
   - PRD.md with Problem Statement, Functional Requirements, Success Metrics (5 pts)
   - ARCHITECTURE.md or architectural documentation in README (5 pts, partial credit: 2-3 pts)

2. **code-documentation** (10 pts)
   - README.md completeness and quality
   - Inline code documentation
   - API documentation

3. **config-security** (10 pts)
   - No hardcoded secrets in production code (2 pts) - **test files excluded**
   - .env.example exists (2 pts)
   - .gitignore includes .env (2 pts)
   - Uses environment variables (2 pts) - **1 pt if documented in README only**
   - Good .gitignore coverage (2 pts)

4. **testing-quality** (10 pts)
   - Test files exist (3 pts)
   - Multiple test files ≥1 (2 pts) - **one test folder is sufficient**
   - Test framework configured (2 pts)
   - Test count >10 (3 pts, partial credit available)

5. **research-analysis** (10 pts)
   - RESEARCH.md or research documentation exists
   - Quality and depth of research analysis

6. **ui-ux** (10 pts)
   - UI implementation quality
   - User experience considerations
   - Interface design

7. **version-management** (10 pts)
   - Git commit history quality
   - Branching strategy
   - Commit message quality

8. **costs-pricing** (10 pts)
   - Cost analysis documentation
   - API pricing considerations
   - Budget planning
   - **Searches**: README, .md files, .py, .js, .ipynb, .json

9. **extensibility** (10 pts)
   - Code modularity
   - Plugin/extension architecture
   - Future-proofing

10. **quality-standards** (10 pts)
    - Code style guide (3 pts) - **primary focus**
    - Pre-commit hooks (1 pt)
    - Linting configuration (2 pts)
    - Type hints/annotations (2 pts)
    - Code review practices (2 pts)

## Performance Tiers

- **Excellence**: 90-100 points
- **Good**: 80-89 points
- **Potential**: 55-79 points
- **Below Standard**: 0-54 points

## Before Starting Grading

### Essential Files to Read

1. **Grading Spreadsheet**: `grading_summary_assignment1.xlsx`
   - Located in: `WorkSubmissions01/`
   - Contains: Student IDs, self-grades, submission metadata
   - Use to identify which students to grade

2. **Previous Assessment Results** (if re-grading):
   - `assessments_tier2_assignment1/tier2_assessment_{student_id}.json`
   - Review to understand previous scores and issues

3. **Submission Metadata**: `submission_info.xlsx` (per student)
   - Located in: `WorkSubmissions01/Participant_{id}_assignsubmission_file/`
   - Contains: GitHub repository URL, submission details
   - **Critical**: Used by clone_repo.py to auto-clone repositories

### Understanding Submission Structure

Each student submission folder contains:
- `submission_info.xlsx` - metadata including GitHub repo URL
- Optionally: cloned repository folder (auto-created if missing)
- Generated PDFs (placed in submission folder, NOT in repo)

## How to Use the Orchestrator

### Basic Usage

```bash
python ".claude/skills/tier2-orchestrator/orchestrate.py" <repo_path> <student_id> [assignment_name]
```

### Parameters

- `<repo_path>`: Path to student repository OR student submission folder
- `<student_id>`: Student identifier (e.g., 38950)
- `[assignment_name]`: Optional, defaults to "Assignment 1"

### Examples

```bash
# Grade with existing repository
python ".claude/skills/tier2-orchestrator/orchestrate.py" \
  "WorkSubmissions01/Participant_38950_assignsubmission_file/repo" \
  38950 \
  "Assignment 1"

# Grade with auto-cloning (repo will be cloned from submission_info.xlsx)
python ".claude/skills/tier2-orchestrator/orchestrate.py" \
  "WorkSubmissions01/Participant_38951_assignsubmission_file/nonexistent-repo" \
  38951 \
  "Assignment 1"
```

## Auto-Cloning Feature

The orchestrator automatically clones repositories if they don't exist:

1. Reads `submission_info.xlsx` from student folder
2. Extracts "GitHub Repository" URL
3. Handles complex URLs:
   - Removes `.git` suffix
   - Handles `/tree/branch/subfolder` paths
   - Handles `/blob/branch/file` paths
4. Clones to student folder with repository name
5. Returns path to cloned repository

### URL Cleaning Examples

- `https://github.com/user/repo.git` → `https://github.com/user/repo`
- `https://github.com/user/repo/tree/main/subfolder` → `https://github.com/user/repo`
- `https://github.com/user/repo/blob/main/file.py` → `https://github.com/user/repo`

## Output Files

### 1. JSON Assessment
**Location**: `assessments_tier2_assignment1/tier2_assessment_{student_id}.json`

**Contents**:
```json
{
  "student_id": "38950",
  "assignment": "Assignment 1",
  "repository_name": "repo-name",
  "repository_path": "full/path/to/repo",
  "assessment_date": "2025-12-02",
  "orchestration_method": "parallel_skill_invocation",
  "orchestrator_version": "3.0.0",
  "skills": {
    "project_planning": 6.0,
    "code_documentation": 10.0,
    ...
  },
  "skill_details": {
    "project_planning": {
      "score": 6.0,
      "notes": [...],
      "recommendations": [...]
    },
    ...
  },
  "total_score": 56.5,
  "final_grade": 56.5,
  "performance_tier": "Potential",
  "tier_description": "55-79 points",
  "recommended_actions": {
    "immediate": [...],
    "high_priority": [...]
  },
  "overall_assessment": {
    "summary": "...",
    "strengths": [...],
    "weaknesses": [...]
  }
}
```

### 2. Detailed Grade Breakdown PDF
**Location**: `WorkSubmissions01/Participant_{id}_assignsubmission_file/Detailed_Grade_Breakdown_{student_id}.pdf`

**Generated by**: `.claude/skills/grader-pdf/generate_detailed_breakdown.py`

**Contents**:
- Overall score and tier
- Detailed breakdown of all 10 skills
- Notes and recommendations per skill
- Visual scoring chart

### 3. Student Grade Report PDF
**Location**: `WorkSubmissions01/Participant_{id}_assignsubmission_file/Grade_Report_{student_id}.pdf`

**Generated by**: `.claude/skills/grade-report-generator/generate_student_report.py`

**Contents**:
- Summary grade report
- Key strengths and areas for improvement
- Repository information
- Assignment details

## Batch Grading Workflow

### Step 1: Identify Students
Read `grading_summary_assignment1.xlsx` to get list of student IDs.

### Step 2: Grade in Batches
Process students in groups of 3-5 for progress tracking:

```bash
# Batch 1
python orchestrate.py "WorkSubmissions01/Participant_38950_assignsubmission_file/repo" 38950 "Assignment 1"
python orchestrate.py "WorkSubmissions01/Participant_38951_assignsubmission_file/repo" 38951 "Assignment 1"
python orchestrate.py "WorkSubmissions01/Participant_38952_assignsubmission_file/repo" 38952 "Assignment 1"

# Batch 2
python orchestrate.py "WorkSubmissions01/Participant_38953_assignsubmission_file/repo" 38953 "Assignment 1"
...
```

### Step 3: Handle Missing Repositories
The orchestrator will automatically attempt to clone missing repositories. If cloning fails:
- Check `submission_info.xlsx` for valid GitHub URL
- Verify repository is public or accessible
- Skip student if no repository exists

### Step 4: Review Results
Check JSON files in `assessments_tier2_assignment1/` and PDFs in submission folders.

## Re-grading Process

To re-grade students with updated skills:

### Step 1: Delete Old Assessments
```bash
# Delete JSON files
del assessments_tier2_assignment1\tier2_assessment_38950.json
del assessments_tier2_assignment1\tier2_assessment_38951.json
...

# Delete PDFs (in each student folder)
del WorkSubmissions01\Participant_38950_assignsubmission_file\Detailed_Grade_Breakdown_38950.pdf
del WorkSubmissions01\Participant_38950_assignsubmission_file\Grade_Report_38950.pdf
...
```

### Step 2: Re-run Orchestrator
Run orchestration commands again with updated skills.

## Skill Update Guidelines

When updating individual skills:

1. **Maintain Scoring Structure**: Each skill should total 10 points
2. **Add Partial Credit**: Reward partial implementations
3. **Update Documentation**: Reflect changes in skill assess.py docstrings
4. **Test on Known Students**: Verify changes with known submissions (e.g., 38981)
5. **Consider Impact**: Major changes may require re-grading all students

### Recent Skill Updates

- **config-security**: Now excludes test files from secret scanning (test credentials are acceptable)
- **config-security**: Hardcoded secrets now deduct 2 points (not entire score)
- **config-security**: Environment variables documented in README gets 1pt (out of 2pts); actual usage gets full 2pts
- **testing-quality**: Changed from >3 test files to ≥1 (one test folder sufficient)
- **costs-pricing**: Enhanced search to include README, .py, .js, .ipynb, .json files
- **quality-standards**: Rebalanced to prioritize code style guides (3 pts) over pre-commit hooks (1 pt)
- **project-planning**: Architecture can be documented in README instead of separate ARCHITECTURE.md (full 5pts if well-documented)
- **project-planning**: Added partial credit (2-3 pts) for architectural info without dedicated file

## Common Issues and Solutions

### Issue: Repository Not Found
**Solution**: Orchestrator will auto-clone from `submission_info.xlsx`. Ensure Excel file exists with valid GitHub URL.

### Issue: GitHub URL with Subdirectory
**Example**: `https://github.com/user/repo/tree/main/subfolder`
**Solution**: `clone_repo.py` automatically cleans URLs to clone full repository.

### Issue: PDFs in Wrong Location
**Solution**: Updated orchestrator to always place PDFs in parent submission folder (Participant_*), not in repo.

### Issue: Test Files Flagged as Security Issues
**Solution**: `scan_secrets.py` now excludes test files (test_*.py, *_test.py, tests/).

### Issue: Low Test Quality Score
**Solution**: Changed requirement from >3 test files to ≥1 to reflect that one comprehensive test folder is sufficient.

## Orchestrator Version History

- **v3.0.0** (Current)
  - Parallel skill invocation using ThreadPoolExecutor
  - Automatic repository cloning from submission_info.xlsx
  - PDF generation in submission folders
  - Enhanced error handling and reporting
  - Partial credit system across skills

- **v2.x** - Previous versions
  - Sequential skill execution
  - Manual repository management

## Performance Metrics

- **Average Grading Time**: 30-60 seconds per student (with parallel execution)
- **Concurrent Skills**: 10 (via ThreadPoolExecutor with max_workers=10)
- **Timeout per Skill**: 30 seconds
- **Total Timeout**: 2 minutes per orchestration

## Integration with Other Tools

### Grader PDF Skill
```bash
python ".claude/skills/grader-pdf/generate_detailed_breakdown.py" \
  <json_file> \
  <output_pdf> \
  <assignment_name>
```

### Grade Report Generator
```bash
python ".claude/skills/grade-report-generator/generate_student_report.py" \
  --student-id <id> \
  --team <team_name> \
  --grade <grade> \
  --repository <repo_name> \
  --output-dir <output_dir> \
  --strengths <strengths> \
  --improvements <improvements> \
  --assignment <assignment_name>
```

## Best Practices

1. **Always Read First**: Review grading spreadsheet and previous assessments before starting
2. **Batch Processing**: Grade in small batches (3-5 students) for better progress tracking
3. **Verify Cloning**: Check that repositories clone successfully before grading
4. **Review Outliers**: Manually review very high (>90) or very low (<40) scores
5. **Document Changes**: Update this README when making significant skill modifications
6. **Test on Known Submissions**: Use student 38981 (excellent submission) and 38950 (average submission) for testing changes

## Contact and Support

For issues or questions about the orchestrator:
- Review skill-specific assess.py files in `.claude/skills/{skill-name}/`
- Check JSON output for detailed error messages
- Review individual skill logs for debugging

## Quick Reference Commands

```bash
# Grade single student
python ".claude/skills/tier2-orchestrator/orchestrate.py" "WorkSubmissions01/Participant_{ID}_assignsubmission_file/repo" {ID} "Assignment 1"

# Clone repository manually
python ".claude/skills/tier2-orchestrator/clone_repo.py" "WorkSubmissions01/Participant_{ID}_assignsubmission_file"

# Check assessment output
cat assessments_tier2_assignment1/tier2_assessment_{ID}.json

# View PDFs
start WorkSubmissions01/Participant_{ID}_assignsubmission_file/Detailed_Grade_Breakdown_{ID}.pdf
start WorkSubmissions01/Participant_{ID}_assignsubmission_file/Grade_Report_{ID}.pdf
```

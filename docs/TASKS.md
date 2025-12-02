# Project Tasks & Progress Tracker
## AutoGrade Report Generator

**Version:** 2.0 (Self-Assessment Based)
**Last Updated:** 2025-12-01

## Task Status Legend
- 🔴 Not Started
- 🟡 In Progress
- 🟢 Completed
- ⏸️ Blocked
- 🔵 In Review

## Progress Overview

| Phase | Progress | Status |
|-------|----------|--------|
| Planning & Documentation | 0% | 🔴 |
| Core Development (Parser, Extractors, Calculators, Router) | 0% | 🔴 |
| Skills Development (4 Claude Skills with Self-Assessment) | 0% | 🔴 |
| PDF Generation (with Grade Breakdown) | 0% | 🔴 |
| Testing & Validation | 0% | 🔴 |
| Documentation & Polish | 0% | 🔴 |

---

## Phase 1: Planning & Documentation

### 1.1 Project Setup
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P1.1.1 | Create project repository | P0 | 🔴 | Day 1 | Initialize with proper structure |
| P1.1.2 | Set up .gitignore | P0 | 🔴 | Day 1 | Include .env, __pycache__, logs/, *.pdf, *.csv |
| P1.1.3 | Create .env.example | P0 | 🔴 | Day 1 | CLAUDE_API_KEY, SCALE_COEFFICIENT_A/B, MIN/MAX_SELF_GRADE |
| P1.1.4 | Initialize requirements.txt | P0 | 🔴 | Day 1 | typer, anthropic, reportlab, pydantic, PyPDF2 |
| P1.1.5 | Create directory structure | P0 | 🔴 | Day 1 | src/, tests/, docs/, prompts/, data/ |

### 1.2 Documentation
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P1.2.1 | Complete PRD.md | P0 | 🔴 | Day 2 | All sections with self-assessment penalty |
| P1.2.2 | Complete CLAUDE.md | P0 | 🔴 | Day 2 | Development guidelines with penalty formula |
| P1.2.3 | Complete PLANNING.md | P0 | 🔴 | Day 2 | C4 diagrams, ADRs, data models |
| P1.2.4 | Complete TASKS.md | P0 | 🔴 | Day 2 | This file |
| P1.2.5 | Create config/formula_params.yaml | P1 | 🔴 | Day 2 | Penalty formula constants, tier thresholds |

---

## Phase 2: Core Development

### 2.1 Markdown Parser
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P2.1.1 | Create src/core/parser.py | P0 | 🔴 | Day 3 | MarkdownParser class |
| P2.1.2 | Implement extract_criteria_table() | P0 | 🔴 | Day 3 | Parse TRUE/FALSE table |
| P2.1.3 | Implement count_requirements_met() | P0 | 🔴 | Day 3 | Count TRUE (not FALSE!) |
| P2.1.4 | Implement extract_metadata() | P0 | 🔴 | Day 3 | Student name, ID, repo URL |
| P2.1.5 | Implement validate_structure() | P0 | 🔴 | Day 3 | Check for required sections |
| P2.1.6 | Add error handling for malformed files | P0 | 🔴 | Day 3 | Clear error messages |

### 2.2 Self-Grade Extractor (NEW)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P2.2.1 | Create src/core/self_grade_extractor.py | P0 | 🔴 | Day 4 | SelfGradeExtractor class |
| P2.2.2 | Implement extract_from_pdf() | P0 | 🔴 | Day 4 | Read PDF metadata for self-grade |
| P2.2.3 | Implement extract_from_csv() | P0 | 🔴 | Day 4 | Read student_id, self_grade columns |
| P2.2.4 | Implement validate_range() | P0 | 🔴 | Day 4 | Check 60 ≤ self_grade ≤ 100 |
| P2.2.5 | Add error handling for missing self-grade | P0 | 🔴 | Day 4 | Clear error with student ID |

### 2.3 Base Grade Calculator (NEW)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P2.3.1 | Create src/core/base_calculator.py | P0 | 🔴 | Day 5 | BaseCalculator class |
| P2.3.2 | Implement calculate_base() | P0 | 🔴 | Day 5 | (requirements_met / 22) × 100 |
| P2.3.3 | Implement validate_criteria_count() | P0 | 🔴 | Day 5 | Check 0 ≤ met ≤ 22 |
| P2.3.4 | Add comprehensive tests | P0 | 🔴 | Day 5 | Test 0, 11, 22 criteria met |

### 2.4 Penalty Calculator (NEW)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P2.4.1 | Create src/core/penalty_calculator.py | P0 | 🔴 | Day 6 | PenaltyCalculator class |
| P2.4.2 | Implement calculate_scale() | P0 | 🔴 | Day 6 | 0.086603 × e^(0.027465 × self_grade) |
| P2.4.3 | Implement apply_penalty() | P0 | 🔴 | Day 6 | Conditional logic (only if self > base) |
| P2.4.4 | Implement max(0, base - penalty) cap | P0 | 🔴 | Day 6 | Prevent negative grades |
| P2.4.5 | Add formula parameter configuration | P1 | 🔴 | Day 6 | Read coefficients from YAML |
| P2.4.6 | Test against known values | P0 | 🔴 | Day 6 | Verify examples from grading_formula_description.md |

### 2.5 Skill Router
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P2.5.1 | Create src/core/router.py | P0 | 🔴 | Day 7 | SkillRouter class |
| P2.5.2 | Implement determine_tier() | P0 | 🔴 | Day 7 | Map FINAL grade to tier name |
| P2.5.3 | Implement select_skill() | P0 | 🔴 | Day 7 | Instantiate appropriate skill |
| P2.5.4 | Load tier config from YAML | P1 | 🔴 | Day 7 | Dynamic tier thresholds |

---

## Phase 3: Skills Development

### 3.1 Base Skill Framework
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P3.1.1 | Create src/skills/base_skill.py | P0 | 🔴 | Day 8 | Abstract BaseSkill class |
| P3.1.2 | Define generate_feedback() interface | P0 | 🔴 | Day 8 | Args: final_grade, assessment_data (with self/base/penalty) |
| P3.1.3 | Implement _analyze_self_assessment() | P0 | 🔴 | Day 8 | Generate self-assessment accuracy feedback |
| P3.1.4 | Implement _load_emoji_pool() | P1 | 🔴 | Day 8 | Load from assets/emoji_mapping.json |
| P3.1.5 | Implement _insert_emojis() | P1 | 🔴 | Day 8 | Add emojis per density setting |

### 3.2 Skill 1: Excellence (90-100)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P3.2.1 | Create src/skills/skill_1_excellence.py | P0 | 🔴 | Day 8 | Inherit from BaseSkill |
| P3.2.2 | Design prompt template with self-assessment | P0 | 🔴 | Day 8 | Include self/base/penalty breakdown |
| P3.2.3 | Implement generate_feedback() | P0 | 🔴 | Day 8 | Call Claude API with full context |
| P3.2.4 | Set emoji_density="high" | P0 | 🔴 | Day 8 | 1 emoji per 20-30 words |
| P3.2.5 | Test with accurate self-assessment | P0 | 🔴 | Day 8 | Self=100, base=100 → praise accuracy |
| P3.2.6 | Test with humble self-assessment | P0 | 🔴 | Day 8 | Self=85, base=100 → praise humility |
| P3.2.7 | Document prompt in prompts/skills/ | P0 | 🔴 | Day 8 | Save prompt text + sample outputs |

### 3.3 Skill 2: Good (80-89)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P3.3.1 | Create src/skills/skill_2_good.py | P0 | 🔴 | Day 9 | Inherit from BaseSkill |
| P3.3.2 | Design prompt template with self-assessment | P0 | 🔴 | Day 9 | Balanced feedback + self-evaluation comment |
| P3.3.3 | Implement generate_feedback() | P0 | 🔴 | Day 9 | Call Claude API |
| P3.3.4 | Set emoji_density="moderate" | P0 | 🔴 | Day 9 | 1 emoji per 50-70 words |
| P3.3.5 | Test with slight overconfidence | P0 | 🔴 | Day 9 | Self=85, base=80 → small penalty mentioned |
| P3.3.6 | Document prompt in prompts/skills/ | P0 | 🔴 | Day 9 | Save prompt text + sample outputs |

### 3.4 Skill 3: Potential (55-79)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P3.4.1 | Create src/skills/skill_3_potential.py | P0 | 🔴 | Day 9 | Inherit from BaseSkill |
| P3.4.2 | Design prompt template with self-assessment | P0 | 🔴 | Day 9 | Motivational + realistic self-view |
| P3.4.3 | Implement generate_feedback() | P0 | 🔴 | Day 9 | Call Claude API |
| P3.4.4 | Set emoji_density="light" | P0 | 🔴 | Day 9 | 1 emoji per 100-120 words |
| P3.4.5 | Test with major overconfidence | P0 | 🔴 | Day 9 | Self=90, base=73 → large penalty, encourage honesty |
| P3.4.6 | Document prompt in prompts/skills/ | P0 | 🔴 | Day 9 | Save prompt text + sample outputs |

### 3.5 Skill 4: Below Expectations (<55)
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P3.5.1 | Create src/skills/skill_4_below.py | P0 | 🔴 | Day 9 | Inherit from BaseSkill |
| P3.5.2 | Design prompt template with self-assessment | P0 | 🔴 | Day 9 | Constructive + honest self-assessment importance |
| P3.5.3 | Implement generate_feedback() | P0 | 🔴 | Day 9 | Call Claude API |
| P3.5.4 | Set emoji_density="minimal" | P0 | 🔴 | Day 9 | 1-2 emojis total |
| P3.5.5 | Test with extreme overconfidence | P0 | 🔴 | Day 9 | Self=100, base=45 → penalty led to <55 |
| P3.5.6 | Document prompt in prompts/skills/ | P0 | 🔴 | Day 9 | Save prompt text + sample outputs |

---

## Phase 4: PDF Generation

### 4.1 PDF Formatter
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P4.1.1 | Create src/pdf/formatter.py | P0 | 🔴 | Day 10 | PDFFormatter class |
| P4.1.2 | Study student submission PDF format | P0 | 🔴 | Day 10 | Extract layout, fonts, spacing |
| P4.1.3 | Implement generate_pdf() | P0 | 🔴 | Day 10 | Use ReportLab |
| P4.1.4 | Add header section | P0 | 🔴 | Day 10 | Title, student info |
| P4.1.5 | Add grade breakdown section (NEW) | P0 | 🔴 | Day 10 | Self/Base/Penalty/Final display |
| P4.1.6 | Add performance tier display | P0 | 🔴 | Day 10 | Excellence/Good/Potential/Below |
| P4.1.7 | Add feedback section | P0 | 🔴 | Day 10 | Preserve emoji encoding |
| P4.1.8 | Add criteria summary table | P0 | 🔴 | Day 10 | Met vs. Missed |
| P4.1.9 | Test emoji rendering | P0 | 🔴 | Day 10 | Ensure UTF-8 support |
| P4.1.10 | Test grade breakdown formatting | P0 | 🔴 | Day 10 | Verify all 4 grades visible |

### 4.2 Template Matching
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P4.2.1 | Create src/pdf/template.py | P1 | 🔴 | Day 11 | Template configuration |
| P4.2.2 | Define font families | P1 | 🔴 | Day 11 | Match student PDF fonts |
| P4.2.3 | Define spacing/margins | P1 | 🔴 | Day 11 | Match student PDF layout |
| P4.2.4 | Create src/pdf/styles.py | P1 | 🔴 | Day 11 | ParagraphStyles for breakdown |

---

## Phase 5: CLI & Orchestration

### 5.1 CLI Interface
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P5.1.1 | Create cli.py | P0 | 🔴 | Day 11 | Main entry point with Typer |
| P5.1.2 | Implement generate-report command | P0 | 🔴 | Day 11 | Args: --input, --self-grade, --output |
| P5.1.3 | Implement batch-generate command | P0 | 🔴 | Day 11 | Args: --input-dir, --self-grades CSV, --output-dir |
| P5.1.4 | Implement verify-grade command | P1 | 🔴 | Day 11 | Args: --input, --self-grade (show calculation) |
| P5.1.5 | Implement validate-formula command (NEW) | P1 | 🔴 | Day 11 | Args: --self-grade, --requirements-met |
| P5.1.6 | Add --verbose flag | P1 | 🔴 | Day 11 | Detailed logging including penalty calculation |

### 5.2 Orchestration
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P5.2.1 | Create src/core/orchestrator.py | P0 | 🔴 | Day 12 | FeedbackOrchestrator class |
| P5.2.2 | Implement generate_report() pipeline | P0 | 🔴 | Day 12 | Parse → Extract self → Base → Penalty → Route → Generate → PDF |
| P5.2.3 | Implement batch_process() | P0 | 🔴 | Day 12 | Sequential processing with self-grades CSV |
| P5.2.4 | Add error handling | P0 | 🔴 | Day 12 | Continue on individual failures, log missing self-grades |
| P5.2.5 | Add progress tracking (tqdm) | P1 | 🔴 | Day 12 | Visual progress bar with self-grade status |

---

## Phase 6: Testing & Validation

### 6.1 Unit Tests
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P6.1.1 | Create tests/unit/test_parser.py | P0 | 🔴 | Day 12 | Test criteria extraction |
| P6.1.2 | Test parser with perfect score (22 TRUE) | P0 | 🔴 | Day 12 | Should parse correctly |
| P6.1.3 | Test parser with malformed table | P0 | 🔴 | Day 12 | Should raise ValueError |
| P6.1.4 | Create tests/unit/test_self_grade_extractor.py | P0 | 🔴 | Day 12 | Test extraction methods |
| P6.1.5 | Test extraction with valid range (60-100) | P0 | 🔴 | Day 12 | Should succeed |
| P6.1.6 | Test extraction with invalid range (<60, >100) | P0 | 🔴 | Day 12 | Should raise ValueError |
| P6.1.7 | Test extraction with missing self-grade | P0 | 🔴 | Day 12 | Should raise ValueError |
| P6.1.8 | Create tests/unit/test_base_calculator.py | P0 | 🔴 | Day 12 | Test base grade calculation |
| P6.1.9 | Test base calculator with 0, 11, 22 met | P0 | 🔴 | Day 12 | Verify 0%, 50%, 100% |
| P6.1.10 | Create tests/unit/test_penalty_calculator.py | P0 | 🔴 | Day 13 | Test penalty formula |
| P6.1.11 | Test penalty with accurate self-assessment | P0 | 🔴 | Day 13 | Self=100, base=100 → penalty=0 |
| P6.1.12 | Test penalty with humble self-assessment | P0 | 🔴 | Day 13 | Self=60, base=100 → penalty=0, final=100 |
| P6.1.13 | Test penalty with overconfidence | P0 | 🔴 | Day 13 | Self=100, base=81.8 → penalty≈24.6, final≈57.2 |
| P6.1.14 | Test penalty scale increases with claim | P0 | 🔴 | Day 13 | Scale(60) < Scale(100) |
| P6.1.15 | Create tests/unit/test_router.py | P0 | 🔴 | Day 13 | Test tier selection |
| P6.1.16 | Test router with each tier (final grade) | P0 | 🔴 | Day 13 | 95 → Skill1, 80 → Skill2, etc. |
| P6.1.17 | Create tests/unit/test_skills.py | P0 | 🔴 | Day 13 | Test each skill |
| P6.1.18 | Test self-assessment analysis in feedback | P0 | 🔴 | Day 13 | Verify mentions of accuracy/humility/overconfidence |
| P6.1.19 | Test emoji density | P1 | 🔴 | Day 13 | Verify count per tier |

### 6.2 Integration Tests
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P6.2.1 | Create tests/integration/test_end_to_end.py | P0 | 🔴 | Day 14 | Full pipeline test |
| P6.2.2 | Test with accurate self-assessment | P0 | 🔴 | Day 14 | Self=100, 22/22 → final=100 |
| P6.2.3 | Test with humble self-assessment | P0 | 🔴 | Day 14 | Self=85, 22/22 → final=100, praise humility |
| P6.2.4 | Test with slight overconfidence | P0 | 🔴 | Day 14 | Self=100, 21/22 → final≈89, small penalty |
| P6.2.5 | Test with major overconfidence | P0 | 🔴 | Day 14 | Self=100, 18/22 → final≈57, large penalty |
| P6.2.6 | Verify PDF output exists | P0 | 🔴 | Day 14 | Check file created |
| P6.2.7 | Verify PDF contains grade breakdown | P0 | 🔴 | Day 14 | Self, base, penalty, final visible |

### 6.3 Test Fixtures
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P6.3.1 | Create tests/fixtures/perfect_assessment.md | P0 | 🔴 | Day 12 | 22 TRUE, 0 FALSE |
| P6.3.2 | Create tests/fixtures/good_assessment.md | P0 | 🔴 | Day 12 | 18 TRUE, 4 FALSE |
| P6.3.3 | Create tests/fixtures/below_assessment.md | P0 | 🔴 | Day 12 | 10 TRUE, 12 FALSE |
| P6.3.4 | Create tests/fixtures/malformed_assessment.md | P0 | 🔴 | Day 12 | Missing table header |
| P6.3.5 | Create tests/fixtures/sample_self_grades.csv | P0 | 🔴 | Day 12 | student_id, self_grade columns |

### 6.4 Manual Validation
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P6.4.1 | Generate report for 63698 (perfect, self=100) | P0 | 🔴 | Day 15 | Accurate self-assessment scenario |
| P6.4.2 | Generate report for 63698 (perfect, self=85) | P0 | 🔴 | Day 15 | Humble self-assessment scenario |
| P6.4.3 | Generate report for 63685 (good, self=90) | P0 | 🔴 | Day 15 | Slight overconfidence scenario |
| P6.4.4 | Generate report for 63688 (poor, self=100) | P0 | 🔴 | Day 15 | Major overconfidence scenario |
| P6.4.5 | Verify PDF format matches template | P0 | 🔴 | Day 15 | Side-by-side comparison |
| P6.4.6 | Verify grade breakdown clarity | P0 | 🔴 | Day 15 | Can student understand penalty? |
| P6.4.7 | Verify self-assessment feedback present | P0 | 🔴 | Day 15 | All scenarios have commentary |
| P6.4.8 | Verify emoji usage | P0 | 🔴 | Day 15 | Count emojis per tier |
| P6.4.9 | Instructor review of sample reports | P0 | 🔴 | Day 15 | Get approval on all scenarios |

---

## Phase 7: Documentation & Polish

### 7.1 README
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P7.1.1 | Write installation instructions | P0 | 🔴 | Day 15 | Step-by-step for non-technical users |
| P7.1.2 | Write usage instructions | P0 | 🔴 | Day 15 | Examples for each command with self-grade |
| P7.1.3 | Explain self-assessment penalty formula | P0 | 🔴 | Day 15 | Non-technical explanation with examples |
| P7.1.4 | Add configuration guide | P0 | 🔴 | Day 15 | Explain .env variables, YAML config |
| P7.1.5 | Add troubleshooting section | P1 | 🔴 | Day 15 | Common errors (missing self-grade, etc.) |
| P7.1.6 | Add example outputs | P1 | 🔴 | Day 15 | Screenshots with grade breakdown |

### 7.2 Prompt Engineering Log
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P7.2.1 | Create prompts/README.md | P0 | 🔴 | Day 15 | Overview of prompt documentation |
| P7.2.2 | Document architecture prompts | P0 | 🔴 | Day 15 | Prompts used for system design |
| P7.2.3 | Create prompts/extraction/ directory | P0 | 🔴 | Day 15 | Self-grade extraction prompts |
| P7.2.4 | Document all 4 skill prompts | P0 | 🔴 | Day 15 | Exact prompts + self-assessment examples |
| P7.2.5 | Document PDF generation prompts | P1 | 🔴 | Day 15 | Layout/formatting with breakdown |
| P7.2.6 | Add lessons learned | P1 | 🔴 | Day 15 | What worked, self-assessment challenges |

### 7.3 Final Checks
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P7.3.1 | Verify all files < 150 lines | P0 | 🔴 | Day 16 | Refactor if needed (extractor, calculators separate) |
| P7.3.2 | Check test coverage ≥ 70% | P0 | 🔴 | Day 16 | Run coverage report |
| P7.3.3 | Verify penalty formula matches spec | P0 | 🔴 | Day 16 | Test against grading_formula_description.md examples |
| P7.3.4 | Verify no secrets in code | P0 | 🔴 | Day 16 | Search for hardcoded keys |
| P7.3.5 | Clean Git history | P1 | 🔴 | Day 16 | Meaningful commits (extractor → base → penalty → skills) |
| P7.3.6 | Add LICENSE file | P1 | 🔴 | Day 16 | MIT recommended |
| P7.3.7 | Update pyproject.toml metadata | P1 | 🔴 | Day 16 | Version 2.0, self-assessment based |

---

## Phase 8: Pilot Run

### 8.1 Production Testing
| ID | Task | Priority | Status | Due Date | Notes |
|----|------|----------|--------|----------|-------|
| P8.1.1 | Create sample self_grades.csv | P0 | 🔴 | Day 16 | 5 students with diverse self-grades |
| P8.1.2 | Process 5 real student assessments | P0 | 🔴 | Day 16 | Include accurate, humble, overconfident |
| P8.1.3 | Review generated PDFs | P0 | 🔴 | Day 16 | Verify quality, format, tone, grade breakdown |
| P8.1.4 | Time the processing | P0 | 🔴 | Day 16 | Should be < 3 min per report |
| P8.1.5 | Verify penalty calculations manually | P0 | 🔴 | Day 16 | Use calculator to confirm |
| P8.1.6 | Fix any issues found | P0 | 🔴 | Day 16 | Bug fixes |
| P8.1.7 | Get instructor final approval | P0 | 🔴 | Day 16 | Sign-off for production use |

---

## Blockers & Issues

| ID | Issue | Blocking Tasks | Status | Resolution |
|----|-------|----------------|--------|------------|
| B001 | Claude API rate limits unknown | P5.2.3 (batch processing) | 🔴 Open | Test with batch of 5, measure latency |
| B002 | Student submission PDF format not yet analyzed | P4.1.2, P4.2.* | 🔴 Open | Obtain sample PDF from instructor |
| B003 | Self-grade data source unclear | P2.2.2, P2.2.3 | 🔴 Open | Confirm with instructor: PDF metadata or CSV? |

---

## Daily Progress Log

### Day 1 (Target: Project Setup)
**Planned**:
- P1.1.1 through P1.1.5 (Project setup)

**Completed**:
- [ ] TBD

**Blockers**:
- [ ] TBD

**Notes**:
- [ ] TBD

---

### Day 2 (Target: Documentation)
**Planned**:
- P1.2.1 through P1.2.5 (Documentation)

**Completed**:
- [ ] TBD

**Blockers**:
- [ ] TBD

**Notes**:
- [ ] TBD

---

### Day 3-7 (Target: Core Development)
**Planned**:
- P2.1.* (Parser)
- P2.2.* (Self-Grade Extractor)
- P2.3.* (Base Calculator)
- P2.4.* (Penalty Calculator)
- P2.5.* (Router)

**Completed**:
- [ ] TBD

**Blockers**:
- [ ] B003 (Self-grade data source)

**Notes**:
- [ ] Critical path: extractor → base calc → penalty calc → router

---

## Submission Checklist

### Functional Requirements
- [ ] Parses markdown criteria tables correctly
- [ ] Extracts self-grades from PDF metadata or CSV
- [ ] Calculates base grade from requirements met
- [ ] Applies penalty formula correctly (with conditional logic)
- [ ] Routes to correct skill based on FINAL grade tier
- [ ] All 4 skills generate appropriate feedback
- [ ] All skills include self-assessment accuracy commentary
- [ ] Emoji usage matches tier specifications
- [ ] PDFs match student submission format
- [ ] PDFs display grade breakdown (self/base/penalty/final)
- [ ] Batch processing works with self-grades CSV
- [ ] Error handling is comprehensive (missing self-grades, invalid ranges)

### Formula Verification
- [ ] Penalty formula matches grading_formula_description.md
- [ ] Test case: Self=100, met=22 → final=100 ✓
- [ ] Test case: Self=100, met=21 → final≈89 ✓
- [ ] Test case: Self=100, met=18 → final≈57 ✓
- [ ] Test case: Self=60, met=22 → final=100 ✓
- [ ] Test case: Self=80, met=18 → final≈82 ✓
- [ ] Test case: Self=90, met=18 → final≈73 ✓

### Code Quality
- [ ] All files under 150 lines
- [ ] Comprehensive docstrings (especially penalty calculator)
- [ ] No hardcoded secrets
- [ ] 70%+ test coverage
- [ ] Type hints throughout
- [ ] Separate files: parser, extractor, base_calc, penalty_calc

### Documentation
- [ ] README is complete user manual
- [ ] PRD, CLAUDE, PLANNING, TASKS docs exist (v2.0)
- [ ] prompts/ directory fully populated (including extraction/)
- [ ] Formula explanation clear for non-technical users
- [ ] Troubleshooting guide includes self-grade issues

### Git & Version Control
- [ ] 15-20+ commits showing progression
- [ ] Meaningful commit messages (feat(extractor), feat(penalty), etc.)
- [ ] No WIP or temporary commits
- [ ] Commits show logical sequence (extractor → base → penalty → skills)

### Testing
- [ ] Unit tests pass (parser, extractor, base_calc, penalty_calc, router, skills)
- [ ] Integration tests pass (accurate, humble, overconfident scenarios)
- [ ] Edge case tests pass (range validation, missing self-grade, penalty=0, penalty>base)
- [ ] Manual validation with real data (all scenarios)
- [ ] Instructor approval on sample outputs (all self-assessment types)

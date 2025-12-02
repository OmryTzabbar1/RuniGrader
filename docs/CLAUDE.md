# CLAUDE.md - AutoGrade Report Generator Development Guidelines

**Version:** 2.0 (Self-Assessment Based)
**Last Updated:** 2025-12-01

## Project Overview

AutoGrade Report Generator is a Claude CLI agent that transforms markdown assessment files into professional, graded PDF reports with self-assessment penalty calculation and tier-appropriate feedback based on student performance (90-100%, 80-89%, 55-79%, <55%).

**Key Innovation**: This system implements a **self-grading penalty formula** that rewards accurate self-assessment and penalizes overconfidence. Students claim a grade (60-100), and the system compares their claim to actual performance, applying exponential penalties for overestimation.

---

## CRITICAL REQUIREMENTS - Read This First

### Git Workflow (MANDATORY)
- **NEVER make just one commit** - Multiple commits throughout development are REQUIRED
- Commit after each logical unit of work (parser done, self-grade extractor, penalty calculator, skill implemented, PDF formatter complete, etc.)
- Minimum 15-20 commits showing clear progression
- Each commit message must follow: `<type>(<scope>): <description>`
  - Examples:
    - `feat(parser): Add markdown criteria table parser`
    - `feat(extractor): Add self-grade extraction from PDF metadata`
    - `feat(calculator): Implement base grade calculator`
    - `feat(calculator): Implement exponential penalty formula`
    - `feat(skills): Add self-assessment analysis to Skill 1`
    - `test(calculator): Add penalty calculation edge case tests`
- Reference task IDs: e.g., "feat(router): Add tier-based skill routing [P2.2.3]"

### Prompt Documentation (MANDATORY)
- **SAVE EVERY SIGNIFICANT PROMPT** to prompts/ directory as you develop
- Document in real-time, not retroactively
- Organize by category:
  - `prompts/architecture/` - System design prompts
  - `prompts/extraction/` - Self-grade extraction prompts
  - `prompts/skills/` - Prompts for each of the 4 feedback skills (include self-assessment analysis)
  - `prompts/pdf-generation/` - PDF formatting prompts
  - `prompts/testing/` - Test generation prompts
- Update `prompts/README.md` with lessons learned
- This is NOT optional - required for academic excellence evaluation

---

## Grading Formula Deep Dive

### The Self-Assessment Penalty System

This is the **core innovation** of the project. Understanding it is CRITICAL.

**Three-Step Process:**

#### Step 1: Calculate Scale Multiplier
```python
scale = 0.086603 * math.exp(0.027465 * self_grade)
```

The scale increases exponentially with claimed grade:
- Claiming 60 → scale = 0.45 (low risk)
- Claiming 80 → scale = 0.78 (moderate risk)
- Claiming 100 → scale = 1.35 (high risk)

**Why?** Higher claims carry more penalty when wrong.

#### Step 2: Calculate Base Grade
```python
base_grade = (requirements_met / 22) * 100
```

This is what the student **actually earned** based on criteria met.

#### Step 3: Apply Penalty (Conditional)
```python
if self_grade > base_grade:  # Overestimated
    difference = self_grade - base_grade
    penalty = difference * scale
    final_grade = max(0, base_grade - penalty)
else:  # Underestimated or accurate
    final_grade = base_grade  # No penalty - reward humility
```

### Example Scenarios

| Self | Met | Base | Scale | Difference | Penalty | Final | Explanation |
|------|-----|------|-------|------------|---------|-------|-------------|
| 100 | 22/22 | 100.0 | 1.35 | 0 | 0 | 100.0 | Perfect accuracy ✓ |
| 100 | 21/22 | 95.5 | 1.35 | 4.5 | -6.1 | 89.4 | Slight overconfidence |
| 100 | 18/22 | 81.8 | 1.35 | 18.2 | -24.6 | 57.2 | Major overconfidence penalty |
| 60 | 22/22 | 100.0 | 0.45 | -40 | 0 | 100.0 | Humble - gets what earned ✓ |
| 80 | 18/22 | 81.8 | 0.78 | -1.8 | 0 | 81.8 | Slightly underestimated ✓ |
| 90 | 18/22 | 81.8 | 1.03 | 8.2 | -8.4 | 73.4 | Overconfident - penalized |

### Constants (NEVER CHANGE)
```python
SCALE_COEFFICIENT_A = 0.086603
SCALE_EXPONENT_B = 0.027465
TOTAL_REQUIREMENTS = 22
MIN_SELF_GRADE = 60
MAX_SELF_GRADE = 100
```

---

## Code Quality Standards

### File Size Limits
- **Maximum file length**: 150 lines of code (STRICTLY ENFORCED)
- When a file exceeds 150 lines, refactor into smaller modules
- Each file should have single responsibility:
  - `parser.py` - Parse markdown only
  - `self_grade_extractor.py` - Extract self-grade from PDF/CSV
  - `base_calculator.py` - Calculate base grade from criteria
  - `penalty_calculator.py` - Apply self-assessment penalty
  - `router.py` - Skill routing only
  - `skill_1_excellence.py` through `skill_4_below.py` - Individual skills

### Code Organization

```
autograde-report-generator/
├── src/
│   ├── core/
│   │   ├── parser.py                   # Markdown → criteria extraction
│   │   ├── self_grade_extractor.py     # Extract self-grade from PDF/CSV
│   │   ├── base_calculator.py          # Base grade = (met/22) * 100
│   │   ├── penalty_calculator.py       # Penalty formula (scale, difference)
│   │   └── router.py                   # Tier determination & skill selection
│   ├── skills/
│   │   ├── base_skill.py               # Abstract base class for skills
│   │   ├── skill_1_excellence.py       # 90-100% feedback (includes self-assessment)
│   │   ├── skill_2_good.py             # 80-89% feedback
│   │   ├── skill_3_potential.py        # 55-79% feedback
│   │   └── skill_4_below.py            # <55% feedback
│   ├── pdf/
│   │   ├── formatter.py                # PDF layout & structure
│   │   ├── template.py                 # Template matching student submissions
│   │   └── styles.py                   # Fonts, colors, spacing
│   ├── utils/
│   │   ├── file_io.py                  # File reading/writing helpers
│   │   ├── logger.py                   # Logging configuration
│   │   └── validator.py                # Input validation (self-grade range, etc.)
│   └── config/
│       └── settings.py                 # Configuration constants
├── tests/
│   ├── unit/
│   │   ├── test_parser.py
│   │   ├── test_self_grade_extractor.py
│   │   ├── test_base_calculator.py
│   │   ├── test_penalty_calculator.py
│   │   ├── test_router.py
│   │   └── test_skills.py
│   ├── integration/
│   │   └── test_end_to_end.py
│   └── fixtures/
│       ├── sample_assessment.md
│       ├── sample_submission.pdf        # With self-grade metadata
│       └── expected_report.pdf
├── data/
│   └── sample_inputs/                  # Example assessment files
├── results/
│   └── generated_reports/              # Output PDFs
├── docs/
│   ├── PRD.md
│   ├── CLAUDE.md                       # This file
│   ├── PLANNING.md
│   └── TASKS.md
├── prompts/
│   ├── README.md                       # Lessons learned
│   ├── architecture/
│   ├── extraction/                     # Self-grade extraction prompts
│   ├── skills/
│   ├── pdf-generation/
│   └── testing/
├── config/
│   └── formula_params.yaml             # Penalty formula coefficients
├── assets/
│   ├── sample_student_pdf.pdf          # Reference formatting
│   └── emoji_mapping.json              # Emoji usage rules per tier
├── cli.py                              # Main CLI entry point
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── pyproject.toml
```

### Naming Conventions
- **Files**: `snake_case.py`
- **Classes**: `PascalCase` (e.g., `SelfGradeExtractor`, `PenaltyCalculator`, `BaseCalculator`)
- **Functions/Methods**: `snake_case` (e.g., `extract_self_grade`, `calculate_penalty`, `calculate_base_grade`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `SCALE_COEFFICIENT_A`, `TOTAL_REQUIREMENTS`)
- **Variables**: `snake_case`

### Documentation Requirements

#### Every Function Must Have:
```python
def calculate_penalty(self_grade: int, base_grade: float) -> float:
    """
    Calculate penalty for self-grade overestimation using exponential scale.

    Applies the three-step penalty formula:
    1. scale = 0.086603 × e^(0.027465 × self_grade)
    2. difference = self_grade - base_grade
    3. penalty = difference × scale (if positive, else 0)

    Args:
        self_grade: Student's claimed grade (60-100)
        base_grade: Actual grade from criteria met (0-100)

    Returns:
        Penalty amount to subtract from base_grade (0 if underestimated)

    Raises:
        ValueError: If self_grade not in range [60, 100]

    Example:
        >>> calculate_penalty(self_grade=100, base_grade=81.8)
        24.57  # High penalty for claiming 100 when earned 81.8
        >>> calculate_penalty(self_grade=80, base_grade=90.0)
        0.0  # No penalty - underestimated (humble)
    """
```

#### Every Class Must Have:
```python
class PenaltyCalculator:
    """
    Calculates self-assessment penalties for overconfident grade claims.

    Implements exponential penalty system where penalty increases with:
    1. Size of overestimation (claimed - earned)
    2. Height of claim (higher claims = higher scale multiplier)

    The system rewards humility: no penalty when student underestimates.

    Attributes:
        scale_coeff_a: Scale formula coefficient (0.086603)
        scale_exp_b: Scale formula exponent (0.027465)
        min_self_grade: Minimum allowed self-grade (60)
        max_self_grade: Maximum allowed self-grade (100)

    Example:
        >>> calc = PenaltyCalculator()
        >>> final = calc.apply_penalty(self_grade=100, base_grade=81.8)
        >>> final
        57.23  # Severe penalty for major overconfidence
    """
```

---

## Configuration Management

### Environment Variables
Create `.env.example`:
```bash
# Claude API Configuration
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Penalty Formula Parameters (RARELY CHANGED - verify before modifying)
SCALE_COEFFICIENT_A=0.086603
SCALE_EXPONENT_B=0.027465
TOTAL_REQUIREMENTS=22
MIN_SELF_GRADE=60
MAX_SELF_GRADE=100

# PDF Generation
PDF_TEMPLATE_PATH=assets/student_template.pdf
OUTPUT_DIR=results/generated_reports/

# Processing Options
BATCH_PROCESSING_ENABLED=true
PARALLEL_WORKERS=1  # Sequential for now

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autograde.log
```

### Configuration Files

`config/formula_params.yaml`:
```yaml
penalty_formula:
  scale_coefficient_a: 0.086603
  scale_exponent_b: 0.027465
  total_requirements: 22
  self_grade_range:
    min: 60
    max: 100

performance_tiers:
  excellence:
    min_grade: 90
    max_grade: 100
    skill: "Skill1Excellence"
    emoji_density: high  # 1 emoji per 20-30 words
    self_assessment_feedback: true  # Include accuracy analysis
  good:
    min_grade: 80
    max_grade: 89
    skill: "Skill2Good"
    emoji_density: moderate  # 1 emoji per 50-70 words
    self_assessment_feedback: true
  potential:
    min_grade: 55
    max_grade: 79
    skill: "Skill3Potential"
    emoji_density: light  # 1 emoji per 100-120 words
    self_assessment_feedback: true
  below:
    min_grade: 0
    max_grade: 54
    skill: "Skill4Below"
    emoji_density: minimal  # 1-2 emojis total
    self_assessment_feedback: true  # Encourage realistic self-view
```

---

## Testing Requirements

### Coverage Targets
- **Minimum**: 70% overall code coverage
- **Critical paths** (parser, extractors, calculators, router): 90%+
- **Skills** (feedback generators): 80%+
- **PDF generation**: 60%+ (harder to test, focus on structure)

### Test Types Required

1. **Unit Tests for Penalty Formula**:
   ```python
   def test_penalty_perfect_accuracy():
       """Test no penalty when self-grade matches base."""
       calc = PenaltyCalculator()
       final = calc.apply_penalty(self_grade=100, base_grade=100.0)
       assert final == 100.0

   def test_penalty_major_overconfidence():
       """Test severe penalty for claiming 100 with 18/22 met."""
       calc = PenaltyCalculator()
       base = (18 / 22) * 100  # 81.82
       final = calc.apply_penalty(self_grade=100, base_grade=base)
       assert 56 < final < 58  # Should be ~57.2

   def test_penalty_humility_rewarded():
       """Test no penalty when student underestimates."""
       calc = PenaltyCalculator()
       final = calc.apply_penalty(self_grade=60, base_grade=100.0)
       assert final == 100.0  # Gets what they earned

   def test_penalty_scale_increases_with_claim():
       """Test that higher claims have higher scale multipliers."""
       calc = PenaltyCalculator()
       scale_60 = calc._calculate_scale(60)
       scale_100 = calc._calculate_scale(100)
       assert scale_100 > scale_60 * 2  # ~1.35 vs ~0.45
   ```

2. **Edge Case Tests**:
   ```python
   def test_self_grade_below_minimum():
       """Test rejection of self-grade < 60."""
       extractor = SelfGradeExtractor()
       with pytest.raises(ValueError, match="Self-grade must be"):
           extractor.validate_self_grade(55)

   def test_self_grade_above_maximum():
       """Test rejection of self-grade > 100."""
       extractor = SelfGradeExtractor()
       with pytest.raises(ValueError, match="Self-grade must be"):
           extractor.validate_self_grade(105)

   def test_parser_missing_self_grade():
       """Test handling when student didn't submit self-grade."""
       with pytest.raises(ValueError, match="No self-grade found"):
           extract_self_grade("no_self_grade.pdf")

   def test_base_calculator_all_criteria_met():
       """Test base grade calculation with perfect score."""
       calc = BaseCalculator()
       base = calc.calculate(requirements_met=22)
       assert base == 100.0

   def test_base_calculator_zero_criteria_met():
       """Test base grade calculation with complete failure."""
       calc = BaseCalculator()
       base = calc.calculate(requirements_met=0)
       assert base == 0.0
   ```

3. **Integration Tests**:
   ```python
   def test_end_to_end_accurate_self_assessment():
       """Test complete pipeline with accurate self-grading."""
       output = generate_report(
           assessment_file="fixtures/assessment_18_of_22.md",
           self_grade=80,  # Accurate for 18/22 (~82)
           output_file="temp_output.pdf"
       )
       assert 81 < output.final_grade < 83  # Gets base grade
       assert output.tier == "Good"
       assert "accurate self-assessment" in output.feedback.lower()

   def test_end_to_end_overconfident():
       """Test pipeline with severe overconfidence."""
       output = generate_report(
           assessment_file="fixtures/assessment_18_of_22.md",
           self_grade=100,  # Overconfident (earned ~82)
           output_file="temp_output.pdf"
       )
       assert 56 < output.final_grade < 58  # Heavy penalty
       assert output.tier == "Potential"
       assert "overestimated" in output.feedback.lower()

   def test_end_to_end_humble():
       """Test pipeline with humble self-assessment."""
       output = generate_report(
           assessment_file="fixtures/assessment_22_of_22.md",
           self_grade=85,  # Humble (earned 100)
           output_file="temp_output.pdf"
       )
       assert output.final_grade == 100.0  # Gets what earned
       assert output.tier == "Excellence"
       assert "humble" in output.feedback.lower() or "underestimated" in output.feedback.lower()
   ```

### Edge Cases to Document

| Edge Case | Expected Behavior |
|-----------|-------------------|
| Self-grade = 60 (minimum) | Calculate normally with scale = 0.45 |
| Self-grade = 100 (maximum) | Calculate normally with scale = 1.35 |
| Self-grade < 60 | Raise `ValueError` with clear message |
| Self-grade > 100 | Raise `ValueError` with clear message |
| Self-grade missing from PDF | Raise `ValueError`, ask user to provide |
| Self-grade = base exactly | No penalty, final = base |
| Penalty would make final < 0 | Cap at 0 using `max(0, base - penalty)` |
| All criteria TRUE (22/22) | Base = 100, penalty only if claimed > 100 (impossible) |
| All criteria FALSE (0/22) | Base = 0, penalty irrelevant (already 0) |
| Self-grade as float (e.g., 85.5) | Round or reject - enforce integer |

---

## Error Handling

### Required Practices

```python
def extract_self_grade(pdf_path: str) -> int:
    """
    Extract self-grade from student PDF metadata or embedded text.

    Self-grade must be in range [60, 100] per assignment requirements.

    Args:
        pdf_path: Path to student submission PDF

    Returns:
        Self-grade as integer (60-100)

    Raises:
        FileNotFoundError: If PDF doesn't exist
        ValueError: If self-grade not found or out of range
        PDFReadError: If PDF is corrupted or unreadable
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"Student submission PDF not found: {pdf_path}\n"
            f"Ensure the file exists and path is correct."
        )

    try:
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            # Extract self-grade from metadata or text
            self_grade_text = extract_metadata_field(pdf, "self_grade")
    except Exception as e:
        raise PDFReadError(f"Cannot read PDF {pdf_path}: {e}")

    if not self_grade_text:
        raise ValueError(
            f"No self-grade found in {pdf_path}. "
            f"Students must include self-grade in PDF metadata or "
            f"prominently displayed text (e.g., 'Self-Grade: 85')."
        )

    try:
        self_grade = int(self_grade_text)
    except ValueError:
        raise ValueError(
            f"Invalid self-grade format: '{self_grade_text}'. "
            f"Expected integer between 60-100."
        )

    if not (60 <= self_grade <= 100):
        raise ValueError(
            f"Self-grade {self_grade} out of range. "
            f"Valid range is 60-100 per assignment guidelines."
        )

    return self_grade
```

### Error Messages

- **User-friendly**: "Could not find self-grade in student PDF. Please ensure the submission includes 'Self-Grade: XX' (60-100)."
- **Actionable**: "Penalty calculation failed because self-grade=105 exceeds maximum of 100. Check student submission for errors."
- **Detailed logging**: `logger.error(f"Self-grade extraction failed for {pdf_path}: {error_detail}")`

---

## Git Practices

### IMPORTANT: Frequent Commits Required

Build up commit history showing development progression:

```
1. docs: Add PRD, CLAUDE.md, PLANNING.md, TASKS.md with self-assessment system
2. feat(core): Initialize project structure with src/, tests/, docs/
3. feat(parser): Add markdown criteria table parser
4. test(parser): Add unit tests for parser edge cases
5. feat(extractor): Add self-grade extraction from PDF metadata
6. test(extractor): Add validation tests for self-grade range [60-100]
7. feat(calculator): Implement base grade calculator (met/22 * 100)
8. test(calculator): Verify base calculation with 0, 11, 22 criteria met
9. feat(calculator): Implement exponential scale formula (0.086603 × e^(0.027465x))
10. feat(calculator): Implement penalty calculator with conditional logic
11. test(calculator): Add penalty tests for accuracy, overconfidence, humility
12. feat(router): Add tier-based skill routing logic
13. test(router): Verify correct skill selection for each tier
14. feat(skills): Add Skill 1 Excellence with self-assessment feedback
15. feat(skills): Add Skill 2 Good with self-assessment feedback
16. feat(skills): Add Skill 3 Potential with self-assessment feedback
17. feat(skills): Add Skill 4 Below with self-assessment feedback
18. test(skills): Add tests for emoji density and self-assessment mentions
19. feat(pdf): Add PDF formatter with self-assessment details
20. test(integration): Add end-to-end test with accurate self-assessment
21. test(integration): Add end-to-end test with overconfident student
22. test(integration): Add end-to-end test with humble student
23. docs: Update README with self-grading formula explanation
24. docs(prompts): Document all prompts used for skill generation
25. fix(calculator): Handle edge case where penalty exceeds base (cap at 0)
26. refactor: Split calculator into base_calculator.py and penalty_calculator.py
27. docs: Add troubleshooting guide for self-grade extraction errors
```

### Commit Messages
```
<type>(<scope>): <short description>

<longer description if needed>

Refs: [TASK_ID]
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

---

## Skill Development Guidelines

### Skill Implementation Template

Each skill must inherit from `BaseSkill` and implement `generate_feedback()`:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSkill(ABC):
    """Abstract base class for feedback generation skills."""

    def __init__(self, emoji_density: str = "moderate"):
        self.emoji_density = emoji_density
        self.emoji_pool = self._load_emoji_pool()

    @abstractmethod
    def generate_feedback(
        self,
        final_grade: float,
        assessment_data: Dict[str, Any]
    ) -> str:
        """
        Generate tier-appropriate feedback for student report.

        Args:
            final_grade: Calculated final grade after penalty (0-100)
            assessment_data: Dict with:
                - 'self_grade': Student's claimed grade (60-100)
                - 'base_grade': Earned grade from criteria (0-100)
                - 'penalty': Penalty applied (0 or positive)
                - 'requirements_met': Number of TRUE criteria (0-22)
                - 'criteria': List of criteria dicts
                - 'metadata': Student info (name, repo, etc.)
                - 'key_findings': Extracted from assessment markdown

        Returns:
            Formatted feedback text (250-450 words) with self-assessment analysis
        """
        pass

    def _load_emoji_pool(self) -> Dict[str, List[str]]:
        """Load emoji mappings from assets/emoji_mapping.json."""
        # Implementation...

    def _insert_emojis(self, text: str) -> str:
        """Insert emojis based on density setting."""
        # Implementation...

    def _analyze_self_assessment(
        self,
        self_grade: int,
        base_grade: float,
        penalty: float
    ) -> str:
        """
        Generate self-assessment accuracy feedback.

        Returns text commenting on student's metacognitive accuracy.
        """
        difference = self_grade - base_grade

        if abs(difference) < 3:
            return "Your self-assessment was remarkably accurate! This demonstrates strong metacognitive awareness."
        elif difference < 0:
            return "You were humble in your self-assessment - you actually performed better than you estimated!"
        elif difference < 10:
            return "Your self-assessment was slightly optimistic. Developing accurate self-evaluation is an important skill."
        else:
            return (
                f"Your self-assessment significantly overestimated your performance "
                f"(claimed {self_grade}, earned {base_grade:.1f}), resulting in a "
                f"{penalty:.1f}-point penalty. Strive for more realistic self-evaluation."
            )
```

### Skill 1: Excellence (90-100)

```python
class Skill1Excellence(BaseSkill):
    """Generate encouraging feedback for top performers."""

    def __init__(self):
        super().__init__(emoji_density="high")

    def generate_feedback(self, final_grade: float, assessment_data: Dict) -> str:
        # Use Claude API with prompt:
        prompt = f"""
You are generating feedback for a student who achieved a FINAL GRADE of {final_grade:.1f}/100
(Excellence tier) after self-assessment penalty calculation.

PERFORMANCE DETAILS:
- Self-Grade (claimed): {assessment_data['self_grade']}
- Base Grade (earned from criteria): {assessment_data['base_grade']:.1f}
- Requirements Met: {assessment_data['requirements_met']}/22
- Penalty Applied: {assessment_data['penalty']:.1f} points
- Final Grade: {final_grade:.1f}

Self-Assessment Accuracy:
{self._analyze_self_assessment(
    assessment_data['self_grade'],
    assessment_data['base_grade'],
    assessment_data['penalty']
)}

Missed Criteria: {[c['name'] for c in assessment_data['criteria'] if not c['met']]}

Key Findings from Assessment:
{assessment_data['key_findings']}

Generate 300-400 word feedback with:
1. Enthusiastic opening celebrating their excellence (use emojis like 🎉 ✨ 🌟)
2. Comment on their self-assessment accuracy (accurate? humble? overconfident?)
3. 2-3 specific strengths from their work
4. 1-2 areas for improvement (even top scores get growth feedback)
5. Encourage continued development of metacognitive skills (accurate self-evaluation)
6. Closing that maintains excellence

Use frequent emojis (every 20-30 words) but tastefully. Maintain professional academic tone.
"""
        # Call Claude API, get response, post-process
        return self._insert_emojis(response)
```

---

## PDF Generation Guidelines

### Template Matching

PDF must visually match student submission format AND include self-assessment details:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf(report_data: Dict, output_path: str):
    """
    Generate PDF matching student submission template with self-assessment breakdown.

    Structure:
    - Header: Assignment title, student info
    - Grade Breakdown: Self-grade, base grade, penalty, final grade
    - Feedback section: Tier-appropriate text with self-assessment analysis
    - Criteria summary: Table of met/missed criteria
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    grade_style = ParagraphStyle(
        'GradeStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a73e8'),
        alignment=1  # Center
    )

    breakdown_style = ParagraphStyle(
        'BreakdownStyle',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20
    )

    # Header
    story.append(Paragraph("Assignment 3 Grading Report", styles['Title']))
    story.append(Spacer(1, 12))

    # Student info
    student_info = [
        ["Student:", report_data['student_name']],
        ["ID:", report_data['student_id']],
        ["Repository:", report_data['repo_url']]
    ]
    story.append(Table(student_info, colWidths=[80, 400]))
    story.append(Spacer(1, 20))

    # Grade Breakdown (KEY ADDITION)
    story.append(Paragraph("GRADE BREAKDOWN:", styles['Heading2']))

    breakdown_data = [
        ["Self-Grade (Claimed):", f"{report_data['self_grade']}/100"],
        ["Base Grade (Earned):", f"{report_data['base_grade']:.1f}/100"],
        ["Requirements Met:", f"{report_data['requirements_met']}/22"],
        ["Penalty Applied:", f"-{report_data['penalty']:.1f} points"],
        ["", ""],
        ["FINAL GRADE:", f"{report_data['final_grade']:.0f}/100"]
    ]

    breakdown_table = Table(breakdown_data, colWidths=[180, 120])
    breakdown_table.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 5), (-1, 5), 14),
        ('TEXTCOLOR', (0, 5), (-1, 5), colors.HexColor('#1a73e8')),
        ('LINEABOVE', (0, 5), (-1, 5), 2, colors.black)
    ])

    story.append(breakdown_table)
    story.append(Spacer(1, 20))

    # Performance tier
    story.append(Paragraph(f"Performance Tier: {report_data['tier']}", styles['Heading2']))
    story.append(Spacer(1, 15))

    # Feedback (includes self-assessment analysis)
    story.append(Paragraph("FEEDBACK:", styles['Heading2']))
    story.append(Paragraph(report_data['feedback'], styles['BodyText']))
    story.append(Spacer(1, 20))

    # Criteria summary
    story.append(Paragraph("CRITERIA SUMMARY:", styles['Heading2']))
    criteria_data = [
        ["✓ Met:", f"{report_data['requirements_met']}/22"],
        ["✗ Missing:", f"{22 - report_data['requirements_met']}/22"]
    ]
    if report_data['requirements_met'] < 22:
        for criterion in report_data['missed_criteria']:
            criteria_data.append(["  -", criterion])

    story.append(Table(criteria_data, colWidths=[80, 400]))

    # Build PDF
    doc.build(story)
```

---

## Task Tracking & Progress Updates

### Automatic TASKS.md Updates
- **Update TASKS.md after completing each task**:
  - Change status from 🔴 to 🟡 when starting
  - Change to 🟢 when complete, add timestamp
  - Update phase progress percentages
- Add entries to Daily Progress Log
- Reference task IDs in commit messages

### CRITICAL: Document Prompts

Save ALL significant prompts:
```
prompts/
├── README.md                               # Lessons learned summary
├── architecture/
│   └── system-design-prompt.md             # Initial architecture planning
├── extraction/
│   └── self-grade-extraction-prompt.md     # Prompt for extracting self-grade
├── skills/
│   ├── skill-1-excellence-prompt.md        # Includes self-assessment analysis
│   ├── skill-2-good-prompt.md
│   ├── skill-3-potential-prompt.md
│   └── skill-4-below-prompt.md
├── pdf-generation/
│   └── template-matching-prompt.md         # Prompt for PDF formatting
└── testing/
    └── test-generation-prompt.md           # Prompts for creating test cases
```

Each prompt file format:
```markdown
# Prompt: [Purpose]

## Context
[What problem this solves, when it was used]

## Prompt Text
```
[Exact prompt sent to Claude]
```

## Output Received
[Summary or excerpt of Claude's response]

## Lessons Learned
[What worked well, what to adjust for next time]
```

---

## Quality Checklist Before Completion

### Code Quality
- [ ] All files under 150 lines (refactor if needed)
- [ ] Docstrings on all functions/classes/modules
- [ ] No hardcoded API keys (use .env)
- [ ] 70%+ test coverage
- [ ] All edge cases have tests (especially self-grade validation)
- [ ] Error messages are user-friendly
- [ ] Self-grade extraction works for PDF and CSV formats

### Formula Verification
- [ ] Penalty formula matches specification exactly
- [ ] Scale calculation verified: 0.086603 × e^(0.027465 × self_grade)
- [ ] Base calculation verified: (met / 22) × 100
- [ ] Conditional penalty application correct (only if self > base)
- [ ] Manual test cases match expected values from grading_formula_description.md

### Git & Version Control
- [ ] 15-20+ commits showing progression
- [ ] Each commit represents logical unit
- [ ] Commit messages follow convention
- [ ] No "WIP" or "temp" commits in final history
- [ ] Commits show self-grade extractor → base calculator → penalty calculator sequence

### Documentation
- [ ] README is complete user manual
- [ ] All 4 planning docs exist (PRD, CLAUDE, PLANNING, TASKS)
- [ ] prompts/ directory fully populated
- [ ] prompts/README.md documents best practices
- [ ] Usage examples in README show self-assessment scenarios
- [ ] Formula explanation clear for non-technical users

### Functionality
- [ ] Single report generation works
- [ ] Batch processing works
- [ ] All 4 skills generate appropriate feedback
- [ ] Self-assessment accuracy mentioned in all feedback
- [ ] Emoji usage matches tier specifications
- [ ] PDF format matches student template
- [ ] Grade breakdown shows self/base/penalty/final clearly

### Testing
- [ ] Unit tests pass (parser, extractors, calculators, router, skills)
- [ ] Integration tests pass (accurate, overconfident, humble scenarios)
- [ ] Edge case tests pass (range validation, missing self-grade, etc.)
- [ ] Sample reports generated for all tiers and reviewed by instructor
- [ ] Penalty calculations verified against manual calculations

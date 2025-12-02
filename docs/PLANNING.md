# Technical Planning & Architecture Document
## AutoGrade Report Generator

**Version:** 2.0 (Self-Assessment Based)
**Last Updated:** 2025-12-01

## 1. System Overview

### 1.1 High-Level Architecture

The AutoGrade Report Generator is a CLI-based automated grading system that transforms markdown assessment files into personalized, graded PDF reports **with self-assessment penalty calculation**. The system uses a multi-stage pipeline:

1. **Input**: Markdown assessment files with TRUE/FALSE criteria tables + Student self-grade (60-100)
2. **Parsing**: Extract criteria, count requirements met
3. **Self-Grade Extraction**: Extract student's claimed grade from PDF metadata or CSV
4. **Base Calculation**: Calculate grade from criteria met: `(met / 22) × 100`
5. **Penalty Calculation**: Apply exponential penalty for overconfident self-assessment
6. **Routing**: Determine performance tier (based on final grade) and select appropriate feedback skill
7. **Generation**: Use Claude API to generate tier-specific feedback **with self-assessment analysis**
8. **Formatting**: Create PDF matching student submission template with grade breakdown
9. **Output**: Professional grade report with personalized feedback and self-assessment accuracy commentary

### 1.2 Architecture Style

**Layered Architecture** with **Pipeline Pattern**

**Rationale**:
- **Layered**: Clear separation between parsing, self-grade extraction, business logic (penalty calculation), AI generation, and presentation
- **Pipeline**: Sequential data transformation (markdown → criteria → self-grade → base → penalty → final → tier → feedback → PDF)
- **Modular**: Each stage is independently testable and replaceable
- **Extensible**: Easy to add new skills, modify formula coefficients, or change self-grade extraction methods

---

## 2. C4 Model Diagrams

### 2.1 Context Diagram (Level 1)

```
┌─────────────────────────────────────────────────────────────┐
│                     System Context                          │
└─────────────────────────────────────────────────────────────┘

    [Course Instructor]
           │
           │ 1. Provides assessment markdown files
           │ 2. Provides student self-grades (PDF/CSV)
           │ 3. Runs CLI command
           │ 4. Receives PDF reports with grade breakdown
           ▼
    ┌──────────────────────────────────┐
    │                                  │
    │   AutoGrade Report Generator     │
    │   (CLI Application)              │
    │   - Self-Assessment Penalty      │
    │   - Tier-Based Feedback          │
    │                                  │
    └──────────────────────────────────┘
           │                    │
           │                    │
           ▼                    ▼
    [File System]         [Claude API]
    - Read .md files      - Generate feedback
    - Read self-grades    - Self-assessment analysis
    - Write PDF reports   - Tier-specific prompts
```

**Description**: Instructor provides markdown files and self-grades, system extracts self-grade, calculates base grade from criteria, applies penalty for overconfidence, calls Claude API for feedback with self-assessment commentary, and writes PDF reports with complete grade breakdown.

### 2.2 Container Diagram (Level 2)

```
┌────────────────────────────────────────────────────────────────┐
│                         Containers                             │
└────────────────────────────────────────────────────────────────┘

[Instructor] ──────────────────┐
                               │
                               ▼
                    ┌─────────────────────┐
                    │   CLI Application   │
                    │   (Python/Typer)    │
                    └─────────────────────┘
                               │
            ┌──────────────────┼──────────────────┬──────────────┐
            ▼                  ▼                  ▼              ▼
    ┌───────────────┐  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐
    │   Core Engine │  │ Self-Grade   │  │ Skill Library│  │ PDF Engine   │
    │   (Parser,    │  │ Extractor    │  │ (4 Claude    │  │ (ReportLab)  │
    │   Base Calc,  │  │ (PDF/CSV)    │  │  Skills with │  │ Grade        │
    │   Penalty     │  │              │  │  Self-Assess │  │ Breakdown    │
    │   Calc,       │  │              │  │  Analysis)   │  │ Display      │
    │   Router)     │  │              │  │              │  │              │
    └───────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
            │                  │                  │                  │
            ▼                  ▼                  ▼                  ▼
    ┌───────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐
    │  Assessment   │  │ Self-Grade   │  │  Claude API  │  │  PDF Files  │
    │  MD Files     │  │ Data (PDF/   │  │  (External)  │  │  (Output)   │
    │               │  │  CSV)        │  │              │  │             │
    └───────────────┘  └──────────────┘  └──────────────┘  └─────────────┘
```

**Description**:
- **CLI Application**: Entry point, orchestrates pipeline
- **Core Engine**: Business logic (parse, base calculation, penalty calculation, routing)
- **Self-Grade Extractor**: Extracts student's claimed grade from PDF metadata or CSV
- **Skill Library**: Four Claude-based feedback generators with self-assessment analysis
- **PDF Engine**: Report formatting with grade breakdown (self/base/penalty/final)
- **External Systems**: File system (assessments, self-grades, reports), Claude API

### 2.3 Component Diagram (Level 3) - Core Engine

```
┌───────────────────────────────────────────────────────────┐
│                  Core Engine Components                    │
└───────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │         MarkdownParser                  │
    │  - extract_criteria_table()             │
    │  - extract_metadata()                   │
    │  - validate_structure()                 │
    │  - count_requirements_met()             │
    └─────────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │       SelfGradeExtractor                │
    │  - extract_from_pdf(pdf_path)           │
    │  - extract_from_csv(csv_path)           │
    │  - validate_range(self_grade)           │
    │  - parse_self_grade_text()              │
    └─────────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │       BaseCalculator                    │
    │  - calculate_base(requirements_met)     │
    │  - formula: (met / 22) × 100            │
    │  - validate_criteria_count()            │
    └─────────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │       PenaltyCalculator                 │
    │  - calculate_scale(self_grade)          │
    │  - apply_penalty(self_grade, base)      │
    │  - formula: 0.086603 × e^(0.027465×x)   │
    │  - conditional_logic()                  │
    └─────────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │         SkillRouter                     │
    │  - determine_tier(final_grade)          │
    │  - select_skill(tier)                   │
    │  - get_tier_config()                    │
    └─────────────────────────────────────────┘
                     │
                     ▼
    ┌─────────────────────────────────────────┐
    │      FeedbackOrchestrator               │
    │  - generate_report(assessment_path)     │
    │  - batch_process(directory)             │
    │  - handle_errors()                      │
    │  - compile_grade_data()                 │
    └─────────────────────────────────────────┘
```

### 2.4 Component Diagram (Level 3) - Skill Library

```
┌───────────────────────────────────────────────────────────┐
│                 Skill Library Components                   │
└───────────────────────────────────────────────────────────┘

              ┌─────────────────────┐
              │    BaseSkill        │
              │  (Abstract)         │
              │  - generate()       │
              │  - insert_emojis()  │
              │  - analyze_self()   │ ← NEW: Self-assessment analysis
              └─────────────────────┘
                       △
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
┌────────────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐
│ Skill1         │ │ Skill2   │ │ Skill3     │ │ Skill4   │
│ Excellence     │ │ Good     │ │ Potential  │ │ Below    │
│ (90-100)       │ │ (80-89)  │ │ (55-79)    │ │ (<55)    │
│ - High emojis  │ │ - Mod em │ │ - Light em │ │ - Min em │
│ - Celebrate    │ │ - Balance│ │ - Motivate │ │ - Direct │
│ - Self-assess  │ │ - Growth │ │ - Realistic│ │ - Honesty│
└────────────────┘ └──────────┘ └────────────┘ └──────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │    ClaudeClient     │
            │  - send_prompt()    │
            │  - handle_retries() │
            │  - include_context()│ ← Self-grade, base, penalty
            └─────────────────────┘
```

---

## 3. Architecture Decision Records (ADRs)

### ADR-001: Use Self-Assessment Penalty Formula Instead of Simple Deduction

- **Status**: Accepted (Updated 2025-12-01)
- **Date**: 2025-12-01
- **Context**: Need a grading system that:
  - Encourages accurate self-evaluation (metacognitive skill)
  - Rewards humility (students who underestimate aren't penalized)
  - Penalizes overconfidence exponentially (higher claims = higher risk)
  - Maintains academic rigor and fairness
- **Decision**: Use **three-step self-assessment penalty formula**:
  1. `scale = 0.086603 × e^(0.027465 × self_grade)`
  2. `base_grade = (requirements_met / 22) × 100`
  3. If `self_grade > base_grade`: `final = max(0, base - (self - base) × scale)`
     Else: `final = base` (no penalty for humility)
- **Consequences**:
  - **Easier**: Grading becomes educational - teaches self-awareness
  - **Easier**: Students learn consequence of overconfidence vs. humility
  - **Harder**: Formula is complex - requires clear documentation
  - **Harder**: Self-grade extraction adds new input requirement
  - **Trade-off**: More sophisticated but more educational
- **Alternatives Considered**:
  | Alternative | Pros | Cons |
  |-------------|------|------|
  | Simple exponential decay (old) | Simple, lenient | Doesn't teach metacognition, too lenient |
  | Fixed penalty per FALSE | Predictable | No self-assessment component |
  | Manual instructor review | Fully personalized | Time-intensive, not reproducible |
- **Previous Version**: Simple `y = 0.0340 × e^(0.0446x)`, final = 100 - y (rejected as not right)

### ADR-002: Use Four Distinct Claude Skills with Self-Assessment Feedback

- **Status**: Accepted (Updated 2025-12-01)
- **Date**: 2025-12-01
- **Context**: Feedback must be personalized, tier-appropriate, AND address self-assessment accuracy.
- **Decision**: Create four separate Claude-based skills, each including self-assessment analysis:
  1. Excellence (90-100): Celebrate + comment on accuracy/humility
  2. Good (80-89): Balanced + comment on self-evaluation
  3. Potential (55-79): Motivate + encourage realistic self-view
  4. Below (<55): Direct + emphasize honest self-assessment
- **Consequences**:
  - **Easier**: Feedback addresses both performance AND metacognition
  - **Easier**: Students understand if penalty was due to overconfidence
  - **Harder**: Skills require additional context (self-grade, base, penalty)
  - **Trade-off**: More complex prompts, but richer feedback
- **Alternatives Considered**:
  | Alternative | Pros | Cons |
  |-------------|------|------|
  | Single skill with dynamic prompts | Less code | Hard to tune for self-assessment + tier |
  | Template-based (no AI) | Faster | Can't personalize self-assessment commentary |
  | Two-tier (performance + metacognition) | Simpler | Loses tier-specific tone nuance |

### ADR-003: Generate PDFs with Grade Breakdown Section

- **Status**: Accepted (Updated 2025-12-01)
- **Date**: 2025-12-01
- **Context**: Students need transparency into how penalty was calculated.
- **Decision**: PDFs include **Grade Breakdown** section showing:
  - Self-Grade (Claimed): X/100
  - Base Grade (Earned): Y.Y/100
  - Requirements Met: Z/22
  - Penalty Applied: -P.P points
  - **FINAL GRADE**: F/100
- **Consequences**:
  - **Easier**: Complete transparency - students see all calculations
  - **Easier**: Students can verify penalty math independently
  - **Harder**: PDF formatting must accommodate 5 grade values instead of 1
  - **Trade-off**: Slightly more complex PDF, but much better for learning
- **Alternatives Considered**:
  | Alternative | Pros | Cons |
  |-------------|------|------|
  | Show only final grade | Simple, clean | Students don't understand penalty |
  | Show self vs. final only | Compact | Missing base grade context |
  | Include formula explanation | Educational | Too verbose for PDF report |

### ADR-004: Extract Self-Grade from PDF Metadata or CSV

- **Status**: Accepted
- **Date**: 2025-12-01
- **Context**: Need student's claimed grade as input. Students submitted PDFs.
- **Decision**: Support two extraction methods:
  1. **PDF metadata**: Read custom field "self_grade" from PDF properties
  2. **CSV file**: Read from CSV with columns (student_id, self_grade)
  3. **Fallback**: Prompt instructor if not found
- **Consequences**:
  - **Easier**: Flexible input - works with multiple submission formats
  - **Easier**: CSV batch processing efficient for large classes
  - **Harder**: Need PDF parsing library (PyPDF2), CSV validation
  - **Trade-off**: More input complexity, but accommodates real-world scenarios
- **Alternatives Considered**:
  | Alternative | Pros | Cons |
  |-------------|------|------|
  | Manual CLI argument per student | Simple | Tedious for batch (35 students) |
  | Hardcode in assessment markdown | Centralized | Violates separation of concerns |
  | OCR from PDF text | Automatic | Error-prone, computationally expensive |

### ADR-005: Sequential Processing for Batch Mode (No Parallelism)

- **Status**: Accepted
- **Date**: 2025-11-30
- **Context**: Batch processing 35 students could benefit from parallelism, but adds complexity.
- **Decision**: Implement sequential processing initially. Process one student at a time in batch mode.
- **Consequences**:
  - **Easier**: Simpler code, easier debugging, no race conditions
  - **Harder**: Slower for large batches (90 min for 35 students vs. potentially 20 min with parallelism)
  - **Trade-off**: Acceptable for current scale (< 50 students), can optimize later if needed
- **Alternatives Considered**:
  | Alternative | Pros | Cons |
  |-------------|------|------|
  | Parallel with ThreadPoolExecutor | 4-5x faster | Complex error handling, API rate limits |
  | Async with asyncio | Most efficient | Steep learning curve |
  | No batch mode (manual runs) | Simplest | Tedious (35 CLI calls) |

---

## 4. Data Architecture

### 4.1 Data Models

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Criterion:
    """Individual assessment criterion."""
    number: int
    name: str
    met: bool  # TRUE or FALSE

@dataclass
class AssessmentData:
    """Parsed assessment information."""
    student_name: str
    student_id: str
    repository_url: str
    criteria: List[Criterion]
    requirements_met: int  # NEW: Count of TRUE criteria (not FALSE!)
    key_findings: Optional[str] = None  # Extracted from markdown

@dataclass
class SelfGradeData:
    """Student's self-assessment grade."""
    student_id: str
    self_grade: int  # 60-100
    source: str  # "pdf_metadata", "csv", "manual"

@dataclass
class GradeCalculation:
    """Complete grade calculation breakdown."""
    self_grade: int  # Student's claim (60-100)
    base_grade: float  # Earned from criteria: (met/22) × 100
    scale: float  # Exponential scale: 0.086603 × e^(0.027465 × self)
    penalty: float  # Applied penalty (0 if humble, positive if overconfident)
    final_grade: float  # After penalty: max(0, base - penalty)

@dataclass
class GradedReport:
    """Complete graded report data."""
    assessment: AssessmentData
    self_grade_data: SelfGradeData
    calculation: GradeCalculation
    tier: str  # "Excellence", "Good", "Potential", "Below"
    feedback: str  # Includes self-assessment analysis
    emoji_count: int
    timestamp: str
```

### 4.2 Data Flow

```
1. File System (Assessment .md + Self-Grade PDF/CSV)
          ↓
2. MarkdownParser → AssessmentData (requirements_met)
          ↓
3. SelfGradeExtractor → SelfGradeData (self_grade)
          ↓
4. BaseCalculator → float (base_grade = (met/22) × 100)
          ↓
5. PenaltyCalculator → GradeCalculation (scale, penalty, final)
          ↓
6. SkillRouter → (tier: str, skill: BaseSkill)
          ↓
7. Selected Skill (via Claude API) → str (feedback with self-assessment)
          ↓
8. PDFFormatter → GradedReport + PDF bytes (with breakdown)
          ↓
9. File System (Report .pdf)
```

### 4.3 Data Storage

| Data Type | Storage | Retention | Access Pattern |
|-----------|---------|-----------|----------------|
| Assessment markdown | File system (.md) | Permanent | Read-only during processing |
| Self-grades | PDF metadata or CSV | Permanent | Read-only during processing |
| Generated PDFs | File system (.pdf) | Permanent | Write-once, read-many |
| Grading config | YAML file (formula_params.yaml) | Permanent | Read at startup |
| API keys | .env file (not in repo) | Permanent | Read at startup |
| Logs | File system (logs/autograde.log) | 30 days | Append-only |
| Prompt documentation | Markdown (prompts/) | Permanent | Write during development |

---

## 5. API Design

### 5.1 API Overview

**CLI Interface** (not REST API)

Using **Typer** framework for type-safe, self-documenting CLI.

### 5.2 CLI Commands

| Command | Description | Arguments | Example |
|---------|-------------|-----------|---------|
| `generate-report` | Generate single PDF report | `--input PATH --self-grade INT --output PATH` | `generate-report --input assessments/63698.md --self-grade 95 --output reports/63698.pdf` |
| `batch-generate` | Process all assessments in directory | `--input-dir PATH --self-grades CSV --output-dir PATH` | `batch-generate --input-dir WorkSubmissions03/ --self-grades self_grades.csv --output-dir reports/` |
| `verify-grade` | Calculate grade without generating report | `--input PATH --self-grade INT` | `verify-grade --input assessments/63698.md --self-grade 100` |
| `validate-formula` | Test penalty formula with sample values | `--self-grade INT --requirements-met INT` | `validate-formula --self-grade 100 --requirements-met 18` |

### 5.3 Command Specifications

```python
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def generate_report(
    input: Path = typer.Option(..., "--input", "-i", help="Path to assessment markdown file"),
    self_grade: int = typer.Option(..., "--self-grade", "-s", help="Student's claimed grade (60-100)"),
    output: Path = typer.Option(..., "--output", "-o", help="Path for output PDF report"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress")
):
    """
    Generate a single graded PDF report with self-assessment penalty.

    Parses criteria table, extracts self-grade, calculates base grade,
    applies penalty for overconfidence, determines tier, generates feedback
    via Claude API (with self-assessment analysis), and creates PDF with
    complete grade breakdown.
    """
    # Validate self-grade range
    if not (60 <= self_grade <= 100):
        raise typer.BadParameter("Self-grade must be between 60 and 100")

    # Implementation...

@app.command()
def batch_generate(
    input_dir: Path = typer.Option(..., "--input-dir", help="Directory containing assessment markdown files"),
    self_grades: Path = typer.Option(..., "--self-grades", help="CSV file with student_id,self_grade columns"),
    output_dir: Path = typer.Option(..., "--output-dir", help="Directory for output PDF reports"),
    pattern: str = typer.Option("repo_assessment.md", "--pattern", help="Filename pattern to match"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress")
):
    """
    Generate PDF reports for all assessments with self-grades from CSV.

    Scans input_dir for files matching pattern, loads self-grades from CSV,
    processes each sequentially with penalty calculation, and saves reports
    to output_dir. Displays progress and summary statistics.
    """
    # Validate CSV exists
    if not self_grades.exists():
        raise typer.BadParameter(f"Self-grades CSV not found: {self_grades}")

    # Implementation...

@app.command()
def validate_formula(
    self_grade: int = typer.Option(..., "--self-grade", help="Claimed grade (60-100)"),
    requirements_met: int = typer.Option(..., "--requirements-met", help="Criteria met (0-22)")
):
    """
    Test the self-assessment penalty formula with sample values.

    Shows complete calculation breakdown:
    - Scale calculation
    - Base grade calculation
    - Penalty (if applicable)
    - Final grade
    - Self-assessment accuracy analysis
    """
    # Validate ranges
    if not (60 <= self_grade <= 100):
        raise typer.BadParameter("Self-grade must be between 60 and 100")
    if not (0 <= requirements_met <= 22):
        raise typer.BadParameter("Requirements met must be between 0 and 22")

    # Calculate and display
    base = (requirements_met / 22) * 100
    scale = 0.086603 * math.exp(0.027465 * self_grade)

    if self_grade > base:
        penalty = (self_grade - base) * scale
        final = max(0, base - penalty)
    else:
        penalty = 0
        final = base

    typer.echo(f"\n=== Penalty Formula Calculation ===")
    typer.echo(f"Self-Grade (claimed): {self_grade}/100")
    typer.echo(f"Requirements Met: {requirements_met}/22")
    typer.echo(f"Base Grade (earned): {base:.2f}/100")
    typer.echo(f"Scale Multiplier: {scale:.4f}")
    typer.echo(f"Penalty Applied: {penalty:.2f} points")
    typer.echo(f"Final Grade: {final:.2f}/100")

    if penalty > 0:
        typer.echo(f"\n⚠️  Overconfident: Claimed {self_grade}, earned {base:.1f}")
    elif self_grade < base:
        typer.echo(f"\n✓ Humble: Claimed {self_grade}, earned {base:.1f} (no penalty!)")
    else:
        typer.echo(f"\n✓ Accurate: Perfect self-assessment!")
```

### 5.4 Error Responses

| Error Type | Exit Code | Message Format |
|------------|-----------|----------------|
| File Not Found | 1 | `Error: Assessment file not found: {path}` |
| Invalid Format | 2 | `Error: Invalid assessment format in {file}: {details}` |
| Self-Grade Out of Range | 2 | `Error: Self-grade {value} out of range [60, 100]` |
| Self-Grade Not Found | 2 | `Error: No self-grade found for student {id} in CSV` |
| API Error | 3 | `Error: Claude API request failed: {reason}` |
| PDF Generation Failed | 4 | `Error: PDF generation failed for {student}: {reason}` |
| Configuration Error | 5 | `Error: Invalid configuration: {issue}` |

---

## 6. Infrastructure & Deployment

### 6.1 Deployment Architecture

```
Instructor's Local Machine
├── Python 3.9+ Virtual Environment
│   ├── autograde-report-generator/ (installed package)
│   └── dependencies (from requirements.txt)
│       ├── typer
│       ├── reportlab
│       ├── PyPDF2 (for self-grade extraction)
│       ├── anthropic (Claude API)
│       └── pyyaml
├── .env (API keys, config)
└── File System
    ├── WorkSubmissions03/ (input: assessment .md files)
    ├── self_grades.csv (input: student_id, self_grade)
    └── reports/ (output: generated .pdf files)

External Services:
└── Claude API (Anthropic) - HTTPS connection
```

### 6.2 Environment Configuration

| Environment | Purpose | Location | Config File |
|-------------|---------|----------|-------------|
| Development | Local testing | Instructor's laptop | `.env.dev` |
| Production | Actual grading | Instructor's laptop | `.env` |

(Note: Only one environment needed - this is a local tool, not a web service)

### 6.3 Installation Steps

```bash
# 1. Clone repository
git clone <repo-url>
cd autograde-report-generator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with Claude API key

# 5. Verify installation
python cli.py --help

# 6. Test penalty formula
python cli.py validate-formula --self-grade 100 --requirements-met 18

# 7. Test with sample (single report)
python cli.py generate-report \
  --input data/sample_inputs/perfect_assessment.md \
  --self-grade 100 \
  --output test_output.pdf

# 8. Test batch processing
python cli.py batch-generate \
  --input-dir data/sample_inputs/ \
  --self-grades data/sample_self_grades.csv \
  --output-dir test_reports/
```

---

## 7. Security Architecture

### 7.1 Authentication

- **Claude API**: API key authentication
  - Stored in `.env` file (git-ignored)
  - Read at runtime via `os.environ.get("CLAUDE_API_KEY")`
  - Never logged or printed to console

### 7.2 Authorization

- **File System**: Relies on OS-level permissions
  - Input files: Read-only access required
  - Output directory: Write access required
  - Log files: Append access required

### 7.3 Data Protection

- **Encryption at rest**: No (files stored locally, not transmitted)
- **Encryption in transit**: Yes (Claude API uses HTTPS)
- **PII handling**:
  - Student names/IDs in assessment markdown are read but not logged
  - Self-grades treated as sensitive - not logged individually
  - Only appear in final PDF output
  - Logs contain only participant IDs (e.g., "63698"), not real names or self-grades

### 7.4 Input Validation

```python
def validate_self_grade(self_grade: int) -> None:
    """Validate self-grade is in acceptable range."""
    if not isinstance(self_grade, int):
        raise TypeError(f"Self-grade must be integer, got {type(self_grade)}")

    if not (60 <= self_grade <= 100):
        raise ValueError(
            f"Self-grade {self_grade} out of range. "
            f"Valid range is 60-100 per assignment requirements."
        )

def validate_assessment_file(file_path: Path) -> None:
    """Validate assessment file before processing."""
    # Check file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check file size (prevent DoS from huge files)
    max_size = 5 * 1024 * 1024  # 5 MB
    if file_path.stat().st_size > max_size:
        raise ValueError(f"File too large: {file_path.stat().st_size} bytes")

    # Check file extension
    if file_path.suffix != ".md":
        raise ValueError(f"Invalid file type: {file_path.suffix}. Expected .md")

    # Validate content encoding
    try:
        file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        raise ValueError(f"Invalid encoding. File must be UTF-8: {file_path}")

def validate_requirements_met(count: int) -> None:
    """Validate criteria count is possible."""
    if not isinstance(count, int):
        raise TypeError(f"Requirements met must be integer, got {type(count)}")

    if not (0 <= count <= 22):
        raise ValueError(
            f"Requirements met {count} out of range. "
            f"Valid range is 0-22 (total criteria)."
        )
```

---

## 8. Extensibility Design

### 8.1 Extension Points

| Extension Point | Purpose | Interface |
|-----------------|---------|-----------|
| New Skill | Add feedback tier | Inherit from `BaseSkill`, implement `generate_feedback()` with self-assessment |
| Custom Penalty Formula | Change penalty algorithm | Modify `PenaltyCalculator.calculate_scale()` |
| Custom Base Formula | Change base calculation | Modify `BaseCalculator.calculate_base()` |
| PDF Template | Alter report format | Modify `PDFFormatter.generate()` |
| New Self-Grade Source | Read from LMS API | Implement `SelfGradeExtractor` interface |

### 8.2 Plugin Architecture (Future)

```python
# Future: Plugin system for custom penalty formulas
class PenaltyFormulaPlugin(ABC):
    @abstractmethod
    def calculate_scale(self, self_grade: int) -> float:
        """Return scale multiplier for given self-grade."""
        pass

    @abstractmethod
    def apply_penalty(self, self_grade: int, base_grade: float) -> float:
        """Return final grade after penalty."""
        pass

# Registration
formula_registry = FormulaRegistry()
formula_registry.register("exponential", ExponentialPenaltyFormula())
formula_registry.register("custom", CustomPenaltyFormula())
```

### 8.3 Configuration-Driven Behavior

```yaml
# config/formula_params.yaml
# Changing values here alters behavior without code changes

penalty_formula:
  scale_coefficient_a: 0.086603  # ← Adjust for steeper/gentler penalties
  scale_exponent_b: 0.027465     # ← Adjust for scale growth rate
  total_requirements: 22
  self_grade_range:
    min: 60  # ← Configurable minimum claim
    max: 100

performance_tiers:
  excellence:
    min_grade: 90
    max_grade: 100
    skill: "Skill1Excellence"
    emoji_density: high
    self_assessment_feedback: true
  # Add new tier here:
  # outstanding:
  #   min_grade: 95
  #   max_grade: 100
  #   skill: "Skill0Outstanding"
  #   self_assessment_feedback: true
```

---

## 9. Performance Considerations

### 9.1 Bottlenecks Identified

| Area | Concern | Mitigation |
|------|---------|------------|
| Claude API calls | Each skill call takes 5-15 seconds | Accept as unavoidable; Claude needed for quality feedback |
| Self-grade extraction (PDF) | PDF parsing can be slow | Cache extracted values; use CSV for batch |
| Penalty calculation | Exponential function (math.exp) | Negligible - O(1) computation |
| PDF generation | Complex layouts slow rendering | Use simple, optimized templates |
| File I/O | Reading 35 large markdown files | Files are small (< 50 KB each), not a bottleneck |
| Sequential processing | Batch takes 90 minutes for 35 students | Acceptable; can parallelize later |

### 9.2 Caching Strategy

- **Not needed for grades**: Each report generated once, no repeated computations
- **Future**: Cache parsed assessment data if re-running same inputs
- **Future**: Cache self-grade extractions from PDFs (save to intermediate CSV)

### 9.3 Scaling Strategy

- **Current**: Sequential processing, single-threaded
- **If > 100 students**:
  - Horizontal: Use `ThreadPoolExecutor` with 4-5 workers (respect Claude API rate limits)
  - Vertical: Run on more powerful machine (not necessary)
  - Batch optimization: Extract all self-grades to CSV first, then process

---

## 10. Monitoring & Observability

### 10.1 Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/autograde.log'),
        logging.StreamHandler()  # Console output
    ]
)

logger = logging.getLogger(__name__)

# Usage in code
logger.info(f"Processing assessment: {file_path}")
logger.info(f"Self-grade: {self_grade}, Base: {base:.1f}, Penalty: {penalty:.1f}, Final: {final:.1f}")
logger.warning(f"Missing metadata in {file_path}, using defaults")
logger.error(f"API call failed: {error}", exc_info=True)
```

**Log levels**:
- **DEBUG**: Detailed function calls, variable values (only when `--verbose`)
- **INFO**: Normal operation (file processed, grades calculated, report generated)
- **WARNING**: Recoverable issues (missing optional metadata, self-grade out of typical range)
- **ERROR**: Failures (API errors, invalid files, self-grade missing)
- **CRITICAL**: System failures (config missing, unrecoverable)

### 10.2 Progress Tracking

```python
from tqdm import tqdm

def batch_generate(input_dir: Path, self_grades_csv: Path, output_dir: Path):
    """Generate reports with progress bar."""
    files = list(input_dir.glob("*/repo_assessment.md"))
    self_grades = load_self_grades(self_grades_csv)

    with tqdm(total=len(files), desc="Generating reports") as pbar:
        for file in files:
            try:
                student_id = extract_student_id(file)
                self_grade = self_grades.get(student_id)

                if not self_grade:
                    logger.error(f"No self-grade for {student_id}, skipping")
                    pbar.set_postfix({"current": student_id, "status": "✗ (no self-grade)"})
                    pbar.update(1)
                    continue

                generate_report(file, self_grade, output_dir)
                pbar.set_postfix({"current": student_id, "status": "✓"})
            except Exception as e:
                logger.error(f"Failed: {file}", exc_info=True)
                pbar.set_postfix({"current": student_id, "status": "✗"})
            finally:
                pbar.update(1)
```

### 10.3 Metrics

| Metric | Type | Purpose |
|--------|------|---------|
| Reports Generated | Counter | Track successful completions |
| Self-Grade Extraction Failures | Counter | Identify students missing self-grades |
| Average Penalty Applied | Histogram | Understand overconfidence distribution |
| Processing Time per Report | Histogram | Identify slow outliers |
| API Call Latency | Histogram | Monitor Claude API performance |
| Error Count by Type | Counter | Identify common failure modes |

---

## 11. Technical Debt Register

| ID | Description | Impact | Priority | Estimated Effort |
|----|-------------|--------|----------|------------------|
| TD-001 | No parallelism in batch mode | Slow for large batches (>50) | P2 | 4 hours |
| TD-002 | Hardcoded tier thresholds in router | Hard to adjust tiers | P3 | 2 hours |
| TD-003 | No retry logic for Claude API | Transient failures cause report skip | P1 | 3 hours |
| TD-004 | Limited PDF template customization | Instructor can't change layout | P3 | 8 hours |
| TD-005 | No validation of criteria count (assumes 22) | Breaks if assignment has different criteria | P2 | 2 hours |
| TD-006 | Self-grade extraction only supports PDF metadata/CSV | Can't read from LMS API | P3 | 6 hours |
| TD-007 | No caching of extracted self-grades from PDFs | Re-parsing slow for re-runs | P3 | 3 hours |

---

## 12. Research Components

### 12.1 Self-Assessment Penalty Formula Analysis

**Algorithm**: Exponential Scale Multiplier with Conditional Penalty

**Formula**:
```
Step 1: scale = 0.086603 × e^(0.027465 × self_grade)
Step 2: base_grade = (requirements_met / 22) × 100
Step 3: if self_grade > base_grade:
            penalty = (self_grade - base_grade) × scale
            final_grade = max(0, base_grade - penalty)
        else:
            final_grade = base_grade
```

**Complexity**:
- Scale calculation: O(1) - constant time (math.exp)
- Base calculation: O(1) - simple division
- Penalty application: O(1) - arithmetic
- **Overall**: O(1)

**Properties**:
1. **Monotonicity**: Higher self-grade claims → higher scale → higher penalty risk
2. **Asymmetry**: Rewards underestimation (no penalty), penalizes overestimation
3. **Non-linearity**: Penalty grows exponentially with claim height AND gap size
4. **Bounded**: Final grade capped at [0, 100], penalty capped at base (can't go negative)

**Validation**:
```python
# Test cases from grading_formula_description.md
test_cases = [
    # (self, met, expected_final)
    (100, 22, 100.0),   # Perfect accuracy
    (100, 21, 89.4),    # Slight overconfidence
    (100, 18, 57.2),    # Major overconfidence
    (60, 22, 100.0),    # Humble
    (80, 18, 81.8),     # Slightly underestimated
    (90, 18, 73.4),     # Overconfident
]

for self_grade, met, expected in test_cases:
    final = calculate_final_grade(self_grade, met)
    assert abs(final - expected) < 1.0, f"Failed for ({self_grade}, {met})"
```

### 12.2 Emoji Density Parameter

| Tier | Density | Words per Emoji | Example Ratio |
|------|---------|-----------------|---------------|
| Excellence | High | 20-30 | 10 emojis in 250 words |
| Good | Moderate | 50-70 | 5 emojis in 300 words |
| Potential | Light | 100-120 | 3 emojis in 350 words |
| Below | Minimal | Total: 1-2 | 2 emojis in 250 words |

**Sensitivity**: High - emoji usage strongly affects perceived tone

### 12.3 Prompt Engineering for Skills with Self-Assessment

Each skill requires carefully tuned prompts that include self-assessment context:

```python
# Example: Skill 1 (Excellence) prompt structure with self-assessment
excellence_prompt_template = """
You are providing feedback for a student who achieved a FINAL GRADE of {final_grade:.1f}/100 (Excellence tier).

PERFORMANCE BREAKDOWN:
- Self-Grade (claimed): {self_grade}
- Base Grade (earned from criteria): {base_grade:.1f}
- Requirements Met: {requirements_met}/22
- Penalty Applied: {penalty:.1f} points
- Final Grade: {final_grade:.1f}

SELF-ASSESSMENT ANALYSIS:
{self_assessment_analysis}

Assessment Data:
- Criteria Met: {met_count}/22
- Missed Criteria: {missed_list}
- Key Strengths: {strengths_from_markdown}

Generate 300-400 word feedback:
1. Enthusiastic opening celebrating their excellence (use 🎉 ✨ 🌟)
2. **Comment on their self-assessment accuracy** (accurate? humble? slightly overconfident?)
3. Highlight 2-3 specific accomplishments
4. Provide 1-2 growth areas (even top students improve)
5. Encourage continued development of metacognitive skills
6. Encouraging closing

Tone: Celebratory but professional
Emoji density: 1 per 20-30 words
"""
```

**Experimentation needed**:
- Test prompts with sample assessments across all self-assessment scenarios (accurate, humble, overconfident)
- Verify output length (250-450 words)
- Check emoji count matches tier
- Validate tone appropriateness (instructor review)
- Ensure self-assessment commentary is present and appropriate

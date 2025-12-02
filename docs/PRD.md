# Product Requirements Document (PRD)
## Student Assignment Grading & Report Generator

## 1. Project Overview & Background

- **Project Name**: AutoGrade Report Generator
- **Version**: 2.0 (Self-Assessment Based)
- **Date**: 2025-12-01
- **Author**: Runi Team

### 1.1 Problem Statement

Educators assessing student programming assignments face a time-consuming challenge when students submit **self-graded assessments**. The process requires:

- Reading through student's self-assigned grade (their claimed performance)
- Manually reviewing assessment markdown files to count actual criteria met
- Calculating penalties for overconfident self-assessments using complex exponential formulas
- Writing personalized feedback that addresses both performance AND self-assessment accuracy
- Formatting professional PDFs that match submission format
- Maintaining consistency across dozens of student reports

This process can take 20-40 minutes per student for a class of 35+ students, resulting in 12-20 hours of repetitive work.

### 1.2 Project Purpose

AutoGrade Report Generator is a Claude CLI agent that automates the conversion of self-assessed markdown files into professional, graded PDF reports with tier-appropriate feedback. The system:

- **Extracts self-grades** from student submission PDFs or metadata
- **Counts actual criteria met** from assessment markdown (TRUE/FALSE table)
- **Calculates base grade**: `(requirements_met / 22) × 100`
- **Applies penalty formula** if overconfident: `scale = 0.086603 × e^(0.027465 × self_grade)`
- **Generates personalized feedback** addressing both performance and self-assessment accuracy
- **Creates professional PDFs** matching student submission format
- **Scales feedback tone** with final grade (better grades = more emojis, more encouragement)
- **Ensures consistency** while maintaining personalization

### 1.3 Market Analysis

**Competitive Landscape**:
- **Manual grading tools** (Word/Google Docs): Flexible but time-intensive, no self-assessment penalty automation
- **LMS auto-graders** (Canvas, Moodle): Limited to simple quizzes, no self-assessment calibration
- **Peer assessment tools** (Kritik, Peergrade): Require student participation, not instructor-driven
- **Generic AI summarizers** (ChatGPT): Not tailored to self-grading penalty formulas

**Strategic Positioning**: First AI-powered tool specifically designed for self-assessment based grading with exponential penalty formulas and pedagogically-sound tier-based feedback addressing accuracy of self-perception.

### 1.4 Target Audience & Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Course Instructor | Primary User | Reduce grading time from 20 hours to 3 hours, teach students accurate self-assessment |
| Teaching Assistants | Secondary User | Standardize self-assessment penalty application, ensure fairness |
| Students | Beneficiary | Receive feedback on both work quality AND self-assessment accuracy |
| Department Head | Approver | Improve teaching efficiency, promote metacognitive skills |

---

## 2. Objectives & Success Metrics

### 2.1 Project Goals

- [ ] **Goal 1**: Reduce per-student grading time from 20 minutes to 3 minutes (85% reduction)
- [ ] **Goal 2**: Generate 100% consistent self-assessment penalty calculations across all students
- [ ] **Goal 3**: Produce PDF reports indistinguishable from manually-created ones
- [ ] **Goal 4**: Provide feedback that addresses BOTH performance quality AND self-assessment accuracy
- [ ] **Goal 5**: Process 35 student reports in under 120 minutes
- [ ] **Goal 6**: Help students develop better self-assessment calibration over time

### 2.2 Key Performance Indicators (KPIs)

| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| Processing Time per Report | < 4 minutes | Time from markdown input to PDF output |
| Grade Calculation Accuracy | 100% | Manual verification against self-grading formula |
| PDF Format Match | 95%+ similarity | Visual comparison with student submissions |
| Feedback Appropriateness | 90%+ instructor approval | Post-generation review survey |
| Self-Assessment Insight Quality | 85%+ | Instructor rating of "addressed overconfidence" feedback |
| System Reliability | 99%+ success rate | Failed generations / total attempts |

### 2.3 Acceptance Criteria

- [ ] Correctly extracts student's self-assigned grade from submission metadata
- [ ] Accurately parses markdown assessment files with TRUE/FALSE criteria
- [ ] Counts requirements met (TRUE criteria) correctly
- [ ] Calculates base grade: `(met / 22) × 100`
- [ ] Computes scale multiplier: `0.086603 × e^(0.027465 × self_grade)`
- [ ] Applies penalty only when `self_grade > base_grade`
- [ ] Routes to appropriate skill (90-100, 80-89, 55-79, <55) based on FINAL grade
- [ ] Generates PDFs matching student submission format
- [ ] Scales emoji usage with final grade (higher grades = more emojis)
- [ ] Includes feedback on self-assessment accuracy (overconfident vs humble vs accurate)
- [ ] Completes batch processing of 35 reports in under 120 minutes

---

## 3. Functional Requirements

### 3.1 Feature List (Prioritized)

| Priority | Feature | Description | User Story |
|----------|---------|-------------|------------|
| P0 (Must) | Self-Grade Extractor | Extract student's claimed grade from submission metadata or PDF | As an instructor, I want automatic extraction so I don't manually enter each student's claim |
| P0 (Must) | Markdown Parser | Extract TRUE/FALSE criteria from assessment files | As an instructor, I want the system to count criteria so I don't manually tally scores |
| P0 (Must) | Base Grade Calculator | Calculate `(requirements_met / 22) × 100` | As an instructor, I want to know what grade student actually earned |
| P0 (Must) | Penalty Calculator | Apply self-grading penalty formula when student overestimates | As an instructor, I want overconfidence penalized fairly and consistently |
| P0 (Must) | Skill Router | Select feedback skill (1-4) based on FINAL grade tier | As an instructor, I want feedback tone to match final performance |
| P0 (Must) | Skill 1: Excellence (90-100) | Generate encouraging feedback, address self-assessment, high emojis | As a top student, I want recognition plus insight into my self-perception accuracy |
| P0 (Must) | Skill 2: Good (80-89) | Generate balanced feedback, moderate emojis | As a good student, I want balanced feedback on performance and self-awareness |
| P0 (Must) | Skill 3: Potential (55-79) | Generate motivational feedback, light emojis | As a struggling student, I want encouragement plus reality check on self-assessment |
| P0 (Must) | Skill 4: Below Expectations (<55) | Generate constructive feedback, minimal emojis | As a failing student, I want clear guidance including self-assessment reflection |
| P0 (Must) | PDF Generator | Create PDFs matching student submission format | As an instructor, I want professional reports |
| P1 (Should) | Self-Assessment Analysis | Explicitly state if student over/under/accurately estimated | As a student, I want to know if I'm calibrated |
| P1 (Should) | Batch Processing | Process multiple students in sequence | As an instructor, I want to grade entire class with one command |
| P1 (Should) | Progress Tracking | Show current progress (e.g., "Processing 12/35") | As an instructor, I want to monitor long-running jobs |
| P2 (Nice) | Penalty Visualization | Show calculation breakdown in PDF | As a student, I want to understand how penalty was computed |
| P2 (Nice) | Export Summary CSV | Generate spreadsheet with self-grades, base grades, final grades, penalties | As an instructor, I want analytics on class self-assessment accuracy |

### 3.2 Use Cases

#### Use Case 1: Single Student Report with Accurate Self-Assessment

- **Actor**: Course Instructor
- **Preconditions**:
  - Markdown assessment file exists (e.g., `repo_assessment.md`)
  - File contains criteria table with TRUE/FALSE values
  - Student's self-grade is known (from submission PDF or metadata): **90**
  - Student metadata available (name, ID, repository)
- **Main Flow**:
  1. Instructor runs: `claude-code generate-report --input assessments/63698_assessment.md --self-grade 90 --output reports/63698_report.pdf`
  2. System parses markdown, counts TRUE criteria: **20/22**
  3. System calculates base grade: `(20/22) × 100 = 90.9%`
  4. System compares: `self_grade (90) ≤ base_grade (90.9)` → **No penalty** (accurate/humble)
  5. System sets final grade: **90.9%**
  6. System determines tier: 90.9% → **Skill 1 (Excellence)**
  7. System invokes Skill 1, passing self-assessment context: "Student accurately self-assessed"
  8. System generates feedback praising both work quality AND self-awareness
  9. System formats PDF with breakdown:
     - Self-Grade: 90
     - Base Grade: 90.9 (20/22 criteria met)
     - Penalty: 0 (accurate assessment)
     - Final Grade: 90.9
  10. System saves to `reports/63698_report.pdf`
  11. System displays: "✓ Report generated: 63698_report.pdf (Self: 90, Base: 90.9, Final: 90.9)"
- **Postconditions**: PDF exists with grade breakdown and feedback praising self-awareness

#### Use Case 2: Single Student Report with Overconfident Self-Assessment

- **Actor**: Course Instructor
- **Preconditions**:
  - Markdown assessment file exists
  - Student's self-grade: **100**
  - Actual criteria met: **18/22**
- **Main Flow**:
  1. Instructor runs: `generate-report --input assessments/63688.md --self-grade 100`
  2. System counts TRUE: **18/22**
  3. System calculates base: `(18/22) × 100 = 81.8%`
  4. System compares: `self_grade (100) > base_grade (81.8)` → **Apply penalty**
  5. System calculates scale: `0.086603 × e^(0.027465 × 100) = 1.35`
  6. System calculates penalty: `(100 - 81.8) × 1.35 = 24.6 points`
  7. System calculates final: `81.8 - 24.6 = 57.2%`
  8. System determines tier: 57.2% → **Skill 3 (Potential)**
  9. System invokes Skill 3, passing context: "Student significantly overestimated (claimed 100, earned 81.8)"
  10. System generates feedback addressing overconfidence: "You have potential, but your self-assessment was off. You claimed 100% but analysis shows 81.8% performance..."
  11. System formats PDF showing calculation breakdown
  12. System displays: "✓ Report generated: 63688_report.pdf (Self: 100, Base: 81.8, Penalty: -24.6, Final: 57.2)"
- **Postconditions**: PDF exists with penalty calculation and feedback addressing overconfidence

#### Use Case 3: Batch Report Generation with Mixed Self-Assessments

- **Actor**: Course Instructor
- **Preconditions**:
  - Directory with 35 assessment markdown files
  - CSV or metadata file with student self-grades
- **Main Flow**:
  1. Instructor runs: `batch-generate --input-dir WorkSubmissions03/ --self-grades students_self_grades.csv --output-dir reports/`
  2. System loads self-grades from CSV (participant_id, self_grade)
  3. System scans directory, finds 35 assessment files
  4. For each assessment:
     - Extract participant ID, load self-grade
     - Parse criteria, calculate base, apply penalty if needed
     - Route to skill, generate feedback
     - Create PDF
     - Display: "✓ 12/35: 63698 (Self: 90, Final: 90.9) ✓ 13/35: 63688 (Self: 100, Final: 57.2, PENALTY) ..."
  5. System generates summary statistics:
     - Average final grade: 67%
     - Students penalized: 18/35 (51%)
     - Average penalty when applied: -15.3 points
     - Most overconfident: Participant 63688 (-42.8 point penalty)
- **Postconditions**: 35 PDFs created, summary CSV with self-assessment analytics

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

- **Response time**: Generate single report in < 3 minutes (including LLM inference)
- **Throughput**: Process 35 reports in < 120 minutes (3.4 min/report average)
- **Resource utilization**:
  - Memory: < 512 MB during processing
  - Disk: < 50 MB per generated PDF
  - CPU: Leverage Claude API (no local compute limits)

### 4.2 Security Requirements

- **Authentication**: API keys stored in `.env` file, never in code
- **Authorization**: File system permissions respect OS-level access control
- **Data protection**:
  - Student data (names, IDs, self-grades) anonymized in logs
  - Self-grades treated as sensitive metadata
  - Assessment files read-only during processing
- **PII Handling**: Student names and self-grades appear only in final PDF, not in intermediate files

### 4.3 Scalability Requirements

- **Expected load**: 35-50 students per class, 1-2 classes per semester
- **Scaling strategy**:
  - Current: Sequential processing (sufficient for < 100 students)
  - Future: Parallel processing for > 100 students

### 4.4 Availability & Reliability

- **Uptime target**: 99% (excludes Claude API downtime)
- **Recovery time objective**: < 5 minutes (restart from failure point)
- **Fault tolerance**:
  - Individual file failures don't halt batch processing
  - Automatic retry on transient API errors (3 attempts)
  - Graceful degradation if PDF generation fails (fallback to markdown output)

---

## 5. Assumptions, Dependencies & Constraints

### 5.1 Assumptions

- Students submit self-grades in submission PDF or separate metadata file
- Assessment markdown files follow consistent format with criteria table
- All assessments use same 22 criteria
- Self-grades are in range 60-100 (as per formula specification)
- Instructor has Claude API access with sufficient quota
- Grading formula remains constant

### 5.2 External Dependencies

| Dependency | Type | Risk Level |
|------------|------|------------|
| Claude API | External | Medium - API downtime affects all operations |
| Python 3.9+ | Runtime | Low - Stable, widely available |
| Markdown parser library | External | Low - Mature libraries exist |
| PDF generation library | External | Medium - Formatting complexity |
| PDF reading library (for self-grade extraction) | External | Medium - Parsing student PDFs |
| File system access | System | Low - Standard OS operations |

### 5.3 Technical Constraints

- Claude API rate limits (affects batch processing speed)
- PDF formatting must match student submission template exactly
- Markdown parsing relies on consistent table structure
- Self-grade must be in valid range (60-100)
- Python environment required (not standalone executable)

### 5.4 Organizational Constraints

- **Budget**: Must use existing Claude API subscription
- **Time**: Project must complete before next assignment deadline (2 weeks)
- **Resources**: Single developer (instructor) with limited Python expertise
- **Privacy**: Must comply with university FERPA regulations (no cloud storage of student data)
- **Pedagogical**: Penalty formula is fixed (defined by course policy)

### 5.5 Out-of-Scope Items

- ❌ Manual grade overrides (instructor edits PDF after generation)
- ❌ Student appeals of self-assessment penalties
- ❌ Integration with LMS (Canvas, Moodle)
- ❌ Real-time grading
- ❌ Plagiarism detection
- ❌ Code execution or testing
- ❌ Multi-language support (English only)
- ❌ Mobile interface
- ❌ Modifying the penalty formula coefficients

---

## 6. Timeline & Milestones

### 6.1 Project Schedule

| Phase | Start | End | Deliverables |
|-------|-------|-----|--------------|
| Planning | Day 1 | Day 2 | PRD, Architecture docs, CLAUDE.md, TASKS.md |
| Core Development | Day 3 | Day 8 | Self-grade extractor, parser, base calculator, penalty calculator, router |
| Skills Development | Day 9 | Day 11 | 4 Claude skills with self-assessment feedback |
| PDF Generation | Day 12 | Day 13 | PDF formatter with grade breakdown |
| Testing | Day 14 | Day 15 | Unit tests, integration tests, sample reports |
| Documentation | Day 16 | Day 16 | README, usage guide, troubleshooting |
| Pilot Run | Day 17 | Day 17 | Process 5 real students, verify output |

### 6.2 Checkpoint Reviews

- [ ] **Day 2**: Architecture Review - Verify self-grading formula implementation approach
- [ ] **Day 8**: Core Functionality Demo - Test penalty calculation with sample data
- [ ] **Day 11**: Skills Review - Verify feedback addresses self-assessment accuracy
- [ ] **Day 13**: PDF Format Verification - Compare output with student submissions
- [ ] **Day 15**: Test Coverage Review - Ensure 70%+ coverage
- [ ] **Day 17**: Final Acceptance - Instructor approves for production use

---

## 7. Technical Specifications

### 7.1 Self-Grading Penalty Formula Details

**Complete Formula**:

```python
# Step 1: Calculate scale multiplier
scale = 0.086603 × e^(0.027465 × self_grade)

# Step 2: Calculate base grade (what student actually earned)
base_grade = (requirements_met / 22) × 100

# Step 3: Determine final grade
if self_grade > base_grade:  # Overestimated
    difference = self_grade - base_grade
    penalty = difference × scale
    final_grade = max(0, base_grade - penalty)
else:  # Underestimated or accurate
    final_grade = base_grade  # No penalty, reward humility
```

**Pre-calculated Scale Values**:
| Self-Grade | Scale Multiplier |
|------------|------------------|
| 60 | 0.45 |
| 70 | 0.59 |
| 80 | 0.78 |
| 90 | 1.03 |
| 100 | 1.35 |

**Example Calculations**:

| Scenario | Self | Met | Base | Scale | Penalty | Final | Explanation |
|----------|------|-----|------|-------|---------|-------|-------------|
| Perfect + Accurate | 100 | 22/22 | 100.0 | 1.35 | 0 | **100.0** | Claimed 100, earned 100, no penalty |
| Perfect + Humble | 60 | 22/22 | 100.0 | 0.45 | 0 | **100.0** | Claimed 60, earned 100, rewarded with full grade |
| Slight Overconfidence | 100 | 21/22 | 95.5 | 1.35 | -6.1 | **89.4** | Claimed 100, earned 95.5, 4.5pt gap × 1.35 scale |
| Major Overconfidence | 100 | 18/22 | 81.8 | 1.35 | -24.6 | **57.2** | Claimed 100, earned 81.8, 18.2pt gap × 1.35 scale |
| Realistic | 80 | 18/22 | 81.8 | 0.78 | 0 | **81.8** | Claimed 80, earned 81.8, no penalty (underestimated) |
| Moderate Overconfidence | 90 | 18/22 | 81.8 | 1.03 | -8.4 | **73.4** | Claimed 90, earned 81.8, 8.2pt gap × 1.03 scale |

### 7.2 Performance Tier Specifications

**Note**: Tiers are based on **FINAL GRADE** (after penalty), not base grade or self-grade.

#### Tier 1: Excellence (90-100)
- **Emoji Usage**: Frequent, celebratory (🎉 ✨ 🌟 💯 🚀 ⭐)
- **Tone**: Enthusiastic, congratulatory, may acknowledge self-assessment accuracy
- **Structure**:
  1. **Opening**: "Exceptional work! 🎉" / "Outstanding submission! ✨"
  2. **Performance Strengths**: 2-3 specific highlights from assessment
  3. **Self-Assessment Reflection**:
     - If accurate/humble: "Your self-assessment was spot-on/admirably humble"
     - If slightly overconfident: "Minor note: you estimated [self], earned [base], final [final]"
  4. **Critical Feedback**: 1-2 areas for improvement
  5. **Closing**: Encouragement to maintain excellence
- **Length**: 300-400 words

#### Tier 2: Good Work (80-89)
- **Emoji Usage**: Moderate, positive (👍 ✅ 💡 🔧)
- **Tone**: Positive but balanced, addresses self-assessment
- **Structure**:
  1. **Opening**: "Good overall project! 👍"
  2. **Performance Strengths**: 2 specific good areas
  3. **Performance Gaps**: 2-3 missing/weak areas
  4. **Self-Assessment Reflection**:
     - If penalty applied: "Your claimed [self] was higher than earned [base], resulting in penalty"
     - If no penalty: "Your self-assessment was realistic"
  5. **Closing**: Encouragement toward excellence
- **Length**: 350-450 words

#### Tier 3: Potential (55-79)
- **Emoji Usage**: Light, motivational (💪 📚 🔍)
- **Tone**: Encouraging but firm, addresses overconfidence directly
- **Structure**:
  1. **Opening**: "You have a lot of potential! 💪"
  2. **Potential Recognition**: What shows promise
  3. **Missing Elements**: Clearly enumerate what criteria weren't met
  4. **Self-Assessment Reality Check**:
     - "You estimated [self]%, but the work demonstrated [base]%. This overconfidence led to a penalty."
     - "Accurate self-assessment is a critical professional skill."
  5. **Action Items**: Specific steps to improve both work AND self-assessment calibration
  6. **Closing**: Belief in ability to improve
- **Length**: 400-500 words

#### Tier 4: Below Expectations (<55)
- **Emoji Usage**: Minimal, professional (📋 ⚠️)
- **Tone**: Constructive, direct, addresses harsh reality of self-assessment gap
- **Structure**:
  1. **Opening**: "This project did not meet expectations ⚠️"
  2. **Requirement Review**: Directive to review submission guidelines
  3. **Major Gaps**: High-level categories of what's missing
  4. **Self-Assessment Discussion**:
     - If major overconfidence: "You estimated [self]%, but the work only demonstrated [base]%. The significant gap (XX points) indicates a misalignment between perception and reality. The penalty formula amplified this to a final grade of [final]%."
     - "Developing accurate self-assessment is crucial for professional growth."
  5. **Path Forward**: Concrete steps for improvement in both work quality and self-reflection
  6. **Closing**: Offer of support, encouragement that improvement is possible
- **Length**: 350-450 words

---

## 8. Appendices

### 8.1 Glossary

| Term | Definition |
|------|------------|
| Self-Grade | The grade a student claims they deserve (60-100) |
| Requirements Met | Number of TRUE criteria in assessment (0-22) |
| Base Grade | What student actually earned: `(met / 22) × 100` |
| Scale Multiplier | Exponential factor based on self-grade: `0.086603 × e^(0.027465 × self_grade)` |
| Penalty | Points deducted for overconfidence: `(self - base) × scale` |
| Final Grade | Grade after penalty: `max(0, base - penalty)` or `base` if no penalty |
| Performance Tier | Grade range (Excellence, Good, Potential, Below) determining skill |
| Skill | Claude CLI feedback generator tuned for specific tier |

### 8.2 References

- Self-Grading Formula Specification (`grading_formula_description.md`)
- ISO/IEC 25010 Software Quality Model (referenced in assessments)
- FERPA Compliance Guidelines (student data privacy)
- Claude API Documentation (skill implementation)
- Metacognition Research (self-assessment accuracy pedagogy)

### 8.3 Sample Input (Assessment Markdown + Self-Grade)

**Assessment Markdown** (`repo_assessment.md`):
```markdown
# Repository Assessment: Sample Project
**Repository:** https://github.com/student/project

## Assessment Results

| # | Criterion | Met (TRUE/FALSE) |
|---|-----------|------------------|
| 1 | Product Requirements Document | TRUE |
| 2 | Architecture Document | TRUE |
| 3 | README File | FALSE |
| 4 | Modular Structure | TRUE |
...
| 22 | Quality Characteristics | TRUE |

**Criteria Met: 20/22**
```

**Student's Self-Grade** (from submission PDF metadata): **95**

### 8.4 Sample Output (PDF Report Structure)

```
┌─────────────────────────────────────────────────┐
│  Assignment 3 Grading Report                    │
│  Student: [Name]                                │
│  ID: [Student ID]                               │
│  Repository: [URL]                              │
├─────────────────────────────────────────────────┤
│  SELF-ASSESSMENT ANALYSIS:                      │
│  • Your Claimed Grade: 95%                      │
│  • Base Grade Earned: 90.9% (20/22 criteria)    │
│  • Difference: +4.1 points (overestimated)      │
│  • Scale Multiplier: 1.18                       │
│  • Penalty Applied: -4.8 points                 │
│                                                  │
│  FINAL GRADE: 86.1 / 100                        │
│  Performance Tier: Good                         │
├─────────────────────────────────────────────────┤
│  FEEDBACK:                                      │
│  Good overall project! 👍                       │
│                                                  │
│  You demonstrated strong capabilities with 20   │
│  out of 22 criteria met. However, your self-   │
│  assessment was slightly overconfident...       │
│  [350-450 word feedback addressing both         │
│   performance and self-assessment accuracy]     │
├─────────────────────────────────────────────────┤
│  CRITERIA SUMMARY:                              │
│  ✓ Met: 20/22                                   │
│  ✗ Missing: 2/22                                │
│    - README File (Comprehensive)                │
│    - Cost Analysis                              │
└─────────────────────────────────────────────────┘
```

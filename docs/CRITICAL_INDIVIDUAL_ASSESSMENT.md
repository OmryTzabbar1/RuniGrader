# CRITICAL: Individual Assessment Requirement

**Date:** 2025-12-01
**Rule:** MANDATORY for all Tier 2 students

---

## The Rule

**EACH STUDENT MUST BE ASSESSED INDIVIDUALLY**

For Tier 2 students (self-grade ≥ 80), you MUST:

1. **Clone their specific repository individually**
2. **Examine their actual code, documentation, and structure**
3. **Run all 10 skill validation commands for each student**
4. **Score based on what's actually in their repository**
5. **Create individual assessment report for each student**
6. **NO batch processing or estimating allowed**
7. **NO shortcuts or assumptions**
8. **NO using patterns from other students**

---

## Why This Matters

- Each student's work is unique
- Batch estimation is unfair and inaccurate
- Students deserve individual evaluation of their actual work
- Quality > Speed - we prioritize accurate grading

---

## Wrong Approach (NEVER DO THIS):

```python
# WRONG - Batch estimating based on TRUE count
for student in tier2_students:
    if student['true'] >= 19:
        estimated = 72
    elif student['true'] >= 16:
        estimated = 65
# This is WRONG and UNFAIR!
```

---

## Correct Approach (ALWAYS DO THIS):

```python
# CORRECT - Individual assessment
for student in tier2_students:
    # 1. Clone their repo
    clone_repository(student['github_url'])

    # 2. Assess EACH skill individually
    skill_1 = assess_project_planning(repo_path)  # Check PRD, architecture
    skill_2 = assess_code_documentation(repo_path)  # Check README, structure
    skill_3 = assess_security(repo_path)  # Check for secrets
    skill_4 = assess_testing(repo_path)  # Count tests, check coverage
    skill_5 = assess_research(repo_path)  # Look for notebooks, analysis
    skill_6 = assess_ui_ux(repo_path)  # Check screenshots, docs
    skill_7 = assess_version_mgmt(repo_path)  # Count commits, check prompts
    skill_8 = assess_costs(repo_path)  # Look for cost analysis
    skill_9 = assess_extensibility(repo_path)  # Check architecture
    skill_10 = assess_quality(repo_path)  # ISO standards

    # 3. Calculate actual score
    total = sum([skill_1, skill_2, ..., skill_10])

    # 4. Save individual report
    save_assessment_report(student['id'], all_skills, total)
```

---

## Time Investment

- Tier 1 student: ~2 minutes (simple formula)
- Tier 2 student: ~15-20 minutes (full 10-skill assessment)

**This is acceptable.** Quality over speed.

---

## Verification Checklist

For each Tier 2 student, verify:

- [ ] Repository cloned to temp directory
- [ ] All 10 skills assessed with actual evidence
- [ ] Individual assessment report created
- [ ] Specific strengths and weaknesses documented
- [ ] Final score calculated from actual skill scores
- [ ] Temp directory cleaned up

---

## Example: Student 38951

CORRECT Assessment Process:
1. Cloned: https://github.com/RonKozitsa/LLM_course
2. Checked PRD: 38KB, has all sections → Skill 1: 10/10
3. Checked README: 9.8KB comprehensive → Skill 2: 9.5/10
4. Ran security scan: No secrets → Skill 3: 10/10
5. Found TESTING.md: 150+ tests → Skill 4: 10/10
6. No notebooks found → Skill 5: 0/10
7. Has screenshots, good UX → Skill 6: 9/10
8. Git history good, no prompts/ → Skill 7: 6/10
9. No cost docs → Skill 8: 0/10
10. Angular architecture strong → Skill 9: 9/10
11. ISO standards met → Skill 10: 8.5/10

TOTAL: 72/100 (based on ACTUAL assessment)
vs Self-Grade: 95 (overconfident by 23 points)

---

## Summary

**NO SHORTCUTS. ASSESS EVERY TIER 2 STUDENT INDIVIDUALLY.**

This is the standard. This is non-negotiable.

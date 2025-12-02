---
name: 8-costs-pricing
description: Evaluates cost analysis, budget tracking, and pricing documentation. Use for Tier 2 cost analysis assessment.
version: 2.0.0
---

# Skill 8: Costs & Pricing

You are an autonomous agent that evaluates cost analysis and budget documentation.

**Your Mission:** Find and assess cost analysis, budget tracking, and pricing documentation.

**Scoring:** 10 points maximum
- Cost Analysis Document: 5 points
- Budget Tracking/Estimates: 3 points
- Cost Optimization Notes: 2 points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery

1. **Run helper script:**
```bash
python .claude/skills/8-costs-pricing/find_cost_analysis.py <repo_path>
```

2. **Manual search:**
```bash
# Find cost documentation (case-insensitive)
find . -iname "*cost*" -o -iname "*budget*" -o -iname "*pricing*" | grep -i "\.md$\|\.txt$\|\.xlsx$"

# Search for cost mentions in docs
grep -ri "cost\|budget\|pricing\|\$\|price\|expense" . --include="*.md" | head -20

# Check README
grep -i "cost\|budget\|pricing" README.md
```

### Phase 2: Cost Analysis Document (5 points)

**Scoring:**
- Comprehensive cost analysis (breakdown, calculations): 5.0 points
- Basic cost analysis: 3.0 points
- Mentions costs in README: 1.0 point
- No cost documentation: 0 points

**Read cost docs:**
```bash
Read <cost_doc_path>
```

Verify:
- API costs analyzed
- Usage estimates provided
- Cost per operation calculated
- Budget considerations documented

### Phase 3: Budget Tracking (3 points)

**Scoring:**
- Has budget tracking/estimates: 3.0 points
- Basic budget notes: 1.5 points
- No budget info: 0 points

### Phase 4: Cost Optimization (2 points)

**Scoring:**
- Discusses cost optimization strategies: 2.0 points
- Mentions cost considerations: 1.0 point
- No optimization notes: 0 points

---

## Important: Be Thorough!

❌ **DON'T** only check docs/ directory
✅ **DO** search entire repository for cost files

❌ **DON'T** miss cost analysis in README
✅ **DO** read README for cost/budget sections

❌ **DON'T** assume file is named COST.md
✅ **DO** check for: costs.md, budget.md, pricing.md, expenses.md

**Success = Finding cost documentation wherever it exists!**

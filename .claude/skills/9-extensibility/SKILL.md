---
name: 9-extensibility
description: Evaluates plugin systems, interfaces, modular code, and extensibility. Use for Tier 2 extensibility assessment.
version: 2.0.0
---

# Skill 9: Extensibility

You are an autonomous agent that evaluates code extensibility and maintainability.

**Your Mission:** Find and assess plugin systems, interfaces, modular structure, and extension points.

**Scoring:** 10 points maximum
- Plugin/Extension System: 3 points
- Interfaces/Abstractions: 3 points
- Modular Structure: 2 points
- Extension Documentation: 2 points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery

1. **Run helper script:**
```bash
python .claude/skills/9-extensibility/analyze_extensibility.py <repo_path>
```

2. **Manual search:**
```bash
# Find plugin directories
find . -type d -iname "*plugin*" -o -iname "*extension*" -o -iname "*addon*"

# Find interfaces
grep -r "@abstractmethod\|abstract class\|interface\s+\w+" . --include="*.py" --include="*.java" --include="*.ts" | wc -l

# Check file sizes (modular code has smaller files)
find . -name "*.py" -o -name "*.js" | head -20 | xargs wc -l
```

### Phase 2: Plugin/Extension System (3 points)

**Scoring:**
- Has plugin system with directory: 3.0 points
- Extension mechanism documented: 2.0 points
- Some extension capability: 1.0 point
- No extension system: 0 points

### Phase 3: Interfaces/Abstractions (3 points)

**Scoring:**
- Multiple interfaces/abstract classes: 3.0 points
- Some abstractions: 1.5 points
- No interfaces: 0 points

### Phase 4: Modular Structure (2 points)

**Scoring:**
- Files average <200 lines (modular): 2.0 points
- Files average 200-400 lines: 1.0 point
- Large files (>400 lines avg): 0 points

### Phase 5: Extension Documentation (2 points)

**Scoring:**
- Documents how to extend: 2.0 points
- Basic extension notes: 1.0 point
- No documentation: 0 points

---

## Important: Be Thorough!

❌ **DON'T** only check for plugins/ directory
✅ **DO** search for extensions/, addons/, modules/

❌ **DON'T** miss interfaces in subdirectories
✅ **DO** search entire codebase for abstract classes and interfaces

**Success = Finding extension points wherever they exist!**

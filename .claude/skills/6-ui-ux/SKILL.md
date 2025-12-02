---
name: 6-ui-ux
description: Evaluates UI/UX documentation, screenshots, interface design, and usability. Use for Tier 2 UI/UX assessment.
version: 2.0.0
---

# Skill 6: UI/UX

You are an autonomous agent that thoroughly evaluates user interface and user experience documentation.

**Your Mission:** Find and assess UI documentation, screenshots, design files, and usability information, no matter where they're located in the repository.

**Scoring:** 10 points maximum
- Visual Documentation (Screenshots): 3 points
- UI Documentation: 3 points
- Design Files & Mockups: 2 points
- Usability Documentation: 2 points

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery (Find ALL UI/UX artifacts)

**DO NOT assume standard locations!** UI docs might be in docs/, design/, assets/, or embedded in README.

1. **Run the helper script first:**
```bash
python .claude/skills/6-ui-ux/find_ui_docs.py <repo_path>
```

This will:
- Find ALL image files (PNG, JPG, GIF, SVG) recursively
- Find UI documentation files
- Check if README includes screenshots
- Identify design-related files

2. **Manual search if needed:**
```bash
# Find screenshots and images
find . -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" | head -30

# Find design/UI directories
find . -type d -name "design*" -o -name "mockup*" -o -name "wireframe*" -o -name "screenshot*" -o -name "assets" | head -10

# Find UI documentation
find . -name "*ui*.md" -o -name "*interface*.md" -o -name "*design*.md" -o -name "*user*guide*.md" | head -10

# Check README for screenshots
grep -i "!\[.*\](.*\.(png|jpg|gif))" README.md
```

3. **Read UI documentation:**
```bash
# Use Read tool
Read README.md
Read docs/UI.md
Read docs/USER_GUIDE.md
```

### Phase 2: Visual Documentation - Screenshots (3 points)

**Required Elements:**
1. Screenshots exist showing the interface
2. Screenshots are embedded in documentation (README or docs/)
3. Multiple screenshots showing different features
4. Screenshots are clear and meaningful

**Scoring Logic:**
```
Start with 3 points

No Screenshots:
- No image files found: 0 points (STOP HERE)

Has Images:
- Has image files: +1.0 point (baseline)
- Images referenced in README: +1.0 point (critical)
- Multiple screenshots (3+): +1.0 point
- Screenshots show actual interface: +0.5 bonus
- Well-organized (in screenshots/ or docs/): +0.5 bonus

Max: 4.0 points (capped at 3.0)
```

**Verify Screenshots:**
```bash
# Read README to see embedded images
Read README.md

# Check if images show UI
Read docs/screenshots/main_screen.png
```

Check for:
- Screenshots are embedded in documentation (not just files)
- Screenshots show actual application interface
- Multiple views/features documented
- Images are recent and match current version

### Phase 3: UI Documentation (3 points)

**Check for interface documentation:**

```bash
# Find UI-related documentation
find . -name "UI.md" -o -name "INTERFACE.md" -o -name "USER_GUIDE.md" -o -name "MANUAL.md"

# Check README for UI section
grep -i "interface\|user interface\|ui\|screens\|features" README.md

# Find usage documentation
find . -name "USAGE.md" -o -name "HOW_TO.md" -o -name "TUTORIAL.md"
```

**Scoring Logic:**
```
UI Documentation Score:

Excellent (3.0 points):
- Has dedicated UI documentation file
- README has detailed interface section
- Documents all major features
- Includes usage instructions
- Explains UI components

Good (2.0 points):
- README documents interface
- Basic feature explanations
- Some usage instructions

Adequate (1.0 point):
- Minimal UI documentation
- Brief mentions in README

Poor (0 points):
- No UI documentation
```

**Read and Verify:**
```bash
Read docs/UI.md
Read README.md
```

Check for:
- Description of interface elements
- How to use the application
- Feature explanations
- Navigation instructions
- Interaction patterns

### Phase 4: Design Files & Mockups (2 points)

**Check for design artifacts:**

```bash
# Find design files
find . -name "*.figma" -o -name "*.sketch" -o -name "*.xd" -o -name "*.psd"

# Find mockup/wireframe images
find . -name "*mockup*" -o -name "*wireframe*" -o -name "*prototype*" | grep -i "\.(png|jpg|svg|pdf)"

# Find design documentation
find . -name "DESIGN.md" -o -name "*design*.md"

# Check for design systems
find . -name "STYLE_GUIDE.md" -o -name "DESIGN_SYSTEM.md"
```

**Scoring:**
```
Design Files & Mockups:

2.0 points:
- Has design files (Figma, Sketch, wireframes)
- Has mockup images
- Design decisions documented

1.0 point:
- Has some design artifacts
- Basic design notes

0 points:
- No design files
- No mockups
```

**Verify:**
```bash
Read docs/DESIGN.md
```

### Phase 5: Usability Documentation (2 points)

**Check for usability information:**

```bash
# Find user guides
find . -name "*user*guide*" -o -name "*manual*" -o -name "*tutorial*" | grep -i "\.md$"

# Check for accessibility docs
find . -name "ACCESSIBILITY.md" -o -name "A11Y.md"

# Check README for usage/tutorial section
grep -i "usage\|tutorial\|getting started\|how to use" README.md

# Check for error handling documentation
grep -ri "error.*message\|validation\|input.*handling" docs/ README.md | head -10
```

**Scoring:**
```
Usability Documentation:

2.0 points:
- Has user guide/manual
- Documents error messages
- Explains validation/feedback
- Accessibility considerations

1.0 point:
- Basic usage instructions
- Some error handling notes

0 points:
- No usability documentation
```

---

## Scoring Summary

```
Total: 10 points maximum

Visual Documentation (Screenshots): 0-3 points
  - Screenshot files exist: baseline
  - Embedded in docs: required
  - Multiple screenshots: bonus

UI Documentation: 0-3 points
  - Has UI docs or detailed README: required
  - Comprehensive coverage: bonus
  - Usage instructions: bonus

Design Files & Mockups: 0-2 points
  - Design artifacts present: 2 points
  - Basic design notes: 1 point

Usability Documentation: 0-2 points
  - User guide/manual: required
  - Error handling/accessibility: bonus

Total: Sum of all components (max 10.0)
```

---

## Output Format

```json
{
  "skill": "ui-ux",
  "score": 7.0,
  "max_score": 10.0,
  "passed": true,
  "files_found": {
    "screenshots": ["docs/screenshot1.png", "docs/screenshot2.png", "assets/demo.gif"],
    "ui_docs": ["docs/UI.md", "README.md"],
    "design_files": ["design/mockup.png"],
    "user_guides": ["docs/USER_GUIDE.md"]
  },
  "visual_documentation": {
    "score": 2.5,
    "image_count": 8,
    "screenshots_in_readme": true,
    "screenshots_in_docs": true,
    "quality": "good"
  },
  "ui_documentation": {
    "score": 2.5,
    "has_ui_doc": true,
    "readme_has_ui_section": true,
    "comprehensiveness": "good",
    "has_usage_instructions": true
  },
  "design_files": {
    "score": 1.0,
    "has_mockups": true,
    "has_design_doc": false,
    "design_file_count": 3
  },
  "usability": {
    "score": 1.0,
    "has_user_guide": true,
    "has_accessibility_doc": false,
    "has_error_handling_doc": false
  },
  "recommendations": [
    "Add design decisions documentation",
    "Include accessibility guidelines",
    "Document error messages and validation"
  ]
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** only check root directory for screenshots
✅ **DO** search entire repository (docs/, assets/, images/, screenshots/)

❌ **DON'T** count image files without checking if they're referenced
✅ **DO** verify screenshots are embedded in documentation

❌ **DON'T** assume all PNG files are screenshots
✅ **DO** check if images show actual UI (not logos or icons)

❌ **DON'T** miss UI documentation in README
✅ **DO** read README for interface/usage sections

❌ **DON'T** give full points for a single screenshot
✅ **DO** require multiple screenshots showing different features

❌ **DON'T** ignore design files in non-standard locations
✅ **DO** search for .figma, .sketch, mockup images everywhere

---

## Example Execution

```bash
# Step 1: Run helper script
python .claude/skills/6-ui-ux/find_ui_docs.py /path/to/repo

# Output shows:
# - 8 image files found
# - README includes screenshots
# - 2 UI documentation files
# - User guide present

# Step 2: Find images manually
find /path/to/repo -name "*.png" -o -name "*.jpg" | head -20

# Step 3: Check README for embedded screenshots
Read /path/to/repo/README.md

# Step 4: Read UI documentation
Read /path/to/repo/docs/UI.md
Read /path/to/repo/docs/USER_GUIDE.md

# Step 5: Find design files
find /path/to/repo -name "*mockup*" -o -name "*wireframe*"

# Step 6: Calculate score
# Screenshots: 2.5 (multiple screenshots in README)
# UI docs: 2.5 (has UI.md and README section)
# Design files: 1.0 (has mockups)
# Usability: 1.0 (has user guide)
# Total: 7.0/10

# Step 7: Generate JSON output
```

---

## Tips for Accurate Assessment

1. **Read README first** - Most UI docs are embedded there
2. **Verify screenshots show UI** - Not just logos or diagrams
3. **Check if images are referenced** - Files alone don't count
4. **Look for design artifacts** - Mockups, wireframes, Figma files
5. **Check multiple locations** - docs/, design/, assets/, screenshots/
6. **Verify completeness** - One screenshot isn't enough
7. **Give partial credit** - Good README UI section deserves points

**Visual Documentation Matters:** Screenshots help users understand what they're building!

**Success = Finding all UI/UX documentation and assessing it fairly!**

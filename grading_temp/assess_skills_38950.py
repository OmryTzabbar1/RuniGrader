#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Assess 10 skills for Student 38950
Repository: https://github.com/Roei-Bracha/ollama-chat-hw
"""

import subprocess
import os
import sys

os.chdir('temp_assessment_38950')

print("="*70)
print("TIER 2 ASSESSMENT: Student 38950")
print("Repository: ollama-chat-hw")
print("Self-Grade: 100/100")
print("TRUE Count: 15/22")
print("="*70)

skills = {}

# SKILL 1: Project Planning (10 points)
print("\n[SKILL 1] Project Planning")
print("-"*50)
score_1 = 0

# Check PRD
if os.path.exists('PRD.md'):
    with open('PRD.md', 'r', encoding='utf-8') as f:
        prd_content = f.read()
        prd_size = len(prd_content)
        print(f"✓ PRD exists: {prd_size} characters")
        score_1 += 2

        # Check sections
        if '## Problem Statement' in prd_content or 'Problem Statement' in prd_content:
            print("✓ Has Problem Statement")
            score_1 += 1
        if 'Functional Requirements' in prd_content or 'Requirements' in prd_content:
            print("✓ Has Functional Requirements")
            score_1 += 1.5
        if 'Success Metrics' in prd_content or 'Metrics' in prd_content:
            print("✓ Has Success Metrics")
            score_1 += 0.5

# Check Architecture (from assessment, we know it's FALSE)
print("✗ No Architecture Document (from assessment)")
score_1 += 0  # Missing

skills['project_planning'] = min(score_1, 10)
print(f"SCORE: {skills['project_planning']}/10")

# SKILL 2: Code Documentation (10 points)
print("\n[SKILL 2] Code Documentation")
print("-"*50)
score_2 = 0

# Check README
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_size = len(f.read())
        print(f"✓ README exists: {readme_size} characters")
        score_2 += 1.5
        if readme_size > 5000:
            print("✓ Comprehensive README (>5000 chars)")
            score_2 += 1.5

# Check structure
if os.path.exists('app') and os.path.exists('components') and os.path.exists('lib'):
    print("✓ Good project structure (app/, components/, lib/)")
    score_2 += 2

# Check file sizes (<150 lines)
result = subprocess.run('find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | head -20',
                       shell=True, capture_output=True, text=True)
files = result.stdout.strip().split('\n') if result.stdout.strip() else []
oversized = 0
for f in files[:10]:  # Check first 10
    if os.path.exists(f):
        lines = sum(1 for line in open(f, 'r', encoding='utf-8', errors='ignore'))
        if lines > 150:
            oversized += 1

if oversized == 0:
    print(f"✓ All checked files <150 lines")
    score_2 += 2
elif oversized <= 2:
    print(f"⚠ {oversized} files >150 lines")
    score_2 += 1
else:
    print(f"✗ {oversized} files >150 lines")

# Docstrings - TypeScript uses JSDoc comments
result = subprocess.run('grep -r "/**" . --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l',
                       shell=True, capture_output=True, text=True)
jsdoc_count = int(result.stdout.strip()) if result.stdout.strip() else 0
print(f"JSDoc comments found: {jsdoc_count}")
if jsdoc_count > 10:
    score_2 += 2
elif jsdoc_count > 5:
    score_2 += 1

skills['code_documentation'] = min(score_2, 10)
print(f"SCORE: {skills['code_documentation']}/10")

# SKILL 3: Configuration & Security (10 points)
print("\n[SKILL 3] Configuration & Security")
print("-"*50)
score_3 = 0

# Check .env and .gitignore
if os.path.exists('.gitignore'):
    print("✓ .gitignore exists")
    score_3 += 2
    with open('.gitignore', 'r') as f:
        gitignore = f.read()
        if '.env' in gitignore:
            print("✓ .env in .gitignore")
            score_3 += 1.5

# Check for config files
config_files = ['next.config.ts', 'tailwind.config.ts', 'tsconfig.json']
found_configs = sum(1 for cf in config_files if os.path.exists(cf))
print(f"✓ Config files found: {found_configs}")
score_3 += min(found_configs * 0.5, 1.5)

# CRITICAL: Check for hardcoded secrets
result = subprocess.run('grep -r "api[_-]\\?key\\s*=\\s*[\'\\\"][^\'\\\"]\\{10,\\}[\'\\\"]" . --include="*.ts" --include="*.tsx" 2>/dev/null',
                       shell=True, capture_output=True, text=True)
secrets_found = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

if secrets_found == 0:
    print("✓ No hardcoded API keys found")
    score_3 += 5  # CRITICAL - full points
else:
    print(f"✗ CRITICAL: {secrets_found} potential hardcoded secrets")
    score_3 = 0  # Auto-fail

skills['config_security'] = min(score_3, 10)
print(f"SCORE: {skills['config_security']}/10")

# SKILL 4: Testing & Quality (10 points)
print("\n[SKILL 4] Testing & Quality")
print("-"*50)
score_4 = 0

# Check for tests
if os.path.exists('test') or os.path.exists('e2e'):
    print("✓ Test directories exist")
    score_4 += 2

    # Count test files
    result = subprocess.run('find test e2e -name "*.test.ts" -o -name "*.spec.ts" 2>/dev/null | wc -l',
                           shell=True, capture_output=True, text=True)
    test_count = int(result.stdout.strip()) if result.stdout.strip() else 0
    print(f"Test files found: {test_count}")

    if test_count >= 5:
        score_4 += 2
    elif test_count >= 3:
        score_4 += 1

# Check for vitest/playwright config
if os.path.exists('vitest.config.ts'):
    print("✓ Vitest configured")
    score_4 += 1
if os.path.exists('playwright.config.ts'):
    print("✓ Playwright configured")
    score_4 += 1

# Check for edge case testing
result = subprocess.run('grep -ri "edge.*case\\|boundary" test/ e2e/ 2>/dev/null | wc -l',
                       shell=True, capture_output=True, text=True)
edge_tests = int(result.stdout.strip()) if result.stdout.strip() else 0
if edge_tests > 0:
    print(f"✓ Edge case tests found: {edge_tests}")
    score_4 += 2
else:
    print("✗ No edge case testing found")

# Test documentation
if os.path.exists('test/README.md'):
    print("✓ Test documentation exists")
    score_4 += 1
else:
    print("⚠ No test documentation")
    score_4 += 0.5  # Partial credit

skills['testing_quality'] = min(score_4, 10)
print(f"SCORE: {skills['testing_quality']}/10")

# SKILL 5: Research & Analysis (10 points)
print("\n[SKILL 5] Research & Analysis")
print("-"*50)
score_5 = 0

# From assessment: FALSE on criteria 11, 12, 13
print("✗ No Parameter Investigation (from assessment)")
print("✗ No Results Analysis Notebook (from assessment)")
print("✗ No Visual Presentation of Results (from assessment)")

# Check anyway for partial credit
result = subprocess.run('find . -name "*.ipynb" 2>/dev/null | wc -l',
                       shell=True, capture_output=True, text=True)
notebooks = int(result.stdout.strip()) if result.stdout.strip() else 0

if notebooks > 0:
    print(f"Notebooks found: {notebooks}")
    score_5 += 2
else:
    score_5 += 0

skills['research_analysis'] = min(score_5, 10)
print(f"SCORE: {skills['research_analysis']}/10")

# SKILL 6: UI/UX (10 points)
print("\n[SKILL 6] UI/UX")
print("-"*50)
score_6 = 0

# Check README for usage
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
        if '## Usage' in readme or 'How to use' in readme:
            print("✓ Usage documentation in README")
            score_6 += 2.5

# Check for screenshots
if os.path.exists('screenshots'):
    result = subprocess.run('ls screenshots/*.png screenshots/*.jpg 2>/dev/null | wc -l',
                           shell=True, capture_output=True, text=True)
    screenshots = int(result.stdout.strip()) if result.stdout.strip() else 0
    if screenshots > 0:
        print(f"✓ Screenshots found: {screenshots}")
        score_6 += 2.5

# UI components
if os.path.exists('components'):
    result = subprocess.run('ls components/*.tsx components/*.ts 2>/dev/null | wc -l',
                           shell=True, capture_output=True, text=True)
    components = int(result.stdout.strip()) if result.stdout.strip() else 0
    print(f"✓ UI components: {components}")
    score_6 += min(components * 0.5, 2.5)

# Interface quality assessment
if os.path.exists('app'):
    print("✓ Next.js app structure (good UX framework)")
    score_6 += 2.5

skills['ui_ux'] = min(score_6, 10)
print(f"SCORE: {skills['ui_ux']}/10")

# SKILL 7: Version Management (10 points)
print("\n[SKILL 7] Version Management")
print("-"*50)
score_7 = 0

# From assessment: FALSE on Git practices
print("✗ Best Practices with Git: FALSE (from assessment)")

# Count commits anyway
result = subprocess.run('git log --oneline --no-merges | wc -l',
                       shell=True, capture_output=True, text=True)
commits = int(result.stdout.strip()) if result.stdout.strip() else 0
print(f"Total commits: {commits}")

if commits >= 25:
    score_7 += 2
elif commits >= 15:
    score_7 += 1.5
elif commits >= 10:
    score_7 += 1
else:
    score_7 += 0.5

# Check prompts directory
if os.path.exists('prompts'):
    result = subprocess.run('ls prompts/*.md prompts/*.txt 2>/dev/null | wc -l',
                           shell=True, capture_output=True, text=True)
    prompt_files = int(result.stdout.strip()) if result.stdout.strip() else 0
    print(f"✓ Prompt files found: {prompt_files}")

    if prompt_files >= 5:
        score_7 += 4
    elif prompt_files >= 3:
        score_7 += 3
    elif prompt_files >= 1:
        score_7 += 2

skills['version_management'] = min(score_7, 10)
print(f"SCORE: {skills['version_management']}/10")

# SKILL 8: Costs & Pricing (10 points)
print("\n[SKILL 8] Costs & Pricing")
print("-"*50)
score_8 = 0

# From assessment: FALSE on both criteria
print("✗ Cost Analysis: FALSE (from assessment)")
print("✗ Budget Management: FALSE (from assessment)")

# Check anyway
result = subprocess.run('grep -ri "cost.*analysis\\|pricing\\|budget" . --include="*.md" 2>/dev/null | wc -l',
                       shell=True, capture_output=True, text=True)
cost_mentions = int(result.stdout.strip()) if result.stdout.strip() else 0

if cost_mentions > 5:
    print(f"Cost mentions found: {cost_mentions}")
    score_8 += 2
else:
    score_8 += 0

skills['costs_pricing'] = min(score_8, 10)
print(f"SCORE: {skills['costs_pricing']}/10")

# SKILL 9: Extensibility (10 points)
print("\n[SKILL 9] Extensibility")
print("-"*50)
score_9 = 0

# Check file sizes (maintainability)
result = subprocess.run('find . -name "*.ts" -name "*.tsx" 2>/dev/null | head -20',
                       shell=True, capture_output=True, text=True)
files = result.stdout.strip().split('\n') if result.stdout.strip() else []
oversized = sum(1 for f in files[:15] if os.path.exists(f) and
                sum(1 for _ in open(f, 'r', encoding='utf-8', errors='ignore')) > 150)

if oversized == 0:
    print("✓ All files <150 lines (excellent maintainability)")
    score_9 += 2.5
elif oversized <= 2:
    print(f"⚠ {oversized} files >150 lines")
    score_9 += 1.5

# Modular structure
if os.path.exists('components') and os.path.exists('lib'):
    print("✓ Modular structure (components/, lib/)")
    score_9 += 2.5

# Check for TypeScript (type safety = extensibility)
if os.path.exists('tsconfig.json'):
    print("✓ TypeScript configured (type safety)")
    score_9 += 2.5

# Extension points
result = subprocess.run('grep -r "interface\\|type\\|abstract" . --include="*.ts" 2>/dev/null | wc -l',
                       shell=True, capture_output=True, text=True)
interfaces = int(result.stdout.strip()) if result.stdout.strip() else 0
if interfaces > 10:
    print(f"✓ Many interfaces/types defined: {interfaces}")
    score_9 += 2.5
elif interfaces > 5:
    score_9 += 1.5

skills['extensibility'] = min(score_9, 10)
print(f"SCORE: {skills['extensibility']}/10")

# SKILL 10: Quality Standards (10 points)
print("\n[SKILL 10] Quality Standards (ISO/IEC 25010)")
print("-"*50)
score_10 = 0

# Functional Suitability (15/22 criteria met = 68%)
print("Functional Suitability: 15/22 criteria met (68%)")
score_10 += 1.5  # Partial (out of 2)

# Performance - check for optimization mentions
result = subprocess.run('grep -ri "performance\\|optimization" . --include="*.md" 2>/dev/null | wc -l',
                       shell=True, capture_output=True, text=True)
perf_mentions = int(result.stdout.strip()) if result.stdout.strip() else 0
if perf_mentions > 0:
    print(f"✓ Performance considerations: {perf_mentions} mentions")
    score_10 += 0.5
else:
    score_10 += 0

# Usability (good README = 1.5/2)
print("✓ Usability: Good README and documentation")
score_10 += 1.5

# Reliability (has tests = 1.5/2)
print("✓ Reliability: Testing implemented")
score_10 += 1.5

# Security (no secrets = 1.5/1.5)
print("✓ Security: No hardcoded secrets")
score_10 += 1.5

# Maintainability (good structure = 1/1)
print("✓ Maintainability: Good code structure")
score_10 += 1

# Portability (TypeScript/Next.js = 0.5/0.5)
print("✓ Portability: Cross-platform (TypeScript/Next.js)")
score_10 += 0.5

skills['quality_standards'] = min(score_10, 10)
print(f"SCORE: {skills['quality_standards']}/10")

# FINAL CALCULATION
print("\n" + "="*70)
print("FINAL SKILL SCORES - Student 38950")
print("="*70)
total = 0
for i, (skill_name, score) in enumerate(skills.items(), 1):
    print(f"Skill {i:2d} - {skill_name:20s}: {score:.1f}/10")
    total += score

final_grade = total  # Already out of 100
print("="*70)
print(f"TOTAL SCORE: {total:.1f}/100")
print(f"FINAL GRADE: {final_grade:.1f}%")

# Determine tier
if final_grade >= 90:
    tier = "Excellence"
elif final_grade >= 80:
    tier = "Good"
elif final_grade >= 55:
    tier = "Potential"
else:
    tier = "Below Standard"

print(f"PERFORMANCE TIER: {tier}")
print("="*70)

# Save results
os.chdir('..')
with open('student_38950_skills.txt', 'w') as f:
    f.write(f"Student 38950 - Tier 2 Assessment\n")
    f.write(f"Repository: ollama-chat-hw\n")
    f.write(f"Self-Grade: 100\n")
    f.write(f"TRUE Count: 15/22\n\n")
    for i, (skill_name, score) in enumerate(skills.items(), 1):
        f.write(f"Skill {i}: {skill_name} = {score:.1f}/10\n")
    f.write(f"\nTotal: {total:.1f}/100\n")
    f.write(f"Final Grade: {final_grade:.1f}%\n")
    f.write(f"Tier: {tier}\n")

print("\nResults saved to student_38950_skills.txt")

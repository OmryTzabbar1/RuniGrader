#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tier 2 Skills Orchestrator
Runs all 10 assessment skills for a student repository
"""

import os
import sys
import subprocess
import json

def run_bash_command(cmd, cwd=None):
    """Run a bash command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def assess_skill_1_project_planning(repo_path):
    """Skill 1: Project Planning (10 points)"""
    score = 0.0
    details = {}

    # Check PRD
    prd_paths = ['PRD.md', 'docs/PRD.md', 'docs/prd.md']
    prd_found = False
    for prd in prd_paths:
        if os.path.exists(os.path.join(repo_path, prd)):
            prd_found = True
            score += 2
            details['prd'] = True
            # Check sections
            with open(os.path.join(repo_path, prd), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'Problem Statement' in content or 'problem statement' in content:
                    score += 1
                    details['problem_statement'] = True
                if 'Functional Requirements' in content or 'Requirements' in content:
                    score += 1.5
                    details['functional_requirements'] = True
                if 'Success Metrics' in content or 'Metrics' in content:
                    score += 0.5
                    details['success_metrics'] = True
            break

    # Check Architecture
    arch_paths = ['ARCHITECTURE.md', 'docs/architecture.md', 'docs/ARCHITECTURE.md']
    for arch in arch_paths:
        if os.path.exists(os.path.join(repo_path, arch)):
            score += 5
            details['architecture'] = True
            break

    return min(score, 10.0), details

def assess_skill_2_code_documentation(repo_path):
    """Skill 2: Code Documentation (10 points)"""
    score = 0.0
    details = {}

    # Check README
    if os.path.exists(os.path.join(repo_path, 'README.md')):
        readme_size = os.path.getsize(os.path.join(repo_path, 'README.md'))
        score += 1.5
        details['readme'] = True
        if readme_size > 5000:
            score += 1.5
            details['readme_comprehensive'] = True

    # Check structure
    has_src = os.path.exists(os.path.join(repo_path, 'src'))
    has_tests = os.path.exists(os.path.join(repo_path, 'tests')) or os.path.exists(os.path.join(repo_path, 'test'))
    if has_src:
        score += 1.5
        details['src_directory'] = True
    if has_tests:
        score += 0.5
        details['test_directory'] = True

    # Check file sizes (sample check)
    output, _ = run_bash_command(
        'find . -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" 2>/dev/null | head -10',
        cwd=repo_path
    )
    files = output.split('\n') if output else []
    oversized = 0
    for f in files:
        if f:
            full_path = os.path.join(repo_path, f.lstrip('./'))
            if os.path.exists(full_path):
                try:
                    lines = sum(1 for _ in open(full_path, 'r', encoding='utf-8', errors='ignore'))
                    if lines > 150:
                        oversized += 1
                except:
                    pass

    if oversized == 0:
        score += 2
        details['file_sizes_good'] = True
    elif oversized <= 2:
        score += 1
        details['file_sizes_ok'] = True

    # Docstrings check
    output, _ = run_bash_command(
        'grep -r "\"\"\"\\|///" . --include="*.py" --include="*.ts" --include="*.js" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        doc_count = int(output) if output else 0
        if doc_count > 20:
            score += 2
        elif doc_count > 10:
            score += 1
        details['docstrings_count'] = doc_count
    except:
        pass

    return min(score, 10.0), details

def assess_skill_3_config_security(repo_path):
    """Skill 3: Configuration & Security (10 points)"""
    score = 0.0
    details = {}

    # Check .gitignore
    if os.path.exists(os.path.join(repo_path, '.gitignore')):
        score += 2
        details['gitignore'] = True
        with open(os.path.join(repo_path, '.gitignore'), 'r') as f:
            if '.env' in f.read():
                score += 1.5
                details['env_in_gitignore'] = True

    # Check config files
    config_files = ['config.yaml', 'config.json', 'package.json', 'tsconfig.json', 'angular.json']
    found_configs = sum(1 for cf in config_files if os.path.exists(os.path.join(repo_path, cf)))
    score += min(found_configs * 0.5, 1.5)
    details['config_files'] = found_configs

    # CRITICAL: Check for hardcoded secrets
    output, _ = run_bash_command(
        'grep -r "api[_-]\\?key\\s*=\\s*[\'\\\"][^\'\\\"]\\{10,\\}[\'\\\"]" . --include="*.py" --include="*.ts" --include="*.js" 2>/dev/null',
        cwd=repo_path
    )
    if output:
        score = 0  # Auto-fail if secrets found
        details['secrets_found'] = True
    else:
        score += 5  # CRITICAL - full points for security
        details['no_secrets'] = True

    return min(score, 10.0), details

def assess_skill_4_testing_quality(repo_path):
    """Skill 4: Testing & Quality (10 points)"""
    score = 0.0
    details = {}

    # Check test directories
    test_dirs = ['tests', 'test', 'e2e', '__tests__']
    has_test_dir = any(os.path.exists(os.path.join(repo_path, td)) for td in test_dirs)
    if has_test_dir:
        score += 2
        details['test_directory'] = True

    # Count test files
    output, _ = run_bash_command(
        'find . -name "*.test.py" -o -name "*.spec.ts" -o -name "*.test.js" -o -name "*_test.py" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        test_count = int(output) if output else 0
        if test_count >= 5:
            score += 2
        elif test_count >= 3:
            score += 1
        details['test_files'] = test_count
    except:
        pass

    # Check test config
    test_configs = ['pytest.ini', 'vitest.config.ts', 'jest.config.js', 'karma.conf.js']
    if any(os.path.exists(os.path.join(repo_path, tc)) for tc in test_configs):
        score += 1
        details['test_config'] = True

    # Check for edge case testing
    output, _ = run_bash_command(
        'grep -ri "edge.*case\\|boundary" tests/ test/ e2e/ 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        edge_tests = int(output) if output else 0
        if edge_tests > 0:
            score += 2
            details['edge_case_tests'] = edge_tests
    except:
        pass

    # Test documentation
    if os.path.exists(os.path.join(repo_path, 'TESTING.md')) or os.path.exists(os.path.join(repo_path, 'tests/README.md')):
        score += 1
        details['test_docs'] = True
    else:
        score += 0.5

    return min(score, 10.0), details

def assess_skill_5_research_analysis(repo_path):
    """Skill 5: Research & Analysis (10 points)"""
    score = 0.0
    details = {}

    # Check for notebooks
    output, _ = run_bash_command(
        'find . -name "*.ipynb" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        notebooks = int(output) if output else 0
        if notebooks > 0:
            score += 3
            details['notebooks'] = notebooks
    except:
        pass

    # Check for analysis docs
    analysis_files = ['ANALYSIS.md', 'docs/ANALYSIS.md', 'RESEARCH.md', 'docs/RESEARCH.md']
    if any(os.path.exists(os.path.join(repo_path, af)) for af in analysis_files):
        score += 2
        details['analysis_docs'] = True

    # Check for visualizations
    output, _ = run_bash_command(
        'find . -name "*.png" -o -name "*.jpg" -o -name "*.svg" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        images = int(output) if output else 0
        if images >= 3:
            score += 3
        elif images >= 1:
            score += 1.5
        details['visualizations'] = images
    except:
        pass

    # Check for LaTeX formulas
    output, _ = run_bash_command(
        'grep -r "\\$\\$\\|\\\\begin{equation}" . --include="*.md" --include="*.ipynb" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        formulas = int(output) if output else 0
        if formulas > 0:
            score += 2
            details['formulas'] = formulas
    except:
        pass

    return min(score, 10.0), details

def assess_skill_6_ui_ux(repo_path):
    """Skill 6: UI/UX (10 points)"""
    score = 0.0
    details = {}

    # Check interface documentation
    if os.path.exists(os.path.join(repo_path, 'README.md')):
        with open(os.path.join(repo_path, 'README.md'), 'r', encoding='utf-8', errors='ignore') as f:
            readme = f.read()
            if '## Usage' in readme or 'How to use' in readme:
                score += 2.5
                details['usage_docs'] = True

    # Check for screenshots
    screenshot_dirs = ['screenshots', 'images', 'docs/images']
    for sd in screenshot_dirs:
        if os.path.exists(os.path.join(repo_path, sd)):
            output, _ = run_bash_command(
                f'ls {sd}/*.png {sd}/*.jpg 2>/dev/null | wc -l',
                cwd=repo_path
            )
            try:
                screenshots = int(output) if output else 0
                if screenshots > 0:
                    score += 2.5
                    details['screenshots'] = screenshots
                    break
            except:
                pass

    # Check UI framework
    frameworks = {
        'angular.json': 'Angular',
        'next.config.ts': 'Next.js',
        'vue.config.js': 'Vue',
        'svelte.config.js': 'Svelte'
    }
    for config, framework in frameworks.items():
        if os.path.exists(os.path.join(repo_path, config)):
            score += 2.5
            details['ui_framework'] = framework
            break

    # UI components
    ui_dirs = ['components', 'src/components', 'app/components']
    for ud in ui_dirs:
        if os.path.exists(os.path.join(repo_path, ud)):
            output, _ = run_bash_command(
                f'ls {ud}/*.tsx {ud}/*.ts {ud}/*.vue {ud}/*.svelte 2>/dev/null | wc -l',
                cwd=repo_path
            )
            try:
                components = int(output) if output else 0
                if components > 0:
                    score += min(components * 0.5, 2.5)
                    details['components'] = components
                    break
            except:
                pass

    return min(score, 10.0), details

def assess_skill_7_version_management(repo_path):
    """Skill 7: Version Management (10 points)"""
    score = 0.0
    details = {}

    # Count commits
    output, _ = run_bash_command('git log --oneline --no-merges | wc -l', cwd=repo_path)
    try:
        commits = int(output) if output else 0
        if commits >= 25:
            score += 2
        elif commits >= 15:
            score += 1.5
        elif commits >= 10:
            score += 1
        else:
            score += 0.5
        details['commits'] = commits
    except:
        pass

    # Check conventional commits
    output, _ = run_bash_command(
        'git log --pretty=format:"%s" --no-merges | grep -E "^(feat|fix|docs|test|refactor)" | wc -l',
        cwd=repo_path
    )
    try:
        conventional = int(output) if output else 0
        if commits > 0:
            ratio = conventional / commits
            if ratio >= 0.7:
                score += 2
            elif ratio >= 0.5:
                score += 1
            details['conventional_commits'] = conventional
            details['conventional_ratio'] = ratio
    except:
        pass

    # Check prompts directory
    prompt_dirs = ['prompts', '.prompts', 'docs/prompts']
    for pd in prompt_dirs:
        if os.path.exists(os.path.join(repo_path, pd)):
            output, _ = run_bash_command(
                f'ls {pd}/*.md {pd}/*.txt 2>/dev/null | wc -l',
                cwd=repo_path
            )
            try:
                prompt_files = int(output) if output else 0
                if prompt_files >= 5:
                    score += 4
                elif prompt_files >= 3:
                    score += 3
                elif prompt_files >= 1:
                    score += 2
                details['prompt_files'] = prompt_files
                break
            except:
                pass

    return min(score, 10.0), details

def assess_skill_8_costs_pricing(repo_path):
    """Skill 8: Costs & Pricing (10 points)"""
    score = 0.0
    details = {}

    # Check for cost analysis docs
    cost_files = ['COSTS.md', 'docs/COSTS.md', 'COST_ANALYSIS.md', 'docs/COST_ANALYSIS.md']
    for cf in cost_files:
        if os.path.exists(os.path.join(repo_path, cf)):
            score += 2.5
            details['cost_docs'] = True
            break

    # Check for cost mentions
    output, _ = run_bash_command(
        'grep -ri "cost.*analysis\\|pricing\\|budget" . --include="*.md" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        cost_mentions = int(output) if output else 0
        if cost_mentions > 5:
            score += 2.5
            details['cost_mentions'] = cost_mentions
    except:
        pass

    # Check for cost tracking code
    output, _ = run_bash_command(
        'grep -r "cost\\|budget\\|CostTracker" . --include="*.py" --include="*.ts" --include="*.js" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        cost_code = int(output) if output else 0
        if cost_code > 10:
            score += 2.5
        elif cost_code > 5:
            score += 1.5
        details['cost_code'] = cost_code
    except:
        pass

    return min(score, 10.0), details

def assess_skill_9_extensibility(repo_path):
    """Skill 9: Extensibility (10 points)"""
    score = 0.0
    details = {}

    # Check file sizes
    output, _ = run_bash_command(
        'find . -name "*.py" -o -name "*.ts" -o -name "*.js" 2>/dev/null | head -20',
        cwd=repo_path
    )
    files = output.split('\n') if output else []
    oversized = 0
    for f in files:
        if f:
            full_path = os.path.join(repo_path, f.lstrip('./'))
            if os.path.exists(full_path):
                try:
                    lines = sum(1 for _ in open(full_path, 'r', encoding='utf-8', errors='ignore'))
                    if lines > 150:
                        oversized += 1
                except:
                    pass

    if oversized == 0:
        score += 2.5
        details['file_sizes_excellent'] = True
    elif oversized <= 2:
        score += 1.5
        details['file_sizes_good'] = True

    # Check modularity
    modular_dirs = ['src', 'lib', 'components', 'services', 'models']
    found_modules = sum(1 for md in modular_dirs if os.path.exists(os.path.join(repo_path, md)))
    if found_modules >= 3:
        score += 2.5
    elif found_modules >= 2:
        score += 1.5
    details['modular_dirs'] = found_modules

    # Check for interfaces/abstractions
    output, _ = run_bash_command(
        'grep -r "interface\\|abstract\\|ABC" . --include="*.py" --include="*.ts" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        interfaces = int(output) if output else 0
        if interfaces > 10:
            score += 2.5
        elif interfaces > 5:
            score += 1.5
        elif interfaces > 0:
            score += 1
        details['interfaces'] = interfaces
    except:
        pass

    # Type safety
    type_configs = ['tsconfig.json', 'mypy.ini', 'pyproject.toml']
    if any(os.path.exists(os.path.join(repo_path, tc)) for tc in type_configs):
        score += 2.5
        details['type_safety'] = True

    return min(score, 10.0), details

def assess_skill_10_quality_standards(repo_path, true_count):
    """Skill 10: Quality Standards (10 points)"""
    score = 0.0
    details = {}

    # Functional Suitability (based on TRUE count)
    functional_pct = (true_count / 22) * 100
    if functional_pct >= 80:
        score += 2
    elif functional_pct >= 70:
        score += 1.5
    elif functional_pct >= 60:
        score += 1
    else:
        score += 0.5
    details['functional_suitability'] = functional_pct

    # Performance (check for performance docs)
    output, _ = run_bash_command(
        'grep -ri "performance\\|optimization" . --include="*.md" 2>/dev/null | wc -l',
        cwd=repo_path
    )
    try:
        perf_mentions = int(output) if output else 0
        if perf_mentions > 0:
            score += 0.5
        details['performance_mentions'] = perf_mentions
    except:
        pass

    # Usability (README quality)
    if os.path.exists(os.path.join(repo_path, 'README.md')):
        readme_size = os.path.getsize(os.path.join(repo_path, 'README.md'))
        if readme_size > 10000:
            score += 2
        elif readme_size > 5000:
            score += 1.5
        else:
            score += 1
        details['usability_readme'] = readme_size

    # Reliability (testing)
    has_tests = os.path.exists(os.path.join(repo_path, 'tests')) or os.path.exists(os.path.join(repo_path, 'test'))
    if has_tests:
        score += 2
        details['reliability_tests'] = True
    else:
        score += 0.5

    # Security (from Skill 3)
    output, _ = run_bash_command(
        'grep -r "api[_-]\\?key\\s*=\\s*[\'\\\"][^\'\\\"]\\{10,\\}[\'\\\"]" . --include="*.py" --include="*.ts" 2>/dev/null',
        cwd=repo_path
    )
    if not output:
        score += 1.5
        details['security_pass'] = True
    else:
        details['security_fail'] = True

    # Maintainability (structure)
    has_structure = os.path.exists(os.path.join(repo_path, 'src'))
    if has_structure:
        score += 1
        details['maintainability'] = True

    # Portability (cross-platform configs)
    if os.path.exists(os.path.join(repo_path, 'package.json')) or os.path.exists(os.path.join(repo_path, 'requirements.txt')):
        score += 0.5
        details['portability'] = True

    return min(score, 10.0), details

def run_tier2_assessment(repo_path, student_id, self_grade, true_count):
    """Run all 10 skills and return assessment"""

    print(f"\n{'='*70}")
    print(f"TIER 2 ORCHESTRATOR: Student {student_id}")
    print(f"Repository: {os.path.basename(repo_path)}")
    print(f"Self-Grade: {self_grade}/100")
    print(f"TRUE Count: {true_count}/22")
    print(f"{'='*70}\n")

    skills = {}
    skill_details = {}

    # Run each skill
    print("[1/10] Assessing Project Planning...")
    skills['project_planning'], skill_details['project_planning'] = assess_skill_1_project_planning(repo_path)
    print(f"        Score: {skills['project_planning']}/10")

    print("[2/10] Assessing Code Documentation...")
    skills['code_documentation'], skill_details['code_documentation'] = assess_skill_2_code_documentation(repo_path)
    print(f"        Score: {skills['code_documentation']}/10")

    print("[3/10] Assessing Configuration & Security...")
    skills['config_security'], skill_details['config_security'] = assess_skill_3_config_security(repo_path)
    print(f"        Score: {skills['config_security']}/10")

    print("[4/10] Assessing Testing & Quality...")
    skills['testing_quality'], skill_details['testing_quality'] = assess_skill_4_testing_quality(repo_path)
    print(f"        Score: {skills['testing_quality']}/10")

    print("[5/10] Assessing Research & Analysis...")
    skills['research_analysis'], skill_details['research_analysis'] = assess_skill_5_research_analysis(repo_path)
    print(f"        Score: {skills['research_analysis']}/10")

    print("[6/10] Assessing UI/UX...")
    skills['ui_ux'], skill_details['ui_ux'] = assess_skill_6_ui_ux(repo_path)
    print(f"        Score: {skills['ui_ux']}/10")

    print("[7/10] Assessing Version Management...")
    skills['version_management'], skill_details['version_management'] = assess_skill_7_version_management(repo_path)
    print(f"        Score: {skills['version_management']}/10")

    print("[8/10] Assessing Costs & Pricing...")
    skills['costs_pricing'], skill_details['costs_pricing'] = assess_skill_8_costs_pricing(repo_path)
    print(f"        Score: {skills['costs_pricing']}/10")

    print("[9/10] Assessing Extensibility...")
    skills['extensibility'], skill_details['extensibility'] = assess_skill_9_extensibility(repo_path)
    print(f"        Score: {skills['extensibility']}/10")

    print("[10/10] Assessing Quality Standards...")
    skills['quality_standards'], skill_details['quality_standards'] = assess_skill_10_quality_standards(repo_path, true_count)
    print(f"        Score: {skills['quality_standards']}/10")

    # Calculate totals
    total_score = sum(skills.values())
    final_grade = total_score

    # Determine tier
    if final_grade >= 90:
        tier = "Excellence"
    elif final_grade >= 80:
        tier = "Good"
    elif final_grade >= 55:
        tier = "Potential"
    else:
        tier = "Below Standard"

    # Self-assessment accuracy
    difference = self_grade - final_grade
    if abs(difference) < 3:
        accuracy = "Accurate"
    elif difference < 0:
        accuracy = f"Humble (underestimated by {abs(difference):.1f} points)"
    else:
        accuracy = f"Overconfident (overestimated by {difference:.1f} points)"

    # Print summary
    print(f"\n{'='*70}")
    print("FINAL RESULTS:")
    print(f"{'='*70}")
    for i, (skill_name, score) in enumerate(skills.items(), 1):
        print(f"Skill {i:2d} - {skill_name:20s}: {score:.1f}/10")
    print(f"{'='*70}")
    print(f"TOTAL SCORE: {total_score:.1f}/100")
    print(f"FINAL GRADE: {final_grade:.1f}%")
    print(f"PERFORMANCE TIER: {tier}")
    print(f"SELF-ASSESSMENT: {accuracy}")
    print(f"{'='*70}\n")

    return {
        'student_id': student_id,
        'self_grade': self_grade,
        'true_count': true_count,
        'repository': os.path.basename(repo_path),
        'skills': skills,
        'skill_details': skill_details,
        'total_score': total_score,
        'final_grade': final_grade,
        'performance_tier': tier,
        'self_assessment_accuracy': accuracy
    }

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python orchestrator.py <repo_path> <student_id> <self_grade> [true_count]")
        print("Example: python orchestrator.py temp_assessment_38950 38950 100 15")
        sys.exit(1)

    repo_path = sys.argv[1]
    student_id = sys.argv[2]
    self_grade = int(sys.argv[3])
    true_count = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    result = run_tier2_assessment(repo_path, student_id, self_grade, true_count)

    # Save results
    output_file = f"tier2_assessment_{student_id}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Results saved to: {output_file}")

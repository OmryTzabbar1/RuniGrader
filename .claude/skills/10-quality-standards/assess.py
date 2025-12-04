#!/usr/bin/env python3
"""
Skill 10: Quality Standards Assessment
Scores based on linting, CI/CD, style guides, and code quality tools.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_quality_standards(repo_path):
    """
    Assess quality standards and tooling.

    Scoring:
    - Linting configuration: 2.0 points
    - CI/CD pipeline: 3.0 points
    - Code style guide: 3.0 points
    - Pre-commit hooks: 1.0 point
    - Quality tools configured: 1.0 point

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "find_quality_tools.py"
    result = subprocess.run(
        [sys.executable, str(finder_script), repo_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": f"Finder script failed: {result.stderr}",
            "skill": "quality_standards"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "quality_standards"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for linting configuration (2 points)
    linting_config = data.get("linting_config", [])
    linting_score = 0.0

    if len(linting_config) > 0:
        linting_score = 2.0
        score += 2.0
        notes.append(f"Linting configured: {', '.join(linting_config[:3])}")
    else:
        recommendations.append("Configure linting tools (pylint, eslint, etc.) (+2.0 points)")

    # Check for CI/CD pipeline (3 points)
    ci_files = data.get("ci_pipeline", [])
    ci_score = 0.0

    if len(ci_files) > 0:
        ci_score = 3.0
        score += 3.0
        notes.append(f"CI/CD pipeline configured: {', '.join(ci_files[:3])}")
    else:
        recommendations.append("Set up CI/CD pipeline (GitHub Actions, GitLab CI, etc.) (+3.0 points)")

    # Check for code style guide (3 points)
    style_guides = data.get("style_guides", [])
    readme_has_quality = data.get("readme_has_quality", False)
    style_score = 0.0

    if len(style_guides) > 0:
        # Check if it's only README mention
        if any('README.md' in sg for sg in style_guides) and len(style_guides) == 1:
            # Partial credit for README quality mentions
            style_score = 1.5
            score += 1.5
            notes.append(f"Code quality information in README: {style_guides[0]}")
            recommendations.append("Create dedicated style guide or CONTRIBUTING.md (+1.5 points)")
        else:
            # Full credit for dedicated style guide
            style_score = 3.0
            score += 3.0
            notes.append(f"Code style guide found: {', '.join(style_guides[:3])}")
    else:
        recommendations.append("Create code style guide or CONTRIBUTING.md (+3.0 points)")

    # Check for pre-commit hooks (1 point)
    has_pre_commit = data.get("has_pre_commit_hooks", False)
    pre_commit_score = 0.0

    if has_pre_commit:
        pre_commit_score = 1.0
        score += 1.0
        notes.append("Pre-commit hooks configured")
    else:
        recommendations.append("Set up pre-commit hooks for automatic quality checks (+1.0 point)")

    # Quality tools configured (1 point)
    # This is a bonus for having multiple quality tools
    quality_tools_score = 0.0
    quality_score = data.get("summary", {}).get("quality_score", 0)

    if quality_score >= 3:
        quality_tools_score = 1.0
        score += 1.0
        notes.append("Multiple quality tools configured")
    elif quality_score >= 2:
        recommendations.append("Add more quality tools (+1.0 point)")
    else:
        recommendations.append("Configure quality assurance tools (+1.0 point)")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "linting_score": linting_score,
        "ci_score": ci_score,
        "style_score": style_score,
        "pre_commit_score": pre_commit_score,
        "quality_tools_score": quality_tools_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "quality_standards"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_quality_standards(repo_path)
    print(json.dumps(result, indent=2))

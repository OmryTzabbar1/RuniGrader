#!/usr/bin/env python3
"""
Skill 2: Code Documentation Assessment
Scores based on README, docstrings, and code structure documentation.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_code_documentation(repo_path):
    """
    Assess code documentation quality.

    Scoring:
    - README.md >1KB: 3.0 points
    - Installation instructions: 1.0 point
    - Usage examples: 1.0 point
    - Code structure documented: 2.0 points
    - Python docstrings (>50% of files): 3.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "find_documentation.py"
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
            "skill": "code_documentation"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "code_documentation"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for README >1KB (3 points)
    readme_files = data.get("readme_files", [])
    readme_score = 0.0

    if readme_files:
        main_readme = readme_files[0]
        if main_readme["size_bytes"] >= 1024:
            readme_score += 3.0
            notes.append(f"README.md found ({main_readme['size_bytes']} bytes)")
        else:
            readme_score += 1.0
            notes.append(f"README.md found but too small ({main_readme['size_bytes']} bytes)")
            recommendations.append(f"Expand README.md to at least 1KB (+{3.0 - readme_score:.1f} points)")

        # Check for installation instructions (1 point)
        if main_readme.get("has_installation"):
            score += 1.0
            notes.append("Installation instructions found in README")
        else:
            recommendations.append("Add installation instructions to README.md (+1.0 point)")

        # Check for usage examples (1 point)
        if main_readme.get("has_usage"):
            score += 1.0
            notes.append("Usage examples found in README")
        else:
            recommendations.append("Add usage examples to README.md (+1.0 point)")
    else:
        recommendations.append("Create README.md with installation and usage instructions (+5.0 points)")

    score += readme_score

    # Check for code structure documentation (2 points)
    structure_docs = data.get("code_structure", {})
    structure_score = 0.0

    if structure_docs.get("docs_directory"):
        structure_score += 1.0
        notes.append("docs/ directory found")

    if structure_docs.get("has_package_init"):
        structure_score += 1.0
        notes.append("Package __init__.py with documentation found")

    if readme_files and readme_files[0].get("has_architecture"):
        structure_score = 2.0  # Full points if README has architecture section
        notes.append("Code structure documented in README")

    if structure_score == 0:
        recommendations.append("Document code structure in README or create docs/ directory (+2.0 points)")
    elif structure_score < 2:
        recommendations.append(f"Improve code structure documentation (+{2.0 - structure_score:.1f} points)")

    score += structure_score

    # Check for Python docstrings >50% of files (3 points)
    docstring_stats = data.get("docstring_statistics", {})
    python_stats = docstring_stats.get("python", {})

    docstring_score = 0.0
    if python_stats.get("files", 0) > 0:
        coverage = python_stats["with_docstrings"] / python_stats["files"]
        if coverage > 0.5:
            docstring_score = 3.0
            notes.append(f"Python docstring coverage: {coverage*100:.0f}%")
        elif coverage > 0.25:
            docstring_score = 1.5
            notes.append(f"Python docstring coverage: {coverage*100:.0f}% (needs improvement)")
            recommendations.append("Increase docstring coverage to >50% of files (+1.5 points)")
        else:
            notes.append(f"Python docstring coverage: {coverage*100:.0f}% (too low)")
            recommendations.append("Add docstrings to Python functions and classes (+3.0 points)")
    else:
        # Check if there are any Python files
        if python_stats.get("files") == 0:
            # Not a Python project, give neutral score
            docstring_score = 3.0
            notes.append("No Python files found (N/A for docstrings)")

    score += docstring_score

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "readme_score": readme_score,
        "structure_score": structure_score,
        "docstring_score": docstring_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "code_documentation"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_code_documentation(repo_path)
    print(json.dumps(result, indent=2))

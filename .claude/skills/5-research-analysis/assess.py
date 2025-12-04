#!/usr/bin/env python3
"""
Skill 5: Research & Analysis Assessment
Scores based on Jupyter notebooks, data analysis, and visualizations.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_research_analysis(repo_path):
    """
    Assess research and analysis capabilities.

    Scoring:
    - Research documentation exists (notebooks, PDFs, markdown): 4.0 points
    - Multiple research artifacts (>2): 2.0 points
    - Has visualizations/plots: 2.0 points
    - Analysis documentation: 2.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "find_research.py"
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
            "skill": "research_analysis"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "research_analysis"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for research documentation existence (4 points)
    notebooks = data.get("notebooks", [])
    research_docs = data.get("research_documents", [])
    all_research = notebooks + research_docs
    total_research_count = len(all_research)
    notebooks_exist_score = 0.0

    if total_research_count > 0:
        notebooks_exist_score = 4.0
        score += 4.0
        if len(notebooks) > 0 and len(research_docs) > 0:
            notes.append(f"Found {len(notebooks)} Jupyter notebook(s) and {len(research_docs)} research document(s)")
        elif len(notebooks) > 0:
            notes.append(f"Found {len(notebooks)} Jupyter notebook(s)")
        else:
            notes.append(f"Found {len(research_docs)} research document(s)")
    else:
        recommendations.append("Create research documentation (Jupyter notebooks, research PDFs, or analysis markdown) (+4.0 points)")

    # Check for multiple research artifacts >2 (2 points)
    multiple_notebooks_score = 0.0

    if total_research_count > 2:
        multiple_notebooks_score = 2.0
        score += 2.0
        notes.append(f"Multiple research artifacts for comprehensive analysis")
    elif total_research_count > 0:
        recommendations.append(f"Create more research documentation (currently {total_research_count}, need >2) (+2.0 points)")
    else:
        recommendations.append("Create at least 3 research documents for different analyses (+2.0 points)")

    # Check for visualizations/plots (2 points)
    notebooks_with_plots = sum(1 for n in notebooks if n.get("has_plots"))
    visualizations_score = 0.0

    # Give credit if notebooks have plots OR if research PDFs exist (assume they have visualizations)
    if notebooks_with_plots > 0 or len(research_docs) > 0:
        visualizations_score = 2.0
        score += 2.0
        if notebooks_with_plots > 0:
            notes.append(f"Visualizations found in {notebooks_with_plots} notebook(s)")
        else:
            notes.append(f"Research documentation includes visualizations")
    elif total_research_count > 0:
        recommendations.append("Add visualizations using matplotlib/seaborn/plotly or include plots in research docs (+2.0 points)")
    else:
        recommendations.append("Create research documentation with data visualizations (+2.0 points)")

    # Check for analysis documentation (2 points)
    # Look for analysis libraries usage OR existence of research docs
    notebooks_with_analysis = sum(1 for n in notebooks if n.get("has_analysis"))
    documentation_score = 0.0

    if notebooks_with_analysis > 0 or len(research_docs) > 0:
        documentation_score = 2.0
        score += 2.0
        if notebooks_with_analysis > 0:
            notes.append(f"Analysis libraries (pandas/numpy/scipy) used in {notebooks_with_analysis} notebook(s)")
        else:
            notes.append(f"Research documentation provides analysis methodology")
    elif total_research_count > 0:
        recommendations.append("Add data analysis using pandas/numpy/scipy or document methodology (+2.0 points)")
    else:
        recommendations.append("Document analysis methodology in research documentation (+2.0 points)")

    # Additional context
    data_files = data.get("data_files", [])
    if len(data_files) > 0:
        notes.append(f"Found {len(data_files)} data file(s) for analysis")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "notebooks_exist_score": notebooks_exist_score,
        "multiple_notebooks_score": multiple_notebooks_score,
        "visualizations_score": visualizations_score,
        "documentation_score": documentation_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "research_analysis"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_research_analysis(repo_path)
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
"""
Skill 1: Project Planning Assessment
Scores based on PRD and ARCHITECTURE documentation.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_project_planning(repo_path):
    """
    Assess project planning documentation.

    Scoring:
    - PRD.md exists: 2.0 points
      - Has Problem Statement: +1.0 point
      - Has Functional Requirements: +1.5 points
      - Has Success Metrics: +0.5 points
    - ARCHITECTURE.md exists: 5.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "find_planning_docs.py"
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
            "skill": "project_planning"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "project_planning"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for PRD (max 4 points)
    prd_found = data["summary"]["has_prd"]
    prd_score = 0.0

    if prd_found:
        prd_score += 2.0
        notes.append("PRD.md found")

        # Check for sections in PRD documents
        best_prd = None
        best_completeness = 0

        for prd in data["prd_documents"]:
            if prd["completeness"] > best_completeness:
                best_completeness = prd["completeness"]
                best_prd = prd

        if best_prd:
            found_sections = best_prd["found_sections"]

            # Problem Statement
            if any("Problem Statement" in s for s in found_sections):
                prd_score += 1.0
                notes.append("Problem Statement found in PRD")
            else:
                recommendations.append("Add Problem Statement section to PRD.md (+1.0 point)")

            # Functional Requirements
            if any("Functional Requirements" in s for s in found_sections):
                prd_score += 1.5
                notes.append("Functional Requirements found in PRD")
            else:
                recommendations.append("Add Functional Requirements section to PRD.md (+1.5 points)")

            # Success Metrics
            if any("Success Metrics" in s for s in found_sections):
                prd_score += 0.5
                notes.append("Success Metrics found in PRD")
            else:
                recommendations.append("Add Success Metrics section to PRD.md (+0.5 points)")
    else:
        recommendations.append("Create PRD.md with Problem Statement, Functional Requirements, and Success Metrics (+4.0 points)")

    score += prd_score

    # Check for ARCHITECTURE.md or architecture in README (5 points with partial credit)
    arch_found = data["summary"]["has_architecture"]
    arch_score = 0.0

    if arch_found:
        arch_score = 5.0
        score += 5.0
        notes.append("ARCHITECTURE.md found")
    else:
        # Check for any architectural documentation in README or other files
        readme_has_arch = False
        readme_arch_doc = None
        for doc in data.get("architecture_documents", []):
            if "readme" in doc.get("path", "").lower():
                readme_has_arch = True
                readme_arch_doc = doc
                break

        if readme_has_arch and readme_arch_doc:
            # Check quality of README architecture section
            completeness = readme_arch_doc.get("completeness", 0)
            if completeness >= 60:  # Good architecture documentation in README
                arch_score = 5.0
                score += 5.0
                notes.append("Architecture documented in README")
            elif completeness >= 30:  # Partial architecture in README
                arch_score = 3.0
                score += 3.0
                notes.append("Partial architecture information found in README")
                recommendations.append("Expand architecture section in README or create ARCHITECTURE.md (+2.0 points)")
            else:
                arch_score = 2.0
                score += 2.0
                notes.append("Some architectural information found in README")
                recommendations.append("Expand architecture documentation (+3.0 points)")
        elif prd_found:
            # Give partial credit for having some structure documentation
            arch_score = 2.0
            score += 2.0
            notes.append("Some architectural information found in documentation")
            recommendations.append("Document architecture in README or ARCHITECTURE.md (+3.0 points)")
        else:
            recommendations.append("Document architecture in README or ARCHITECTURE.md (+5.0 points)")

    return {
        "score": score,
        "max_score": 10.0,
        "prd_found": prd_found,
        "prd_score": prd_score,
        "architecture_found": arch_found,
        "architecture_score": arch_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "project_planning"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_project_planning(repo_path)
    print(json.dumps(result, indent=2))

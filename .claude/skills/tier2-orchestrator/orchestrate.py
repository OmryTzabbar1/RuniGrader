#!/usr/bin/env python3
"""
Tier 2 Orchestrator - Parallel Skill Invocation
Properly invokes all 10 individual skills in parallel for true orchestration.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Add skills directory to path
SKILLS_DIR = Path(__file__).parent.parent

def invoke_skill(skill_name, repo_path):
    """
    Invoke a single skill and return its JSON result.

    Args:
        skill_name: Name of skill folder (e.g., "1-project-planning")
        repo_path: Path to repository to assess

    Returns:
        dict: Skill assessment result with 'score' and 'details'
    """
    skill_path = SKILLS_DIR / skill_name

    # Look for assess.py first, then fall back to any .py file
    assess_script = skill_path / "assess.py"

    if assess_script.exists():
        script = assess_script
    else:
        # Check if skill has a Python script
        script_files = list(skill_path.glob("*.py"))
        if not script_files:
            return {"score": 0, "error": f"No Python script found in {skill_name}"}
        script = script_files[0]

    # Convert repo_path to absolute path
    abs_repo_path = str(Path(repo_path).resolve())

    try:
        # Run the skill's Python script
        result = subprocess.run(
            [sys.executable, str(script), abs_repo_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(skill_path)
        )

        if result.returncode != 0:
            return {
                "score": 0,
                "error": f"Skill execution failed: {result.stderr}",
                "skill": skill_name
            }

        # Try to parse JSON output
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            # If not JSON, assume the output is just the score
            try:
                score = float(result.stdout.strip())
                return {"score": score, "skill": skill_name}
            except ValueError:
                return {
                    "score": 0,
                    "error": f"Could not parse output: {result.stdout[:100]}",
                    "skill": skill_name
                }

    except subprocess.TimeoutExpired:
        return {"score": 0, "error": "Skill execution timed out", "skill": skill_name}
    except Exception as e:
        return {"score": 0, "error": str(e), "skill": skill_name}

def orchestrate_tier2_assessment(repo_path, student_id, assignment="Assignment 1"):
    """
    Run all 10 skills in parallel and aggregate results.

    Args:
        repo_path: Path to student repository
        student_id: Student identifier
        assignment: Assignment name

    Returns:
        dict: Complete assessment with all skill scores
    """
    skills = [
        "1-project-planning",
        "2-code-documentation",
        "3-config-security",
        "4-testing-quality",
        "5-research-analysis",
        "6-ui-ux",
        "7-version-management",
        "8-costs-pricing",
        "9-extensibility",
        "10-quality-standards"
    ]

    skill_display_names = {
        "1-project-planning": "project_planning",
        "2-code-documentation": "code_documentation",
        "3-config-security": "config_security",
        "4-testing-quality": "testing_quality",
        "5-research-analysis": "research_analysis",
        "6-ui-ux": "ui_ux",
        "7-version-management": "version_management",
        "8-costs-pricing": "costs_pricing",
        "9-extensibility": "extensibility",
        "10-quality-standards": "quality_standards"
    }

    print(f"[Orchestrator] Assessing {student_id} using 10 skills in parallel...")

    results = {}
    errors = []

    # Execute all skills in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_skill = {
            executor.submit(invoke_skill, skill, repo_path): skill
            for skill in skills
        }

        for future in as_completed(future_to_skill):
            skill = future_to_skill[future]
            skill_display = skill_display_names[skill]

            try:
                result = future.result()
                score = result.get("score", 0)

                if "error" in result:
                    errors.append(f"{skill}: {result['error']}")
                    print(f"  [!] {skill}: {score}/10 (with errors)")
                else:
                    print(f"  [OK] {skill}: {score}/10")

                results[skill_display] = result

            except Exception as e:
                errors.append(f"{skill}: {str(e)}")
                results[skill_display] = {"score": 0, "error": str(e)}
                print(f"  [FAIL] {skill}: 0/10 (exception)")

    # Calculate total score
    total_score = sum(r.get("score", 0) for r in results.values())

    # Determine performance tier
    if total_score >= 90:
        tier = "Excellence"
    elif total_score >= 80:
        tier = "Good"
    elif total_score >= 55:
        tier = "Potential"
    else:
        tier = "Below Standard"

    # Build final assessment
    assessment = {
        "student_id": student_id,
        "assignment": assignment,
        "repository_name": os.path.basename(repo_path),
        "repository_path": repo_path,
        "assessment_date": datetime.now().strftime("%Y-%m-%d"),
        "orchestration_method": "parallel_skill_invocation",
        "orchestrator_version": "3.0.0",
        "skills": {name: r.get("score", 0) for name, r in results.items()},
        "skill_details": results,
        "total_score": total_score,
        "final_grade": total_score,
        "performance_tier": tier,
        "tier_description": get_tier_description(tier),
        "errors": errors if errors else None
    }

    # Generate recommendations
    assessment["recommended_actions"] = generate_recommendations(results)

    # Add overall assessment
    assessment["overall_assessment"] = generate_overall_assessment(results, total_score, tier)

    return assessment

def get_tier_description(tier):
    """Get point range for performance tier."""
    tiers = {
        "Excellence": "90-100 points",
        "Good": "80-89 points",
        "Potential": "55-79 points",
        "Below Standard": "0-54 points"
    }
    return tiers.get(tier, "Unknown")

def generate_recommendations(results):
    """Generate recommended actions based on skill scores."""
    immediate = []
    high_priority = []

    for skill_name, result in results.items():
        score = result.get("score", 0)
        display_name = skill_name.replace('_', ' ').title()

        if score == 0:
            immediate.append(f"Address {display_name} (0/10 points)")
        elif score < 5:
            high_priority.append(f"Improve {display_name} ({score}/10 points)")

    if not immediate:
        immediate = ["All critical areas addressed - focus on optimization"]

    if not high_priority:
        high_priority = ["Maintain current standards across all skills"]

    return {
        "immediate": immediate,
        "high_priority": high_priority
    }

def generate_overall_assessment(results, total_score, tier):
    """Generate overall assessment summary."""
    strengths = []
    weaknesses = []

    for skill_name, result in results.items():
        score = result.get("score", 0)
        display_name = skill_name.replace('_', ' ').title()

        if score >= 8:
            strengths.append(f"{display_name} ({score}/10)")
        elif score < 5:
            weaknesses.append(f"{display_name} ({score}/10)")

    return {
        "summary": f"Assessment completed with {total_score}/100 points ({tier} tier)",
        "strengths": strengths if strengths else ["No skills with excellent scores (8+/10)"],
        "weaknesses": weaknesses if weaknesses else ["No critical weaknesses (<5/10)"],
        "parallel_execution": True,
        "skills_assessed": len(results)
    }

def clone_repo_if_needed(repo_path_or_student_folder):
    """
    Try to clone repository if path doesn't exist.
    If the path looks like a student folder, try to clone the repo.
    Returns: (actual_repo_path, was_cloned)
    """
    path_obj = Path(repo_path_or_student_folder)

    # If path exists, return it as-is
    if path_obj.exists():
        return str(path_obj), False

    # Check if parent is a student folder (contains submission_info.xlsx)
    parent = path_obj.parent
    if (parent / "submission_info.xlsx").exists():
        # This looks like a repo path inside a student folder that doesn't exist
        # Try to clone from the student folder
        student_folder = parent
    elif "Participant_" in str(path_obj) and (path_obj / "submission_info.xlsx").exists():
        # This is the student folder itself
        student_folder = path_obj
    else:
        return None, False

    # Try to clone the repo
    clone_script = Path(__file__).parent / "clone_repo.py"
    try:
        result = subprocess.run(
            [sys.executable, str(clone_script), str(student_folder)],
            capture_output=True,
            text=True,
            timeout=180
        )

        if result.returncode == 0:
            # Extract REPO_PATH from output
            for line in result.stdout.split('\n'):
                if line.startswith('REPO_PATH:'):
                    cloned_path = line.replace('REPO_PATH:', '').strip()
                    return cloned_path, True

        return None, False
    except Exception as e:
        print(f"[Warning] Failed to clone repository: {str(e)}")
        return None, False

def main():
    """Main entry point for orchestrator."""
    if len(sys.argv) < 3:
        print("Usage: python orchestrate.py <repo_path_or_student_folder> <student_id> [assignment_name]")
        print("\nThe orchestrator will automatically clone the repository from submission_info.xlsx if it doesn't exist.")
        sys.exit(1)

    repo_path = sys.argv[1]
    student_id = sys.argv[2]
    assignment = sys.argv[3] if len(sys.argv) > 3 else "Assignment 1"

    # Try to clone repo if it doesn't exist
    if not os.path.exists(repo_path):
        print(f"[Orchestrator] Repository not found, attempting to clone from submission_info.xlsx...")
        cloned_path, was_cloned = clone_repo_if_needed(repo_path)

        if cloned_path:
            repo_path = cloned_path
            if was_cloned:
                print(f"[Orchestrator] Successfully cloned repository to: {repo_path}")
            else:
                print(f"[Orchestrator] Using existing repository at: {repo_path}")
        else:
            print(f"Error: Repository path does not exist and could not be cloned: {repo_path}")
            sys.exit(1)

    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    # Run orchestration
    assessment = orchestrate_tier2_assessment(repo_path, student_id, assignment)

    # Save JSON - use assignment name to determine output directory
    assignment_num = assignment.lower().replace("assignment", "").replace(" ", "").strip()
    if assignment_num.isdigit():
        output_dir = Path(f"assessments_tier2_assignment{assignment_num}")
    else:
        output_dir = Path("assessments_tier2_assignment1")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"tier2_assessment_{student_id}.json"
    with open(output_file, 'w') as f:
        json.dump(assessment, f, indent=2)

    print(f"\n[Orchestrator] Assessment complete!")
    print(f"  Total Score: {assessment['total_score']}/100")
    print(f"  Tier: {assessment['performance_tier']}")
    print(f"  Output: {output_file}")

    if assessment.get("errors"):
        print(f"\n[Warnings] {len(assessment['errors'])} errors occurred:")
        for error in assessment['errors'][:5]:
            print(f"  - {error}")

    # Generate PDFs
    print(f"\n[Orchestrator] Generating PDF reports...")

    # Determine student folder path (always use parent folder for PDFs)
    repo_path_obj = Path(repo_path)
    # Check if we're in a repo subdirectory - look for "Participant_" in parent path
    if "Participant_" in str(repo_path_obj.parent):
        # We're inside a repo folder, go up to submission folder
        student_folder = repo_path_obj.parent
    else:
        # Already at submission level or higher
        student_folder = repo_path_obj

    # 1. Generate detailed breakdown PDF (grader-pdf skill)
    grader_pdf_script = SKILLS_DIR / "grader-pdf" / "generate_detailed_breakdown.py"
    detailed_pdf_path = student_folder / f"Detailed_Grade_Breakdown_{student_id}.pdf"

    try:
        result = subprocess.run(
            [sys.executable, str(grader_pdf_script), str(output_file), str(detailed_pdf_path), assignment],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"  [OK] Detailed breakdown PDF: {detailed_pdf_path}")
        else:
            print(f"  [!] Failed to generate detailed breakdown PDF: {result.stderr[:200]}")
    except Exception as e:
        print(f"  [!] Error generating detailed breakdown PDF: {str(e)}")

    # 2. Generate grade report PDF (grade-report-generator skill)
    grade_report_script = SKILLS_DIR / "grade-report-generator" / "generate_student_report.py"

    # Extract strengths and improvements from assessment
    strengths = "|".join(assessment['overall_assessment']['strengths'])
    weaknesses = "|".join(assessment['overall_assessment']['weaknesses'])

    # Determine team name from repository
    repo_name = assessment.get('repository_name', 'Unknown')

    try:
        result = subprocess.run(
            [
                sys.executable, str(grade_report_script),
                "--student-id", student_id,
                "--team", repo_name,
                "--grade", str(int(assessment['total_score'])),
                "--repository", repo_name,
                "--output-dir", str(student_folder),
                "--strengths", strengths,
                "--improvements", weaknesses,
                "--assignment", assignment
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            grade_report_path = student_folder / f"Grade_Report_{student_id}.pdf"
            print(f"  [OK] Grade report PDF: {grade_report_path}")
        else:
            print(f"  [!] Failed to generate grade report PDF: {result.stderr[:200]}")
    except Exception as e:
        print(f"  [!] Error generating grade report PDF: {str(e)}")

    print(f"\n[Orchestrator] Complete! Assessment and PDFs generated for student {student_id}")

if __name__ == "__main__":
    main()

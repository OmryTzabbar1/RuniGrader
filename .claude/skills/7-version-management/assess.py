#!/usr/bin/env python3
"""
Skill 7: Version Management Assessment
Scores based on git history, commit quality, and prompt documentation.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_version_management(repo_path):
    """
    Assess version management practices.

    Scoring:
    - Git commits >10: 2.0 points
    - Meaningful commit messages: 2.0 points
    - PROMPT_BOOK.md exists: 5.0 points
    - Branching strategy: 1.0 point

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "analyze_git_history.py"
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
            "skill": "version_management"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "version_management"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for git commits >10 (2 points)
    commits = data.get("commits", {})
    total_commits = commits.get("total_commits", 0)
    commits_score = 0.0

    if total_commits > 10:
        commits_score = 2.0
        score += 2.0
        notes.append(f"Good commit history: {total_commits} commits")
    elif total_commits > 5:
        commits_score = 1.0
        score += 1.0
        notes.append(f"Moderate commit history: {total_commits} commits")
        recommendations.append("Make more commits to document project evolution (+1.0 point)")
    elif total_commits > 0:
        notes.append(f"Limited commit history: {total_commits} commits")
        recommendations.append("Make more commits (target: >10) (+2.0 points)")
    else:
        recommendations.append("Initialize git repository and make regular commits (+2.0 points)")

    # Check for meaningful commit messages (2 points)
    meaningful_percent = commits.get("meaningful_percent", 0)
    meaningful_score = 0.0

    if total_commits > 0:
        if meaningful_percent >= 60:
            meaningful_score = 2.0
            score += 2.0
            notes.append(f"Excellent commit message quality ({meaningful_percent:.0f}% meaningful)")
        elif meaningful_percent >= 40:
            meaningful_score = 1.0
            score += 1.0
            notes.append(f"Good commit message quality ({meaningful_percent:.0f}% meaningful)")
            recommendations.append("Improve commit message quality (+1.0 point)")
        else:
            notes.append(f"Poor commit message quality ({meaningful_percent:.0f}% meaningful)")
            recommendations.append("Write more descriptive commit messages (+2.0 points)")
    else:
        recommendations.append("Write meaningful commit messages explaining changes (+2.0 points)")

    # Check for PROMPT_BOOK.md or any prompt documentation (5 points)
    prompt_docs = data.get("prompt_documentation")
    prompt_book_score = 0.0

    if prompt_docs:
        prompt_book_score = 5.0
        score += 5.0
        notes.append(f"Prompt documentation found: {prompt_docs}")
    else:
        recommendations.append("Create PROMPT_BOOK.md to document AI interactions (+5.0 points)")

    # Check for branching strategy (1 point)
    branching = data.get("branching", {})
    has_branches = branching.get("has_branches", False)
    branching_score = 0.0

    if has_branches:
        branch_count = branching.get("branch_count", 0)
        branching_score = 1.0
        score += 1.0
        notes.append(f"Branching strategy in use ({branch_count} branches)")
    else:
        recommendations.append("Use branches for feature development (+1.0 point)")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "commits_score": commits_score,
        "meaningful_score": meaningful_score,
        "prompt_book_score": prompt_book_score,
        "branching_score": branching_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "version_management"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_version_management(repo_path)
    print(json.dumps(result, indent=2))

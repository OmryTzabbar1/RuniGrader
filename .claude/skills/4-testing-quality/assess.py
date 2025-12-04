#!/usr/bin/env python3
"""
Skill 4: Testing & Quality Assessment
Scores based on test files, test coverage, and testing infrastructure.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_testing_quality(repo_path):
    """
    Assess testing and quality practices.

    Scoring:
    - Test files exist: 3.0 points
    - Multiple test files (≥1): 2.0 points (sufficient to have one test folder/file)
    - Test framework configured: 2.0 points
    - Test functions/classes (>10): 3.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "analyze_tests.py"
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
            "skill": "testing_quality"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "testing_quality"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for test files existence (3 points)
    test_files = data.get("test_files", [])
    test_file_count = len(test_files)
    test_exists_score = 0.0

    if test_file_count > 0:
        test_exists_score = 3.0
        score += 3.0
        notes.append(f"Found {test_file_count} test file(s)")
    else:
        recommendations.append("Create test files for your code (+3.0 points)")

    # Check for test files (≥1 is sufficient) (2 points)
    multiple_tests_score = 0.0

    if test_file_count >= 1:
        multiple_tests_score = 2.0
        score += 2.0
        if test_file_count > 3:
            notes.append(f"Excellent test coverage with {test_file_count} test files")
        else:
            notes.append(f"Good test coverage with {test_file_count} test file(s)")
    else:
        recommendations.append("Create test files for your code (+2.0 points)")

    # Check for test framework configuration (2 points)
    coverage_config = data.get("coverage_config", [])
    framework_score = 0.0

    if len(coverage_config) > 0:
        framework_score = 2.0
        score += 2.0
        notes.append(f"Test framework configured: {', '.join(coverage_config)}")
    else:
        recommendations.append("Configure a test framework (pytest, jest, etc.) (+2.0 points)")

    # Check for test functions/classes >10 (3 points)
    test_quality = data.get("test_quality", {})
    total_tests = test_quality.get("total_tests", 0)
    test_count_score = 0.0

    if total_tests > 10:
        test_count_score = 3.0
        score += 3.0
        notes.append(f"Excellent test count: {total_tests} test functions")
    elif total_tests > 5:
        test_count_score = 1.5
        score += 1.5
        notes.append(f"Good test count: {total_tests} test functions")
        recommendations.append("Write more test functions to reach >10 (+1.5 points)")
    elif total_tests > 0:
        test_count_score = 0.5
        score += 0.5
        notes.append(f"Limited test count: {total_tests} test functions")
        recommendations.append("Write more test functions to reach >10 (+2.5 points)")
    else:
        recommendations.append("Write test functions (target: >10) (+3.0 points)")

    # Additional notes
    if test_quality.get("quality") == "excellent":
        notes.append("Overall test quality: Excellent")
    elif test_quality.get("quality") == "good":
        notes.append("Overall test quality: Good")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "test_exists_score": test_exists_score,
        "multiple_tests_score": multiple_tests_score,
        "framework_score": framework_score,
        "test_count_score": test_count_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "testing_quality"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_testing_quality(repo_path)
    print(json.dumps(result, indent=2))

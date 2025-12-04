#!/usr/bin/env python3
"""
Skill 6: UI/UX Assessment
Scores based on screenshots, images, and UI documentation.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_ui_ux(repo_path):
    """
    Assess UI/UX documentation and materials.

    Scoring:
    - Screenshots/images (1+): 3.0 points
    - Screenshots/images (5+): 3.0 points additional
    - UI documentation in README: 2.0 points
    - User guide exists: 2.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "find_ui_docs.py"
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
            "skill": "ui_ux"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "ui_ux"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for screenshots/images (1+) = 3 points
    images = data.get("images", [])
    image_count = len(images)
    basic_images_score = 0.0

    if image_count >= 1:
        basic_images_score = 3.0
        score += 3.0
        notes.append(f"Found {image_count} image(s)/screenshot(s)")
    else:
        recommendations.append("Add screenshots of your application (+3.0 points)")

    # Check for multiple screenshots/images (5+) = additional 3 points
    multiple_images_score = 0.0

    if image_count >= 5:
        multiple_images_score = 3.0
        score += 3.0
        notes.append("Excellent visual documentation with 5+ images")
    elif image_count >= 1:
        recommendations.append(f"Add more screenshots (currently {image_count}, need 5+) (+3.0 points)")
    else:
        recommendations.append("Add at least 5 screenshots showing different features (+3.0 points)")

    # Check for UI documentation in README (2 points)
    readme_has_screenshots = data.get("readme_has_screenshots", False)
    readme_ui_score = 0.0

    if readme_has_screenshots:
        readme_ui_score = 2.0
        score += 2.0
        notes.append("README includes UI screenshots/documentation")
    else:
        recommendations.append("Add UI screenshots to README.md (+2.0 points)")

    # Check for user guide (2 points)
    ui_docs = data.get("ui_documentation", [])
    user_guide_score = 0.0

    if len(ui_docs) > 0:
        user_guide_score = 2.0
        score += 2.0
        notes.append(f"UI documentation found: {', '.join(ui_docs[:3])}")
    else:
        recommendations.append("Create user guide or UI documentation (+2.0 points)")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "basic_images_score": basic_images_score,
        "multiple_images_score": multiple_images_score,
        "readme_ui_score": readme_ui_score,
        "user_guide_score": user_guide_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "ui_ux"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_ui_ux(repo_path)
    print(json.dumps(result, indent=2))

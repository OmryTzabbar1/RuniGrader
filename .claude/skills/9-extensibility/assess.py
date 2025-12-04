#!/usr/bin/env python3
"""
Skill 9: Extensibility Assessment
Scores based on plugin systems, modular structure, and APIs.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_extensibility(repo_path):
    """
    Assess code extensibility and modularity.

    Scoring:
    - Plugin/extension system: 3.0 points
    - Modular structure (3+ key dirs): 3.0 points
    - Interfaces/APIs: 2.0 points
    - Extension documentation: 2.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "analyze_extensibility.py"
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
            "skill": "extensibility"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "extensibility"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Check for plugin/extension system (3 points)
    plugin_dirs = data.get("plugin_directories", [])
    ext_docs = data.get("extensibility_docs", [])
    doc_quality = data.get("doc_quality", {})
    plugin_score = 0.0

    if len(plugin_dirs) > 0:
        # Actual plugin directories exist
        plugin_score = 3.0
        score += 3.0
        notes.append(f"Plugin/extension system found: {', '.join(plugin_dirs[:3])}")
    elif len(ext_docs) > 0 and doc_quality.get("has_extension_points", False):
        # No actual plugin dirs, but documented how to create plugins
        plugin_score = 1.0
        score += 1.0
        notes.append("Plugin architecture documented but not implemented")
        recommendations.append("Implement actual plugin/extension system (+2.0 points)")
    else:
        recommendations.append("Create plugin/extension system for modularity (+3.0 points)")

    # Check for modular structure (3 points)
    # We'll check if the code is modular based on avg lines per file
    modularity = data.get("modularity", {})
    is_modular = modularity.get("is_modular", False)
    avg_lines = modularity.get("avg_lines_per_file", 0)
    modular_score = 0.0

    if is_modular and avg_lines < 150:
        modular_score = 3.0
        score += 3.0
        notes.append(f"Excellent modular structure (avg {avg_lines:.0f} lines/file)")
    elif is_modular:
        modular_score = 2.0
        score += 2.0
        notes.append(f"Good modular structure (avg {avg_lines:.0f} lines/file)")
        recommendations.append("Further refactor to smaller modules (+1.0 point)")
    elif avg_lines < 300:
        modular_score = 1.0
        score += 1.0
        notes.append(f"Somewhat modular (avg {avg_lines:.0f} lines/file)")
        recommendations.append("Break down large files into smaller modules (+2.0 points)")
    else:
        notes.append(f"Large files detected (avg {avg_lines:.0f} lines/file)")
        recommendations.append("Refactor into modular structure with smaller files (+3.0 points)")

    # Check for interfaces/APIs (2 points)
    interface_files = data.get("interface_files", [])
    interface_count = len(interface_files)
    interface_score = 0.0

    if interface_count >= 3:
        interface_score = 2.0
        score += 2.0
        notes.append(f"Well-defined interfaces/APIs ({interface_count} interface files)")
    elif interface_count > 0:
        interface_score = 1.0
        score += 1.0
        notes.append(f"Some interfaces defined ({interface_count} interface files)")
        recommendations.append("Define more interfaces for better extensibility (+1.0 point)")
    else:
        recommendations.append("Define interfaces/APIs for extensibility (+2.0 points)")

    # Check for extension documentation (2 points)
    # Check for actual extensibility documentation files
    extension_docs_score = 0.0
    ext_docs = data.get("extensibility_docs", [])
    doc_quality = data.get("doc_quality", {})
    has_extension_points = doc_quality.get("has_extension_points", False)
    has_examples = doc_quality.get("has_examples", False)
    word_count = doc_quality.get("word_count", 0)

    if len(ext_docs) > 0:
        # Found extensibility documentation file(s)
        if has_extension_points and has_examples and word_count > 500:
            # Comprehensive documentation with examples
            extension_docs_score = 2.0
            score += 2.0
            notes.append(f"Comprehensive extensibility documentation: {', '.join(ext_docs[:2])}")
        elif has_extension_points or has_examples or word_count > 200:
            # Good documentation
            extension_docs_score = 1.5
            score += 1.5
            notes.append(f"Good extensibility documentation: {', '.join(ext_docs[:2])}")
            recommendations.append("Expand extensibility docs with more examples (+0.5 points)")
        else:
            # Basic documentation
            extension_docs_score = 1.0
            score += 1.0
            notes.append(f"Basic extensibility documentation found: {', '.join(ext_docs[:2])}")
            recommendations.append("Add extension points and code examples (+1.0 point)")
    elif len(plugin_dirs) > 0 and interface_count > 0:
        # Infer documentation from code structure
        extension_docs_score = 1.0
        score += 1.0
        notes.append("Extension architecture appears documented in code")
        recommendations.append("Create dedicated extensibility guide (+1.0 point)")
    elif len(plugin_dirs) > 0 or interface_count > 0:
        extension_docs_score = 0.5
        score += 0.5
        notes.append("Partial extension support in code")
        recommendations.append("Document how to extend/customize the system (+1.5 points)")
    else:
        recommendations.append("Document extension/customization approach (+2.0 points)")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "plugin_score": plugin_score,
        "modular_score": modular_score,
        "interface_score": interface_score,
        "extension_docs_score": extension_docs_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "extensibility"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_extensibility(repo_path)
    print(json.dumps(result, indent=2))

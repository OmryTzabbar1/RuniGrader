#!/usr/bin/env python3
"""
Skill 8: Costs & Pricing Assessment
Scores based on cost analysis documentation and budget tracking.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_costs_pricing(repo_path):
    """
    Assess cost analysis and pricing documentation.

    Scoring:
    - Cost analysis document: 5.0 points
    - Cost mentions in docs: 3.0 points
    - Budget tracking: 2.0 points

    Total: 10 points
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "find_cost_analysis.py"
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
            "skill": "costs_pricing"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "costs_pricing"
        }

    score = 0.0
    notes = []
    recommendations = []

    # Get enhanced data from finder
    cost_docs = data.get("cost_documents", [])
    cost_mentions = data.get("cost_mentions", 0)
    files_with_cost = data.get("files_mentioning_cost", [])
    detailed_analysis = data.get("detailed_analysis_files", [])
    summary = data.get("summary", {})
    has_api_pricing = summary.get("has_api_pricing", False)
    has_cost_calculations = summary.get("has_cost_calculations", False)

    # Check for cost analysis document (5 points)
    cost_analysis_score = 0.0

    if len(cost_docs) > 0:
        cost_analysis_score = 5.0
        score += 5.0
        if len(cost_docs) == 1:
            notes.append(f"Cost analysis document found: {cost_docs[0]}")
        else:
            notes.append(f"Multiple cost documents found ({len(cost_docs)}): {', '.join(cost_docs[:2])}")
    elif len(detailed_analysis) > 0:
        # Give credit if detailed cost analysis exists in files (even without dedicated doc)
        cost_analysis_score = 3.0
        score += 3.0
        notes.append(f"Detailed cost analysis found in: {', '.join(detailed_analysis[:2])}")
        recommendations.append("Create dedicated cost analysis document (e.g., COSTS.md) for better organization (+2.0 points)")
    elif cost_mentions > 10:
        # Give partial credit for substantial cost discussion
        cost_analysis_score = 2.0
        score += 2.0
        notes.append(f"Substantial cost discussion found ({cost_mentions} mentions)")
        recommendations.append("Consolidate into dedicated cost analysis document (+3.0 points)")
    else:
        recommendations.append("Create cost analysis document (e.g., COSTS.md, budget.xlsx) (+5.0 points)")

    # Check for cost mentions and depth (3 points)
    cost_mentions_score = 0.0

    if cost_mentions > 20:
        cost_mentions_score = 3.0
        score += 3.0
        notes.append(f"Comprehensive cost documentation ({cost_mentions} mentions in {len(files_with_cost)} files)")
    elif cost_mentions > 10:
        cost_mentions_score = 2.0
        score += 2.0
        notes.append(f"Good cost documentation ({cost_mentions} mentions in {len(files_with_cost)} files)")
        recommendations.append("Add more detailed cost analysis (+1.0 point)")
    elif cost_mentions > 5:
        cost_mentions_score = 1.5
        score += 1.5
        notes.append(f"Moderate cost documentation ({cost_mentions} mentions)")
        recommendations.append("Expand cost documentation with more details (+1.5 points)")
    elif cost_mentions > 0:
        cost_mentions_score = 0.5
        score += 0.5
        notes.append(f"Limited cost documentation ({cost_mentions} mentions)")
        recommendations.append("Add detailed cost analysis (+2.5 points)")
    else:
        recommendations.append("Document costs, pricing, and budget considerations (+3.0 points)")

    # Check for budget tracking (2 points)
    budget_tracking_score = 0.0

    budget_files = [doc for doc in cost_docs if any(term in doc.lower() for term in ['budget', 'expense', 'financial'])]
    spreadsheet_files = [doc for doc in cost_docs if doc.endswith(('.xlsx', '.csv'))]

    if len(budget_files) > 0 or len(spreadsheet_files) > 0:
        budget_tracking_score = 2.0
        score += 2.0
        notes.append("Budget tracking system found")
    elif has_cost_calculations:
        # Give credit for cost calculations in code
        budget_tracking_score = 1.5
        score += 1.5
        notes.append("Cost calculations found in code")
        recommendations.append("Create dedicated budget tracking document (+0.5 points)")
    elif cost_mentions > 10:
        budget_tracking_score = 1.0
        score += 1.0
        notes.append("Some budget information in documentation")
        recommendations.append("Create dedicated budget tracking system (+1.0 point)")
    else:
        recommendations.append("Create budget tracking system/document (+2.0 points)")

    # Bonus recognition for API pricing analysis
    if has_api_pricing:
        notes.append("API pricing analysis found (excellent for LLM projects)")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "cost_analysis_score": cost_analysis_score,
        "cost_mentions_score": cost_mentions_score,
        "budget_tracking_score": budget_tracking_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "costs_pricing"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_costs_pricing(repo_path)
    print(json.dumps(result, indent=2))

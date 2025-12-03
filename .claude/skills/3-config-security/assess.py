#!/usr/bin/env python3
"""
Skill 3: Configuration & Security Assessment
Scores based on secrets scanning, environment variable usage, and configuration.
"""
import sys
import json
import subprocess
from pathlib import Path

def assess_config_security(repo_path):
    """
    Assess configuration and security practices.

    Scoring:
    - No hardcoded secrets: 2.0 points (deduct 2.0 if found)
    - .env.example exists: 2.0 points
    - .gitignore exists and includes .env: 2.0 points
    - Uses environment variables: 2.0 points (1.0 if documented in README only)
    - Good .gitignore coverage: 2.0 points

    Total: 10 points

    Note: Test files are excluded from secret scanning as they commonly
    contain hardcoded test credentials which is acceptable practice.
    """
    # Run the finder script
    finder_script = Path(__file__).parent / "scan_secrets.py"
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
            "skill": "config_security"
        }

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0,
            "max_score": 10.0,
            "error": "Could not parse finder output",
            "skill": "config_security"
        }

    score = 0.0
    notes = []
    recommendations = []
    secrets_score = 2.0  # Start with full points

    # Check for hardcoded secrets (2 points - deduct if found in non-test files)
    secrets_found = data.get("secrets_found", 0)
    findings = data.get("findings", [])

    if secrets_found > 0:
        # Lose 2 points for hardcoded secrets (not entire score)
        secrets_score = 0.0
        notes.append(f"WARNING: {secrets_found} hardcoded secret(s) found in production code!")
        for finding in findings[:3]:  # Show first 3
            notes.append(f"  - {finding['type']} in {finding['file']}:{finding['line']}")
        recommendations.append("Remove hardcoded secrets and use environment variables (+2.0 points)")
    else:
        score += 2.0
        notes.append("No hardcoded secrets found in production code")

    # Check for .env.example (2 points)
    env_config = data.get("env_configuration", {})
    env_example_score = 0.0

    if env_config.get("has_env_example"):
        env_example_score = 2.0
        score += 2.0
        notes.append(".env.example file found")
    else:
        recommendations.append("Create .env.example file to document required environment variables (+2.0 points)")

    # Check for .gitignore with .env (2 points)
    gitignore_score = 0.0

    if env_config.get("has_gitignore"):
        if env_config.get("env_in_gitignore"):
            gitignore_score = 2.0
            score += 2.0
            notes.append(".gitignore file found with .env properly ignored")
        else:
            gitignore_score = 1.0
            score += 1.0
            notes.append(".gitignore file found")
            recommendations.append("Add .env to .gitignore to prevent committing secrets (+1.0 point)")
    else:
        recommendations.append("Create .gitignore file and add .env to it (+2.0 points)")

    # Check for environment variable usage (2 points)
    env_vars_score = 0.0

    if env_config.get("uses_environment_variables"):
        env_var_count = env_config.get("env_var_usage_count", 0)
        env_documented_in_readme = env_config.get("env_documented_in_readme", False)

        if env_var_count >= 5:
            # Full credit for using environment variables in code
            env_vars_score = 2.0
        elif env_var_count >= 2:
            # Good usage, full credit
            env_vars_score = 2.0
        elif env_var_count >= 1:
            # Minimal usage
            env_vars_score = 1.5
        elif env_documented_in_readme:
            # Documented in README but not used in code (1 point out of 2)
            env_vars_score = 1.0
        else:
            env_vars_score = 0.5

        score += env_vars_score

        if env_documented_in_readme and env_var_count == 0:
            notes.append("Environment variables documented in README")
            recommendations.append("Implement environment variable usage in code (+1.0 point)")
        elif env_documented_in_readme and env_var_count < 2:
            notes.append(f"Uses environment variables ({env_var_count} instances) and documented in README")
            recommendations.append(f"Increase environment variable usage (+{2.0 - env_vars_score:.1f} points)")
        else:
            notes.append(f"Uses environment variables ({env_var_count} instances)")
            if env_vars_score < 2.0:
                recommendations.append(f"Increase environment variable usage (+{2.0 - env_vars_score:.1f} points)")
    else:
        recommendations.append("Use environment variables for configuration (+2.0 points)")

    # Check for good .gitignore coverage (2 points)
    gitignore_coverage_score = 0.0

    if env_config.get("has_gitignore"):
        # This is a bonus for having any .gitignore - already gave points above
        # Give additional points based on overall security posture
        if secrets_score > 0 and env_example_score > 0:
            gitignore_coverage_score = 2.0
            score += 2.0
            notes.append("Good security configuration overall")
        elif secrets_score > 0 or env_vars_score > 0:
            gitignore_coverage_score = 1.0
            score += 1.0
            notes.append("Adequate security configuration")
            recommendations.append("Improve overall security practices (+1.0 point)")
    else:
        recommendations.append("Improve .gitignore coverage for better security (+2.0 points)")

    return {
        "score": round(score, 1),
        "max_score": 10.0,
        "secrets_score": secrets_score,
        "env_example_score": env_example_score,
        "gitignore_score": gitignore_score,
        "env_vars_score": env_vars_score,
        "gitignore_coverage_score": gitignore_coverage_score,
        "notes": notes,
        "recommendations": recommendations,
        "skill": "config_security"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assess.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    result = assess_config_security(repo_path)
    print(json.dumps(result, indent=2))

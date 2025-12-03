#!/usr/bin/env python3
"""
Clone student repository from submission_info.xlsx if it doesn't exist.
"""
import os
import sys
import subprocess
import pandas as pd
from pathlib import Path

def get_repo_url_from_excel(student_folder):
    """Extract GitHub repository URL from submission_info.xlsx."""
    excel_path = Path(student_folder) / "submission_info.xlsx"

    if not excel_path.exists():
        return None, f"submission_info.xlsx not found in {student_folder}"

    try:
        df = pd.read_excel(excel_path)

        # Find the GitHub Repository row
        repo_row = df[df['Field'] == 'GitHub Repository']

        if repo_row.empty:
            return None, "GitHub Repository field not found in Excel"

        repo_url = repo_row['Value'].values[0]

        if pd.isna(repo_url) or not repo_url:
            return None, "GitHub Repository URL is empty"

        return str(repo_url).strip(), None

    except Exception as e:
        return None, f"Error reading Excel: {str(e)}"

def clean_github_url(repo_url):
    """Clean GitHub URL to get the actual clonable repository URL."""
    # Remove .git suffix if present
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]

    # Handle URLs with /tree/branch/path - extract just the repo part
    if '/tree/' in repo_url:
        # https://github.com/user/repo/tree/main/subfolder -> https://github.com/user/repo
        parts = repo_url.split('/tree/')
        repo_url = parts[0]

    # Handle URLs with /blob/branch/file
    if '/blob/' in repo_url:
        parts = repo_url.split('/blob/')
        repo_url = parts[0]

    return repo_url.rstrip('/')

def get_repo_name_from_url(repo_url):
    """Extract repository name from GitHub URL."""
    # Clean the URL first
    clean_url = clean_github_url(repo_url)

    parts = clean_url.rstrip('/').split('/')
    return parts[-1]

def clone_repository(repo_url, student_folder):
    """Clone the repository into the student folder."""
    # Clean the URL to get the actual clonable repository
    clean_url = clean_github_url(repo_url)
    repo_name = get_repo_name_from_url(repo_url)
    repo_path = Path(student_folder) / repo_name

    # Check if repo already exists
    if repo_path.exists():
        return str(repo_path), None, "already_exists"

    if clean_url != repo_url:
        print(f"Note: URL contains subdirectory path. Cloning full repository: {clean_url}")

    print(f"Cloning {clean_url} into {student_folder}...")

    try:
        result = subprocess.run(
            ['git', 'clone', clean_url],
            cwd=student_folder,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            return None, f"Git clone failed: {result.stderr}", "failed"

        if not repo_path.exists():
            return None, "Repository was not cloned successfully", "failed"

        print(f"Successfully cloned to {repo_path}")
        return str(repo_path), None, "cloned"

    except subprocess.TimeoutExpired:
        return None, "Git clone timed out (>120s)", "timeout"
    except FileNotFoundError:
        return None, "Git is not installed or not in PATH", "no_git"
    except Exception as e:
        return None, f"Error during clone: {str(e)}", "error"

def main():
    if len(sys.argv) < 2:
        print("Usage: python clone_repo.py <student_folder>")
        sys.exit(1)

    student_folder = sys.argv[1]

    if not os.path.exists(student_folder):
        print(f"Error: Student folder does not exist: {student_folder}")
        sys.exit(1)

    # Get repo URL from Excel
    repo_url, error = get_repo_url_from_excel(student_folder)

    if error:
        print(f"Error: {error}")
        sys.exit(1)

    print(f"Found repository URL: {repo_url}")

    # Clone the repository
    repo_path, error, status = clone_repository(repo_url, student_folder)

    if error:
        print(f"Error: {error}")
        sys.exit(1)

    if status == "already_exists":
        print(f"Repository already exists at: {repo_path}")
    elif status == "cloned":
        print(f"Successfully cloned repository to: {repo_path}")

    # Output the repo path for the orchestrator to use
    print(f"REPO_PATH:{repo_path}")
    sys.exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Analyze git history and version management practices."""
import os, sys, json, re, subprocess

def run_git_command(cmd, cwd):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.returncode
    except:
        return '', 1

def analyze_commits(repo_path):
    output, code = run_git_command('git log --oneline --all', repo_path)
    if code != 0:
        return {'error': 'Not a git repository or git not available'}

    commits = output.split('\n') if output else []
    commit_count = len(commits)

    # Analyze commit message quality
    meaningful = 0
    for commit in commits[:50]:  # Sample first 50
        msg = commit.split(' ', 1)[1] if ' ' in commit else ''
        if len(msg) > 10 and not re.match(r'^(fix|update|change|add)\s*$', msg, re.IGNORECASE):
            meaningful += 1

    meaningful_percent = (meaningful / min(50, commit_count) * 100) if commit_count > 0 else 0

    return {
        'total_commits': commit_count,
        'meaningful_messages': meaningful,
        'meaningful_percent': meaningful_percent,
        'sample_commits': commits[:10]
    }

def find_prompt_docs(root_dir):
    """Find ANY prompt documentation file (flexible naming)."""
    # Accept ANY file with 'prompt' in the name
    patterns = [r'prompt']  # Just look for 'prompt' anywhere in filename
    found_files = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            # Check if file contains 'prompt' and is a markdown/text file
            if re.search(r'prompt', filename, re.IGNORECASE) and filename.endswith(('.md', '.txt')):
                rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                found_files.append(rel_path)

    # Return first one found, or None
    return found_files[0] if found_files else None

def check_branching_strategy(repo_path):
    output, code = run_git_command('git branch -a', repo_path)
    if code != 0:
        return {'has_branches': False, 'branch_count': 0}

    branches = [b.strip() for b in output.split('\n') if b.strip()]
    return {
        'has_branches': len(branches) > 1,
        'branch_count': len(branches),
        'branches': branches[:10]
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_git_history.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    commit_analysis = analyze_commits(repo_path)
    prompt_docs = find_prompt_docs(repo_path)
    branching = check_branching_strategy(repo_path)
    output = {
        'commits': commit_analysis,
        'prompt_documentation': prompt_docs,  # Changed from prompt_book
        'branching': branching,
        'summary': {
            'has_git_history': commit_analysis.get('total_commits', 0) > 0,
            'has_prompt_documentation': prompt_docs is not None,  # Changed
            'commit_count': commit_analysis.get('total_commits', 0),
            'has_multiple_branches': branching['has_branches']
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

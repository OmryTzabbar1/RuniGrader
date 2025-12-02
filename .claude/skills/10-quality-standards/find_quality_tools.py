#!/usr/bin/env python3
"""Find quality tools, linters, and CI/CD configurations."""
import os, sys, json, re

def find_linting_config(root_dir):
    linting_files = []
    patterns = [
        '.pylintrc', 'pylint.cfg', '.flake8', 'setup.cfg', 'pyproject.toml',
        '.eslintrc', '.eslintrc.js', '.eslintrc.json',
        'tslint.json', '.prettierrc',
        'checkstyle.xml', 'pmd.xml'
    ]
    for pattern in patterns:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if pattern in filenames:
                rel_path = os.path.relpath(os.path.join(dirpath, pattern), root_dir)
                linting_files.append(rel_path)
    return linting_files

def find_ci_pipeline(root_dir):
    ci_files = []
    ci_dirs = ['.github/workflows', '.gitlab-ci.yml', '.travis.yml', '.circleci']

    gh_workflows = os.path.join(root_dir, '.github', 'workflows')
    if os.path.exists(gh_workflows):
        for f in os.listdir(gh_workflows):
            if f.endswith(('.yml', '.yaml')):
                ci_files.append(f'.github/workflows/{f}')

    for ci_file in ['.gitlab-ci.yml', '.travis.yml', 'circle.yml']:
        if os.path.exists(os.path.join(root_dir, ci_file)):
            ci_files.append(ci_file)

    return ci_files

def find_style_guides(root_dir):
    style_docs = []
    patterns = [r'style', r'coding.*standard', r'contributing', r'code.*of.*conduct']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith('.md'):
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                        style_docs.append(rel_path)
                        break
    return style_docs

def check_pre_commit_hooks(root_dir):
    pre_commit = os.path.join(root_dir, '.pre-commit-config.yaml')
    return os.path.exists(pre_commit)

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_quality_tools.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    linting = find_linting_config(repo_path)
    ci_files = find_ci_pipeline(repo_path)
    style_guides = find_style_guides(repo_path)
    has_pre_commit = check_pre_commit_hooks(repo_path)
    output = {
        'linting_config': linting,
        'ci_pipeline': ci_files,
        'style_guides': style_guides,
        'has_pre_commit_hooks': has_pre_commit,
        'summary': {
            'has_linting': len(linting) > 0,
            'has_ci': len(ci_files) > 0,
            'has_style_guide': len(style_guides) > 0,
            'has_pre_commit': has_pre_commit,
            'quality_score': sum([len(linting) > 0, len(ci_files) > 0, len(style_guides) > 0, has_pre_commit])
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

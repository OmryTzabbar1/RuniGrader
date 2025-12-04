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
    readme_has_quality = False

    # Patterns for dedicated style guide files
    patterns = [r'style', r'coding.*standard', r'contributing', r'code.*of.*conduct']

    readme_path = None
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith('.md'):
                # Track README location
                if filename.lower() == 'readme.md' and readme_path is None:
                    readme_path = os.path.join(dirpath, filename)

                # Check for dedicated style guide files
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        rel_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                        style_docs.append(rel_path)
                        break

    # If no dedicated style guides, check README for quality standards sections
    if len(style_docs) == 0 and readme_path:
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Look for quality-related sections
                quality_patterns = [
                    r'code.*quality', r'quality.*standard', r'linting', r'code.*style',
                    r'contributing', r'development.*guide', r'testing.*standard',
                    r'ci.*cd', r'continuous.*integration'
                ]

                for pattern in quality_patterns:
                    # Check for headers
                    header_pattern = r'^#{1,4}\s+.*' + pattern + r'.*$'
                    if re.search(header_pattern, content, re.IGNORECASE | re.MULTILINE):
                        readme_has_quality = True
                        style_docs.append('README.md (quality standards section)')
                        break

                # Also check for inline quality mentions
                if not readme_has_quality:
                    quality_keywords = ['pylint', 'eslint', 'prettier', 'black', 'flake8',
                                       'code quality', 'linting', 'ci/cd', 'github actions']
                    quality_count = sum(1 for keyword in quality_keywords
                                       if re.search(keyword, content, re.IGNORECASE))

                    if quality_count >= 3:
                        readme_has_quality = True
                        style_docs.append('README.md (quality tools mentioned)')
        except:
            pass

    return style_docs, readme_has_quality

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
    style_guides, readme_has_quality = find_style_guides(repo_path)
    has_pre_commit = check_pre_commit_hooks(repo_path)
    output = {
        'linting_config': linting,
        'ci_pipeline': ci_files,
        'style_guides': style_guides,
        'has_pre_commit_hooks': has_pre_commit,
        'readme_has_quality': readme_has_quality,
        'summary': {
            'has_linting': len(linting) > 0,
            'has_ci': len(ci_files) > 0,
            'has_style_guide': len(style_guides) > 0,
            'has_pre_commit': has_pre_commit,
            'readme_quality_info': readme_has_quality,
            'quality_score': sum([len(linting) > 0, len(ci_files) > 0, len(style_guides) > 0, has_pre_commit])
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Helper script to find and analyze code documentation.
Searches for README files, docstrings, and code structure documentation.
"""

import os
import sys
import json
import re

def find_readme_files(root_dir):
    """Find all README files in repository."""
    readme_files = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories and common excludes
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]

        for filename in filenames:
            if re.match(r'readme\.md$', filename, re.IGNORECASE):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                file_size = os.path.getsize(full_path)

                # Analyze README content
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    word_count = len(content.split())

                    has_installation = bool(re.search(r'install|setup|getting started', content, re.IGNORECASE))
                    has_usage = bool(re.search(r'usage|example|how to use|quick start', content, re.IGNORECASE))
                    has_api_docs = bool(re.search(r'api|reference|functions|methods|classes', content, re.IGNORECASE))
                    has_architecture = bool(re.search(r'architecture|structure|organization|design', content, re.IGNORECASE))
                    has_contributing = bool(re.search(r'contributing|development|setup', content, re.IGNORECASE))

                    # Count code blocks (documentation quality indicator)
                    code_blocks = len(re.findall(r'```', content)) // 2

                readme_files.append({
                    'path': rel_path,
                    'size_bytes': file_size,
                    'word_count': word_count,
                    'has_installation': has_installation,
                    'has_usage': has_usage,
                    'has_api_docs': has_api_docs,
                    'has_architecture': has_architecture,
                    'has_contributing': has_contributing,
                    'code_blocks': code_blocks,
                    'quality': 'comprehensive' if word_count > 500 else 'basic' if word_count > 200 else 'minimal'
                })

    return readme_files

def count_docstrings(root_dir):
    """Count docstrings in Python, JavaScript, and Java files."""
    docstring_stats = {
        'python': {'files': 0, 'with_docstrings': 0, 'total_docstrings': 0},
        'javascript': {'files': 0, 'with_docstrings': 0, 'total_docstrings': 0},
        'java': {'files': 0, 'with_docstrings': 0, 'total_docstrings': 0}
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    if filename.endswith('.py'):
                        docstring_stats['python']['files'] += 1
                        # Python docstrings: """...""" or '''...'''
                        docstrings = re.findall(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', content)
                        if docstrings:
                            docstring_stats['python']['with_docstrings'] += 1
                            docstring_stats['python']['total_docstrings'] += len(docstrings)

                    elif filename.endswith(('.js', '.ts')):
                        docstring_stats['javascript']['files'] += 1
                        # JSDoc: /** ... */
                        docstrings = re.findall(r'/\*\*[\s\S]*?\*/', content)
                        if docstrings:
                            docstring_stats['javascript']['with_docstrings'] += 1
                            docstring_stats['javascript']['total_docstrings'] += len(docstrings)

                    elif filename.endswith('.java'):
                        docstring_stats['java']['files'] += 1
                        # JavaDoc: /** ... */
                        docstrings = re.findall(r'/\*\*[\s\S]*?\*/', content)
                        if docstrings:
                            docstring_stats['java']['with_docstrings'] += 1
                            docstring_stats['java']['total_docstrings'] += len(docstrings)
            except:
                pass

    return docstring_stats

def find_additional_docs(root_dir):
    """Find additional documentation files."""
    doc_files = {
        'contributing': [],
        'changelog': [],
        'api_reference': [],
        'user_guide': [],
        'developer_guide': []
    }

    doc_patterns = {
        'contributing': r'contributing|development|dev_guide',
        'changelog': r'changelog|changes|history|releases',
        'api_reference': r'api|reference',
        'user_guide': r'user.*guide|manual|tutorial',
        'developer_guide': r'dev.*guide|developer'
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

        for filename in filenames:
            if filename.endswith(('.md', '.txt', '.rst')):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)

                for doc_type, pattern in doc_patterns.items():
                    if re.search(pattern, filename, re.IGNORECASE):
                        doc_files[doc_type].append(rel_path)

    return doc_files

def analyze_code_structure_docs(root_dir):
    """Check if code structure is documented."""
    structure_indicators = {
        'has_module_docs': False,
        'has_package_init': False,
        'docs_directory': False,
        'inline_comments': 0
    }

    # Check for docs/ directory
    docs_dir = os.path.join(root_dir, 'docs')
    if os.path.exists(docs_dir) and os.path.isdir(docs_dir):
        structure_indicators['docs_directory'] = True

    # Check for Python __init__.py with documentation
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__init__.py' in filenames:
            init_path = os.path.join(dirpath, '__init__.py')
            try:
                with open(init_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if '"""' in content or "'''" in content:
                        structure_indicators['has_package_init'] = True
                        break
            except:
                pass

    # Sample inline comments (check first 10 Python files)
    py_files_checked = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

        for filename in filenames:
            if filename.endswith('.py') and py_files_checked < 10:
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Count comment lines
                        comments = len([line for line in content.split('\n') if line.strip().startswith('#')])
                        structure_indicators['inline_comments'] += comments
                        py_files_checked += 1
                except:
                    pass

    return structure_indicators

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_documentation.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print(json.dumps({'error': f'Directory not found: {repo_path}'}))
        sys.exit(1)

    readme_files = find_readme_files(repo_path)
    docstring_stats = count_docstrings(repo_path)
    additional_docs = find_additional_docs(repo_path)
    structure_docs = analyze_code_structure_docs(repo_path)

    output = {
        'repo_path': repo_path,
        'readme_files': readme_files,
        'docstring_statistics': docstring_stats,
        'additional_documentation': additional_docs,
        'code_structure': structure_docs,
        'summary': {
            'has_readme': len(readme_files) > 0,
            'readme_quality': readme_files[0]['quality'] if readme_files else 'none',
            'total_readme_files': len(readme_files),
            'docstring_coverage': {
                lang: f"{stats['with_docstrings']}/{stats['files']}" if stats['files'] > 0 else "0/0"
                for lang, stats in docstring_stats.items()
            },
            'has_additional_docs': any(docs for docs in additional_docs.values())
        }
    }

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

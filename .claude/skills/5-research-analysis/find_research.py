#!/usr/bin/env python3
"""Find and analyze research artifacts (notebooks, PDFs, markdown, etc.)."""
import os, sys, json, re

def find_notebooks(root_dir):
    """Find Jupyter notebooks."""
    notebooks = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
        for filename in filenames:
            if filename.endswith('.ipynb'):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        has_plots = bool(re.search(r'matplotlib|seaborn|plotly|pyplot', content, re.IGNORECASE))
                        has_analysis = bool(re.search(r'pandas|numpy|scipy|sklearn', content, re.IGNORECASE))
                        cell_count = len(re.findall(r'"cell_type"', content))
                        notebooks.append({
                            'path': rel_path,
                            'size_bytes': os.path.getsize(full_path),
                            'has_plots': has_plots,
                            'has_analysis': has_analysis,
                            'cell_count': cell_count,
                            'type': 'jupyter'
                        })
                except:
                    pass
    return notebooks

def find_research_documents(root_dir):
    """Find research documents (PDFs, markdown files with research keywords)."""
    research_docs = []
    research_keywords = [
        r'research', r'analysis', r'experiment', r'results?', r'findings?',
        r'evaluation', r'benchmark', r'performance', r'comparison', r'study',
        r'survey', r'investigation', r'test', r'measurement'
    ]

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
        for filename in filenames:
            # Check for research PDFs or markdown files
            is_research_file = False
            file_type = None

            if filename.endswith('.pdf'):
                # Check if filename suggests research
                for keyword in research_keywords:
                    if re.search(keyword, filename, re.IGNORECASE):
                        is_research_file = True
                        file_type = 'pdf'
                        break
            elif filename.endswith('.md') and filename.lower() not in ['readme.md', 'contributing.md', 'license.md', 'changelog.md']:
                # Check markdown files (excluding standard docs)
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Check for research keywords or analysis content
                        for keyword in research_keywords:
                            if re.search(keyword, content, re.IGNORECASE):
                                is_research_file = True
                                file_type = 'markdown'
                                break
                except:
                    pass

            if is_research_file:
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                research_docs.append({
                    'path': rel_path,
                    'size_bytes': os.path.getsize(full_path),
                    'type': file_type
                })

    return research_docs

def find_data_files(root_dir):
    data_files = []
    patterns = [r'\.csv$', r'\.json$', r'\.xlsx?$', r'\.parquet$', r'\.pkl$']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_dir)
                    data_files.append({'path': rel_path, 'size_bytes': os.path.getsize(full_path)})
                    break
    return data_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_research.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    notebooks = find_notebooks(repo_path)
    research_docs = find_research_documents(repo_path)
    data_files = find_data_files(repo_path)

    # Combine all research artifacts
    all_research = notebooks + research_docs

    output = {
        'notebooks': notebooks,
        'research_documents': research_docs,
        'data_files': data_files,
        'summary': {
            'has_research': len(all_research) > 0,
            'total_research_count': len(all_research),
            'notebook_count': len(notebooks),
            'research_doc_count': len(research_docs),
            'notebooks_with_plots': sum(1 for n in notebooks if n.get('has_plots')),
            'has_data': len(data_files) > 0
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

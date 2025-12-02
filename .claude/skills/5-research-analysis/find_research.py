#!/usr/bin/env python3
"""Find and analyze Jupyter notebooks and research artifacts."""
import os, sys, json, re

def find_notebooks(root_dir):
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
                            'cell_count': cell_count
                        })
                except:
                    pass
    return notebooks

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
    data_files = find_data_files(repo_path)
    output = {
        'notebooks': notebooks,
        'data_files': data_files,
        'summary': {
            'has_notebooks': len(notebooks) > 0,
            'notebook_count': len(notebooks),
            'notebooks_with_plots': sum(1 for n in notebooks if n['has_plots']),
            'has_data': len(data_files) > 0
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Find cost analysis and budget documentation."""
import os, sys, json, re

def find_cost_docs(root_dir):
    cost_docs = []
    patterns = [r'cost', r'pricing', r'budget', r'expense', r'financial']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith(('.md', '.txt', '.pdf', '.xlsx', '.csv')):
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        full_path = os.path.join(dirpath, filename)
                        rel_path = os.path.relpath(full_path, root_dir)
                        cost_docs.append(rel_path)
                        break
    return cost_docs

def search_cost_content(root_dir):
    cost_mentions = 0
    files_with_cost = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith(('.md', '.txt')):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(r'\$\d+|\bcost\b|\bprice\b|\bbudget\b|\bexpense\b', content, re.IGNORECASE):
                            rel_path = os.path.relpath(full_path, root_dir)
                            files_with_cost.append(rel_path)
                            cost_mentions += len(re.findall(r'\$\d+|\bcost\b|\bprice\b|\bbudget\b', content, re.IGNORECASE))
                except:
                    pass
    return cost_mentions, files_with_cost

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_cost_analysis.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    cost_docs = find_cost_docs(repo_path)
    cost_mentions, files_with_cost = search_cost_content(repo_path)
    output = {
        'cost_documents': cost_docs,
        'cost_mentions': cost_mentions,
        'files_mentioning_cost': files_with_cost,
        'summary': {
            'has_cost_docs': len(cost_docs) > 0,
            'has_cost_analysis': cost_mentions > 5,
            'total_mentions': cost_mentions
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

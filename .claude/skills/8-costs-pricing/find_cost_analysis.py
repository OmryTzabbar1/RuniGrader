#!/usr/bin/env python3
"""Find cost analysis and budget documentation."""
import os, sys, json, re

def find_cost_docs(root_dir):
    cost_docs = []
    patterns = [r'cost', r'pricing', r'budget', r'expense', r'financial']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith(('.md', '.txt', '.pdf', '.xlsx', '.csv', '.json')):
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
    detailed_cost_analysis = []
    api_pricing_found = False
    cost_calculations_found = False

    # Enhanced cost-related patterns
    cost_keywords = [
        r'\$\d+(?:\.\d{2})?',  # Dollar amounts like $10.00
        r'\bcost\b', r'\bprice\b', r'\bpricing\b', r'\bbudget\b', r'\bexpense\b',
        r'\btotal[_\s]cost\b', r'\bunit[_\s]cost\b', r'\bmonthly[_\s]cost\b',
        r'\bapi[_\s]cost\b', r'\btoken[_\s]cost\b', r'\btoken[_\s]price\b',
        r'\bfinancial\b', r'\bROI\b', r'\breturn on investment\b'
    ]

    # API pricing patterns
    api_patterns = [
        r'openai.*pricing', r'anthropic.*pricing', r'claude.*pricing',
        r'gpt.*pricing', r'api.*cost', r'token.*\$', r'\$.*token',
        r'price.*per.*token', r'cost.*per.*request'
    ]

    # Cost calculation patterns (in code)
    calc_patterns = [
        r'calculate.*cost', r'compute.*cost', r'total.*cost\s*=',
        r'cost\s*\*', r'price\s*\*', r'budget\s*-', r'expense\s*\+'
    ]

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
        for filename in filenames:
            # Check more file types
            if filename.endswith(('.md', '.txt', '.py', '.js', '.ipynb', '.json')):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                        # Count cost mentions using enhanced patterns
                        file_cost_mentions = 0
                        for pattern in cost_keywords:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            file_cost_mentions += len(matches)

                        if file_cost_mentions > 0:
                            rel_path = os.path.relpath(full_path, root_dir)
                            files_with_cost.append(rel_path)
                            cost_mentions += file_cost_mentions

                            # Check for detailed analysis (>10 mentions in one file)
                            if file_cost_mentions > 10:
                                detailed_cost_analysis.append(rel_path)

                        # Check for API pricing analysis
                        for pattern in api_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                api_pricing_found = True
                                break

                        # Check for cost calculations in code
                        for pattern in calc_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                cost_calculations_found = True
                                break

                except:
                    pass

    return cost_mentions, files_with_cost, detailed_cost_analysis, api_pricing_found, cost_calculations_found

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_cost_analysis.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    cost_docs = find_cost_docs(repo_path)
    cost_mentions, files_with_cost, detailed_analysis, api_pricing, cost_calculations = search_cost_content(repo_path)
    output = {
        'cost_documents': cost_docs,
        'cost_mentions': cost_mentions,
        'files_mentioning_cost': files_with_cost,
        'detailed_analysis_files': detailed_analysis,
        'summary': {
            'has_cost_docs': len(cost_docs) > 0,
            'has_cost_analysis': cost_mentions > 5,
            'has_detailed_analysis': len(detailed_analysis) > 0,
            'has_api_pricing': api_pricing,
            'has_cost_calculations': cost_calculations,
            'total_mentions': cost_mentions,
            'files_count': len(files_with_cost)
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

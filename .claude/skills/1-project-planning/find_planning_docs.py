#!/usr/bin/env python3
"""
Helper script to find project planning documents in any location.
Searches recursively for PRD, Architecture, and Planning documents.
"""

import os
import sys
import json
import re

def find_files_case_insensitive(root_dir, patterns):
    """Find files matching patterns (case-insensitive)."""
    matches = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        for filename in filenames:
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_dir)
                    matches.append(rel_path)
                    break
    return matches

def check_file_sections(filepath, required_sections):
    """Check if file contains required sections (case-insensitive)."""
    found_sections = []
    missing_sections = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            for section in required_sections:
                # Look for markdown headers: # Section, ## Section, ### Section
                pattern = r'^#{1,3}\s+' + re.escape(section)
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    found_sections.append(section)
                # Also check without # (plain text sections)
                elif re.search(r'\b' + re.escape(section) + r'\b', content, re.IGNORECASE):
                    found_sections.append(section + " (found as text)")
                else:
                    missing_sections.append(section)
    except Exception as e:
        return [], required_sections, str(e)

    return found_sections, missing_sections, None

def analyze_prd(root_dir):
    """Find and analyze PRD documents."""
    prd_patterns = [
        r'prd\.md$',
        r'product.*requirements?\.md$',
        r'requirements?\.md$',
        r'prd\.txt$'
    ]

    prd_files = find_files_case_insensitive(root_dir, prd_patterns)

    required_sections = [
        "Problem Statement",
        "Functional Requirements",
        "Non-Functional Requirements",
        "Success Metrics",
        "Technical Constraints",
        "User Stories"
    ]

    results = []
    for prd_file in prd_files:
        full_path = os.path.join(root_dir, prd_file)
        file_size = os.path.getsize(full_path)
        found, missing, error = check_file_sections(full_path, required_sections)

        results.append({
            'path': prd_file,
            'size_bytes': file_size,
            'found_sections': found,
            'missing_sections': missing,
            'error': error,
            'completeness': len(found) / len(required_sections) * 100
        })

    return results

def analyze_architecture(root_dir):
    """Find and analyze Architecture documents."""
    arch_patterns = [
        r'architect.*\.md$',
        r'design\.md$',
        r'planning\.md$',
        r'technical.*design\.md$'
    ]

    arch_files = find_files_case_insensitive(root_dir, arch_patterns)

    # Look for diagrams
    diagram_patterns = [
        r'\.png$',
        r'\.jpg$',
        r'\.svg$',
        r'\.puml$',
        r'\.plantuml$'
    ]
    diagram_files = find_files_case_insensitive(root_dir, diagram_patterns)

    results = []
    for arch_file in arch_files:
        full_path = os.path.join(root_dir, arch_file)
        file_size = os.path.getsize(full_path)

        # Check for C4 model mentions and diagrams
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            has_c4_context = bool(re.search(r'context\s+diagram|c4.*context|system.*context', content, re.IGNORECASE))
            has_c4_container = bool(re.search(r'container\s+diagram|c4.*container', content, re.IGNORECASE))
            has_c4_component = bool(re.search(r'component\s+diagram|c4.*component', content, re.IGNORECASE))
            has_mermaid = bool(re.search(r'```mermaid', content, re.IGNORECASE))
            has_plantuml = bool(re.search(r'```plantuml|@startuml', content, re.IGNORECASE))
            has_tech_stack = bool(re.search(r'technology stack|tech stack|technologies used', content, re.IGNORECASE))

        results.append({
            'path': arch_file,
            'size_bytes': file_size,
            'has_c4_context': has_c4_context,
            'has_c4_container': has_c4_container,
            'has_c4_component': has_c4_component,
            'has_mermaid': has_mermaid,
            'has_plantuml': has_plantuml,
            'has_tech_stack': has_tech_stack,
            'related_diagrams': [d for d in diagram_files if os.path.dirname(d) == os.path.dirname(arch_file)]
        })

    return results, diagram_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_planning_docs.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print(json.dumps({'error': f'Directory not found: {repo_path}'}))
        sys.exit(1)

    prd_results = analyze_prd(repo_path)
    arch_results, all_diagrams = analyze_architecture(repo_path)

    output = {
        'repo_path': repo_path,
        'prd_documents': prd_results,
        'architecture_documents': arch_results,
        'all_diagram_files': all_diagrams,
        'summary': {
            'has_prd': len(prd_results) > 0,
            'has_architecture': len(arch_results) > 0,
            'total_diagrams': len(all_diagrams),
            'prd_count': len(prd_results),
            'arch_count': len(arch_results)
        }
    }

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

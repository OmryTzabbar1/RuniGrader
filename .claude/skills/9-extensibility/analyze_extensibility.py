#!/usr/bin/env python3
"""Analyze code extensibility and plugin architecture."""
import os, sys, json, re

def find_plugin_system(root_dir):
    plugin_dirs = []
    patterns = ['plugin', 'plugins', 'extension', 'extensions', 'addon', 'addons']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for pattern in patterns:
            if pattern in [d.lower() for d in dirnames]:
                plugin_dirs.append(os.path.relpath(dirpath, root_dir))
    return plugin_dirs

def find_interfaces(root_dir):
    interfaces = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith(('.py', '.java', '.ts')):
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(r'@abstractmethod|class.*\(ABC\)|interface\s+\w+|abstract class', content):
                            rel_path = os.path.relpath(full_path, root_dir)
                            interfaces.append(rel_path)
                except:
                    pass
    return interfaces

def check_modular_structure(root_dir):
    # Count Python/JS files and check average size
    files_checked = 0
    total_lines = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith(('.py', '.js', '.ts')) and files_checked < 20:
                full_path = os.path.join(dirpath, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        files_checked += 1
                except:
                    pass
    avg_lines = total_lines / files_checked if files_checked > 0 else 0
    return {'files_sampled': files_checked, 'avg_lines_per_file': avg_lines, 'is_modular': avg_lines < 200}

def find_extensibility_docs(root_dir):
    """Find extensibility/plugin documentation files and README sections."""
    doc_files = []
    doc_quality = {'has_extension_points': False, 'has_examples': False, 'word_count': 0, 'in_readme': False}

    # Patterns for dedicated extensibility documentation files
    patterns = [
        r'extensibility',
        r'extension',
        r'plugin',
        r'customization',
        r'api.*guide',
        r'developer.*guide',
        r'extending'
    ]

    readme_path = None

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        for filename in filenames:
            # Check markdown, text, or doc files
            if filename.endswith(('.md', '.txt', '.rst', '.adoc')):
                # Track README location
                if filename.lower() == 'readme.md' and readme_path is None:
                    readme_path = os.path.join(dirpath, filename)

                # Check for dedicated extensibility docs
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        full_path = os.path.join(dirpath, filename)
                        rel_path = os.path.relpath(full_path, root_dir)

                        # Analyze content quality
                        try:
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                word_count = len(content.split())

                                # Check for extension points documentation
                                if re.search(r'extension point|plugin.*interface|custom.*class|extend.*system|override|hook', content, re.IGNORECASE):
                                    doc_quality['has_extension_points'] = True

                                # Check for code examples
                                if re.search(r'```|example.*:|usage.*:|class.*extends|def.*override', content, re.IGNORECASE):
                                    doc_quality['has_examples'] = True

                                doc_quality['word_count'] = max(doc_quality['word_count'], word_count)

                        except:
                            pass

                        doc_files.append(rel_path)
                        break

    # If no dedicated extensibility docs found, check README for extensibility sections
    if len(doc_files) == 0 and readme_path:
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Look for extensibility-related headers and content
                ext_section_found = False
                ext_content = []

                for pattern in patterns:
                    # Find headers with extensibility keywords
                    header_pattern = r'^#{1,4}\s+.*' + pattern + r'.*$'
                    matches = re.finditer(header_pattern, content, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        ext_section_found = True
                        # Extract section content (from header to next header of same level)
                        start = match.start()
                        header_level = len(match.group().split()[0])  # Count # symbols

                        # Find next header of same or higher level
                        next_header = re.search(r'\n#{1,' + str(header_level) + r'}\s+', content[start+1:])
                        end = start + next_header.start() if next_header else len(content)

                        section = content[start:end]
                        ext_content.append(section)

                if ext_section_found:
                    combined_content = '\n'.join(ext_content)
                    word_count = len(combined_content.split())

                    # Check for extension points
                    if re.search(r'extension point|plugin.*interface|custom.*class|extend.*system|override|hook|base class', combined_content, re.IGNORECASE):
                        doc_quality['has_extension_points'] = True

                    # Check for code examples
                    if re.search(r'```|example.*:|usage.*:|class.*extends|def.*override', combined_content, re.IGNORECASE):
                        doc_quality['has_examples'] = True

                    doc_quality['word_count'] = word_count
                    doc_quality['in_readme'] = True
                    doc_files.append('README.md (extensibility section)')
        except:
            pass

    return doc_files, doc_quality

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_extensibility.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    plugin_dirs = find_plugin_system(repo_path)
    interfaces = find_interfaces(repo_path)
    modularity = check_modular_structure(repo_path)
    ext_docs, doc_quality = find_extensibility_docs(repo_path)
    output = {
        'plugin_directories': plugin_dirs,
        'interface_files': interfaces,
        'modularity': modularity,
        'extensibility_docs': ext_docs,
        'doc_quality': doc_quality,
        'summary': {
            'has_plugin_system': len(plugin_dirs) > 0,
            'has_interfaces': len(interfaces) > 0,
            'is_modular': modularity['is_modular'],
            'interface_count': len(interfaces),
            'has_extension_docs': len(ext_docs) > 0,
            'extension_doc_count': len(ext_docs)
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

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

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_extensibility.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    plugin_dirs = find_plugin_system(repo_path)
    interfaces = find_interfaces(repo_path)
    modularity = check_modular_structure(repo_path)
    output = {
        'plugin_directories': plugin_dirs,
        'interface_files': interfaces,
        'modularity': modularity,
        'summary': {
            'has_plugin_system': len(plugin_dirs) > 0,
            'has_interfaces': len(interfaces) > 0,
            'is_modular': modularity['is_modular'],
            'interface_count': len(interfaces)
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

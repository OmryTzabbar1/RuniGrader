#!/usr/bin/env python3
"""Find and analyze UI/UX documentation and screenshots."""
import os, sys, json, re

def find_screenshots(root_dir):
    images = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if re.search(r'\.(png|jpg|jpeg|gif|svg|webp)$', filename, re.IGNORECASE):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                images.append({'path': rel_path, 'size_bytes': os.path.getsize(full_path)})
    return images

def find_ui_docs(root_dir):
    ui_docs = []
    patterns = [r'ui', r'interface', r'design', r'user.*guide', r'screenshot', r'wireframe', r'mockup']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        for filename in filenames:
            if filename.endswith(('.md', '.txt', '.pdf')):
                for pattern in patterns:
                    if re.search(pattern, filename, re.IGNORECASE):
                        full_path = os.path.join(dirpath, filename)
                        rel_path = os.path.relpath(full_path, root_dir)
                        ui_docs.append(rel_path)
                        break
    return ui_docs

def check_readme_screenshots(root_dir):
    readme_paths = []
    for root, dirs, files in os.walk(root_dir):
        if 'README.md' in files or 'readme.md' in files:
            readme = 'README.md' if 'README.md' in files else 'readme.md'
            readme_paths.append(os.path.join(root, readme))

    has_screenshots = False
    for readme_path in readme_paths:
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if re.search(r'!\[.*\]\(.*\.(png|jpg|gif|svg)', content, re.IGNORECASE):
                    has_screenshots = True
                    break
        except:
            pass
    return has_screenshots

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_ui_docs.py <repo_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    images = find_screenshots(repo_path)
    ui_docs = find_ui_docs(repo_path)
    readme_has_screenshots = check_readme_screenshots(repo_path)
    output = {
        'images': images,
        'ui_documentation': ui_docs,
        'readme_has_screenshots': readme_has_screenshots,
        'summary': {
            'has_images': len(images) > 0,
            'image_count': len(images),
            'has_ui_docs': len(ui_docs) > 0,
            'readme_includes_screenshots': readme_has_screenshots
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

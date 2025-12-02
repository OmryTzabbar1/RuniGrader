#!/usr/bin/env python3
"""
Advanced secret scanner that detects hardcoded credentials and API keys.
More thorough than simple grep patterns.
"""

import os
import sys
import json
import re

# Patterns for detecting secrets
SECRET_PATTERNS = [
    # API Keys
    (r'api[_-]?key\s*[=:]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', 'API Key (hardcoded)'),
    (r'apikey\s*[=:]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', 'API Key (hardcoded)'),
    (r'api[_-]?secret\s*[=:]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', 'API Secret (hardcoded)'),

    # OpenAI Keys
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI API Key'),
    (r'OPENAI_API_KEY\s*[=:]\s*["\']sk-[a-zA-Z0-9]{20,}["\']', 'OpenAI Key (hardcoded)'),

    # AWS Keys
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'aws[_-]?access[_-]?key[_-]?id\s*[=:]\s*["\']([A-Z0-9]{20})["\']', 'AWS Access Key'),
    (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']([A-Za-z0-9/+=]{40})["\']', 'AWS Secret Key'),

    # Google Cloud
    (r'AIza[0-9A-Za-z\-_]{35}', 'Google API Key'),

    # GitHub Tokens
    (r'ghp_[0-9a-zA-Z]{36}', 'GitHub Personal Access Token'),
    (r'gho_[0-9a-zA-Z]{36}', 'GitHub OAuth Token'),

    # Generic secrets
    (r'password\s*[=:]\s*["\'](?!.*\$\{)([^"\']{8,})["\']', 'Hardcoded Password'),
    (r'secret\s*[=:]\s*["\'](?!.*\$\{)([a-zA-Z0-9_\-]{15,})["\']', 'Hardcoded Secret'),
    (r'token\s*[=:]\s*["\'](?!.*\$\{)([a-zA-Z0-9_\-]{20,})["\']', 'Hardcoded Token'),

    # Database credentials
    (r'jdbc:.*://.*:.*@', 'Database URL with credentials'),
    (r'mongodb://[^:]+:[^@]+@', 'MongoDB URL with credentials'),
    (r'postgres://[^:]+:[^@]+@', 'PostgreSQL URL with credentials'),
]

# Files to skip
SKIP_PATTERNS = [
    r'\.git/',
    r'node_modules/',
    r'__pycache__/',
    r'\.pyc$',
    r'venv/',
    r'env/',
    r'\.lock$',
    r'package-lock\.json$',
    r'yarn\.lock$',
    r'\.min\.js$',
]

# File extensions to scan
SCAN_EXTENSIONS = [
    '.py', '.js', '.ts', '.java', '.go', '.rb', '.php',
    '.sh', '.bash', '.env', '.config', '.json', '.yaml', '.yml',
    '.txt', '.md', '.properties', '.conf'
]

def should_skip(filepath):
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False

def scan_file(filepath):
    """Scan a single file for secrets."""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            for line_num, line in enumerate(content.split('\n'), 1):
                # Skip comments (basic detection)
                line_stripped = line.strip()
                if line_stripped.startswith('#') or line_stripped.startswith('//'):
                    continue

                for pattern, secret_type in SECRET_PATTERNS:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Extract the matched secret (mask most of it)
                        secret_value = match.group(0)

                        # Check if it's a placeholder (contains YOUR, PLACEHOLDER, EXAMPLE, INSERT, etc.)
                        placeholder_indicators = ['YOUR', 'PLACEHOLDER', 'EXAMPLE', 'INSERT', 'XXX', 'TODO', 'CHANGE', 'REPLACE']
                        is_placeholder = any(indicator in secret_value.upper() for indicator in placeholder_indicators)

                        # Skip if it's a placeholder
                        if is_placeholder:
                            continue

                        if len(secret_value) > 10:
                            masked = secret_value[:4] + '*' * (len(secret_value) - 8) + secret_value[-4:]
                        else:
                            masked = secret_value[:2] + '*' * (len(secret_value) - 2)

                        findings.append({
                            'file': filepath,
                            'line': line_num,
                            'type': secret_type,
                            'matched': masked,
                            'severity': 'CRITICAL',
                            'context': line.strip()[:100]
                        })

    except Exception as e:
        pass

    return findings

def scan_repository(repo_path):
    """Scan entire repository for secrets."""
    all_findings = []
    files_scanned = 0

    for root, dirs, files in os.walk(repo_path):
        # Skip hidden and ignored directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]

        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, repo_path)

            if should_skip(rel_path):
                continue

            # Check if file extension should be scanned
            _, ext = os.path.splitext(filename)
            if ext not in SCAN_EXTENSIONS and filename not in ['.env', '.env.example', 'config']:
                continue

            findings = scan_file(filepath)
            if findings:
                all_findings.extend([{**f, 'file': rel_path} for f in findings])

            files_scanned += 1

    return all_findings, files_scanned

def check_env_files(repo_path):
    """Check for .env.example and .gitignore."""
    checks = {
        'has_env_example': False,
        'has_gitignore': False,
        'env_in_gitignore': False,
        'uses_environment_variables': False
    }

    # Check for .env.example
    env_example_paths = ['.env.example', 'env.example', '.env.sample', 'example.env']
    for env_file in env_example_paths:
        if os.path.exists(os.path.join(repo_path, env_file)):
            checks['has_env_example'] = True
            break

    # Check for .gitignore
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.exists(gitignore_path):
        checks['has_gitignore'] = True
        with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
            gitignore_content = f.read()
            if re.search(r'\.env', gitignore_content):
                checks['env_in_gitignore'] = True

    # Check if code uses environment variables
    env_var_count = 0
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        for filename in files:
            if filename.endswith(('.py', '.js', '.ts', '.java')):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        env_var_count += len(re.findall(r'os\.getenv|process\.env|System\.getenv', content))
                except:
                    pass

    checks['uses_environment_variables'] = env_var_count > 0
    checks['env_var_usage_count'] = env_var_count

    return checks

def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_secrets.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print(json.dumps({'error': f'Directory not found: {repo_path}'}))
        sys.exit(1)

    print(f"Scanning {repo_path} for hardcoded secrets...", file=sys.stderr)

    findings, files_scanned = scan_repository(repo_path)
    env_checks = check_env_files(repo_path)

    output = {
        'repo_path': repo_path,
        'files_scanned': files_scanned,
        'secrets_found': len(findings),
        'findings': findings,
        'env_configuration': env_checks,
        'security_status': 'FAIL' if findings else 'PASS',
        'critical_issues': len([f for f in findings if f['severity'] == 'CRITICAL'])
    }

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Helper script to find and analyze test files and test coverage.
"""

import os
import sys
import json
import re

def find_test_files(root_dir):
    """Find all test files in repository."""
    test_files = []
    test_patterns = [
        r'test_.*\.py$',
        r'.*_test\.py$',
        r'.*\.test\.js$',
        r'.*\.test\.ts$',
        r'.*\.spec\.js$',
        r'.*\.spec\.ts$',
        r'Test.*\.java$',
        r'.*Test\.java$'
    ]

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

        for filename in filenames:
            for pattern in test_patterns:
                if re.search(pattern, filename):
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_dir)
                    file_size = os.path.getsize(full_path)

                    # Analyze test file content
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                            # Count test functions/methods
                            test_count = 0
                            test_count += len(re.findall(r'def test_', content))  # Python
                            test_count += len(re.findall(r'it\(|test\(|describe\(', content))  # JS/TS
                            test_count += len(re.findall(r'@Test', content))  # Java

                            # Check for assertions
                            assertions = 0
                            assertions += len(re.findall(r'assert|assertEquals|expect\(|toBe\(', content, re.IGNORECASE))

                            # Check for mocking
                            has_mocks = bool(re.search(r'mock|Mock|stub|Stub|spy|Spy|patch', content))

                            test_files.append({
                                'path': rel_path,
                                'size_bytes': file_size,
                                'test_count': test_count,
                                'assertions': assertions,
                                'has_mocks': has_mocks
                            })
                    except:
                        pass
                    break

    return test_files

def find_coverage_config(root_dir):
    """Find test coverage configuration files."""
    coverage_files = []
    coverage_patterns = [
        'pytest.ini',
        '.coveragerc',
        'coverage.xml',
        'jest.config.js',
        'jest.config.ts',
        'karma.conf.js',
        '.nycrc',
        'jacoco.xml'
    ]

    for pattern in coverage_patterns:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

            if pattern in filenames:
                full_path = os.path.join(dirpath, pattern)
                rel_path = os.path.relpath(full_path, root_dir)
                coverage_files.append(rel_path)

    return coverage_files

def analyze_test_quality(test_files):
    """Analyze overall test quality."""
    if not test_files:
        return {
            'total_tests': 0,
            'total_assertions': 0,
            'files_with_mocks': 0,
            'quality': 'none'
        }

    total_tests = sum(f['test_count'] for f in test_files)
    total_assertions = sum(f['assertions'] for f in test_files)
    files_with_mocks = sum(1 for f in test_files if f['has_mocks'])

    quality = 'poor'
    if total_tests >= 20 and total_assertions >= 40 and files_with_mocks >= 2:
        quality = 'excellent'
    elif total_tests >= 10 and total_assertions >= 20:
        quality = 'good'
    elif total_tests >= 5:
        quality = 'adequate'

    return {
        'total_tests': total_tests,
        'total_assertions': total_assertions,
        'files_with_mocks': files_with_mocks,
        'mock_coverage_percent': (files_with_mocks / len(test_files) * 100) if test_files else 0,
        'quality': quality
    }

def check_ci_testing(root_dir):
    """Check if tests run in CI/CD."""
    ci_files = []
    ci_patterns = [
        '.github/workflows/*.yml',
        '.github/workflows/*.yaml',
        '.gitlab-ci.yml',
        '.travis.yml',
        'circle.yml',
        '.circleci/config.yml'
    ]

    has_ci_testing = False

    # Check GitHub Actions
    gh_workflows = os.path.join(root_dir, '.github', 'workflows')
    if os.path.exists(gh_workflows):
        for filename in os.listdir(gh_workflows):
            if filename.endswith(('.yml', '.yaml')):
                filepath = os.path.join(gh_workflows, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(r'pytest|npm test|mvn test|gradle test', content):
                            has_ci_testing = True
                            ci_files.append(f'.github/workflows/{filename}')
                except:
                    pass

    # Check other CI files
    other_ci = ['.gitlab-ci.yml', '.travis.yml', 'circle.yml']
    for ci_file in other_ci:
        filepath = os.path.join(root_dir, ci_file)
        if os.path.exists(filepath):
            ci_files.append(ci_file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if re.search(r'test|pytest|npm test', content):
                        has_ci_testing = True
            except:
                pass

    return {
        'has_ci': len(ci_files) > 0,
        'has_ci_testing': has_ci_testing,
        'ci_files': ci_files
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_tests.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not os.path.exists(repo_path):
        print(json.dumps({'error': f'Directory not found: {repo_path}'}))
        sys.exit(1)

    test_files = find_test_files(repo_path)
    coverage_config = find_coverage_config(repo_path)
    test_quality = analyze_test_quality(test_files)
    ci_info = check_ci_testing(repo_path)

    output = {
        'repo_path': repo_path,
        'test_files': test_files,
        'coverage_config': coverage_config,
        'test_quality': test_quality,
        'ci_testing': ci_info,
        'summary': {
            'has_tests': len(test_files) > 0,
            'test_file_count': len(test_files),
            'total_test_count': test_quality['total_tests'],
            'has_coverage_config': len(coverage_config) > 0,
            'has_ci_testing': ci_info['has_ci_testing'],
            'quality_level': test_quality['quality']
        }
    }

    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Convenience script to process all WorkSubmissions folders.

Usage:
    python run_all.py
"""

import os
import sys
import subprocess
from pathlib import Path


def run_assignment(assignment_dir, assignment_name, assignment_num):
    """Run processing for one assignment."""
    print(f"\n{'='*80}")
    print(f"PROCESSING {assignment_name}")
    print(f"{'='*80}\n")

    report_file = f"submission_grades_report_hw{assignment_num}.json"

    cmd = [
        sys.executable,
        ".claude/skills/submission-info-updater/process_assignment.py",
        "--assignment-dir", assignment_dir,
        "--assignment-name", assignment_name,
        "--output-report", report_file
    ]

    try:
        result = subprocess.run(cmd, check=False, text=True,
                              capture_output=False, encoding='utf-8')
        return result.returncode == 0
    except Exception as e:
        print(f"Error processing {assignment_name}: {e}")
        return False


def main():
    """Process all three assignments."""
    base_dir = Path("C:/Users/Guest1/CoOp/Runi")
    os.chdir(base_dir)

    assignments = [
        ("WorkSubmissions01", "Assignment 1", 1),
        ("WorkSubmissions02", "Assignment 2", 2),
        ("WorkSubmissions03", "Assignment 3", 3),
    ]

    results = {}
    for folder, name, num in assignments:
        full_path = base_dir / folder
        if full_path.exists():
            success = run_assignment(str(full_path), name, num)
            results[name] = success
        else:
            print(f"Warning: {folder} not found, skipping...")
            results[name] = False

    # Summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    for name, success in results.items():
        status = "[OK]" if success else "[FAILED]"
        print(f"  {status} {name}")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()

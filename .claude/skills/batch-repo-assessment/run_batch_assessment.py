#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run git-repo-assessment for all students and organize outputs
This script will be called by Claude Code to process repositories in batches
"""

import os
import sys
import json
from pathlib import Path

# Set UTF-8 encoding for stdout
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def load_assessments(json_file='assessments_batch.json'):
    """Load the assessment batch JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_assessment_commands(assessments, batch_size=5):
    """Print the assessment commands for Claude to execute in batches."""
    total = len(assessments)

    print(f"Total repositories to assess: {total}\n")
    print(f"Processing in batches of {batch_size}\n")

    # Group into batches
    for batch_idx in range(0, total, batch_size):
        batch = assessments[batch_idx:batch_idx + batch_size]
        batch_num = (batch_idx // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size

        print(f"{'='*80}")
        print(f"BATCH {batch_num}/{total_batches} ({len(batch)} repositories)")
        print(f"{'='*80}\n")

        for idx, assessment in enumerate(batch, 1):
            pid = assessment['participant_id']
            url = assessment['github_url']
            group = assessment['group_code']
            folder = assessment['folder_path']

            print(f"{idx}. Participant {pid} - Group: {group}")
            print(f"   URL: {url}")
            print(f"   Output folder: {folder}")
            print()

        print(f"Next steps for Batch {batch_num}:")
        print(f"1. Call /git-repo-assessment for each URL above")
        print(f"2. Move the generated markdown file to the corresponding student folder")
        print(f"3. Rename to 'repo_assessment.md' in each folder")
        print()


def generate_move_commands(assessments):
    """Generate file move commands after assessments are complete."""
    print("\n" + "="*80)
    print("AFTER RUNNING ASSESSMENTS - Move files to student folders:")
    print("="*80 + "\n")

    for assessment in assessments:
        pid = assessment['participant_id']
        folder = assessment['folder_path']

        # The assessment output will be in the current directory with some naming pattern
        # We'll need to identify and move it
        print(f"# Participant {pid}")
        print(f"# Move assessment file to: {folder}\\repo_assessment.md")
        print()


if __name__ == '__main__':
    # Load the assessments
    assessments = load_assessments('assessments_batch.json')

    # Print commands for Claude to execute
    print_assessment_commands(assessments, batch_size=5)

    # Print move commands for later
    # generate_move_commands(assessments)

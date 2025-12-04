#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process all students in a WorkSubmissions folder to extract and update self-grades.

Usage:
    python process_assignment.py --assignment-dir <path> --assignment-name <name> --output-report <path>
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from extract_self_grade import SelfGradeExtractor

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if hasattr(sys.stderr, 'encoding') and sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class AssignmentProcessor:
    """Process all students in an assignment folder."""

    def __init__(self, assignment_dir, assignment_name):
        """Initialize processor."""
        self.assignment_dir = Path(assignment_dir)
        self.assignment_name = assignment_name
        self.results = []
        self.stats = {
            'total_students': 0,
            'grades_found': 0,
            'grades_missing': 0,
            'excel_updated': 0,
            'errors': 0
        }

    def find_participant_folders(self):
        """
        Find all Participant_* folders in assignment directory.

        Returns:
            List of Path objects
        """
        folders = []
        for item in self.assignment_dir.iterdir():
            if item.is_dir() and item.name.startswith('Participant_'):
                folders.append(item)

        # Sort by participant ID
        def get_id(folder):
            import re
            match = re.search(r'Participant_(\d+)', folder.name)
            return int(match.group(1)) if match else 0

        folders.sort(key=get_id)
        return folders

    def process_all_students(self):
        """Process all students in the assignment."""
        participant_folders = self.find_participant_folders()
        self.stats['total_students'] = len(participant_folders)

        print(f"\n{'='*80}")
        print(f"Processing {self.assignment_name}")
        print(f"Found {len(participant_folders)} student folders")
        print(f"{'='*80}\n")

        for idx, folder in enumerate(participant_folders, 1):
            print(f"[{idx}/{len(participant_folders)}] Processing {folder.name}...")

            try:
                extractor = SelfGradeExtractor(folder)
                result = extractor.process()
                self.results.append(result)

                # Update stats
                if result['self_grade_extracted'] is not None:
                    self.stats['grades_found'] += 1
                else:
                    self.stats['grades_missing'] += 1

                if result['excel_updated']:
                    self.stats['excel_updated'] += 1

                if result['error']:
                    self.stats['errors'] += 1
                    print(f"  [WARNING] {result['error']}")
                else:
                    print(f"  [OK] Grade: {result['self_grade_extracted']}, Updated: {result['excel_updated']}")

            except Exception as e:
                print(f"  [ERROR] Unexpected error: {e}")
                self.stats['errors'] += 1
                self.results.append({
                    'participant_id': folder.name,
                    'folder': str(folder),
                    'error': str(e),
                    'excel_updated': False
                })

        print(f"\n{'='*80}")
        self._print_summary()
        print(f"{'='*80}\n")

    def _print_summary(self):
        """Print processing summary."""
        print("\nPROCESSING SUMMARY:")
        print(f"  Total Students: {self.stats['total_students']}")
        print(f"  Grades Found: {self.stats['grades_found']}")
        print(f"  Grades Missing: {self.stats['grades_missing']}")
        print(f"  Excel Updated: {self.stats['excel_updated']}")
        print(f"  Errors: {self.stats['errors']}")
        print(f"  Success Rate: {self.stats['grades_found']/max(1, self.stats['total_students'])*100:.1f}%")

    def generate_grade_distribution(self):
        """Calculate grade distribution."""
        distribution = {}
        for result in self.results:
            grade = result.get('self_grade_extracted')
            if grade is not None:
                distribution[grade] = distribution.get(grade, 0) + 1

        return distribution

    def generate_report(self, output_path):
        """Generate JSON report."""
        # Separate successful and failed extractions
        successful = [r for r in self.results if r.get('self_grade_extracted') is not None]
        failed = [r for r in self.results if r.get('self_grade_extracted') is None]

        report = {
            'skill': 'submission-info-updater',
            'assignment': self.assignment_name,
            'assignment_dir': str(self.assignment_dir),
            'processed_date': datetime.now().isoformat(),
            'total_students': self.stats['total_students'],
            'grades_found': self.stats['grades_found'],
            'grades_missing': self.stats['grades_missing'],
            'excel_updated': self.stats['excel_updated'],
            'errors': self.stats['errors'],
            'success_rate': f"{self.stats['grades_found']/max(1, self.stats['total_students'])*100:.1f}%",
            'students_processed': successful,
            'failed_extractions': failed,
            'grade_distribution': self.generate_grade_distribution(),
            'needs_manual_review': [
                {
                    'participant_id': r['participant_id'],
                    'reason': r.get('error', 'Unknown'),
                    'folder': r['folder']
                }
                for r in failed
            ]
        }

        # Save report
        output_path = Path(output_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Report saved to: {output_path}")

        # Also print students needing manual review
        if report['needs_manual_review']:
            print(f"\n[MANUAL REVIEW NEEDED] ({len(report['needs_manual_review'])} students):")
            for student in report['needs_manual_review']:
                print(f"  - Participant {student['participant_id']}: {student['reason']}")

        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract self-grades from student submissions and update Excel files'
    )
    parser.add_argument(
        '--assignment-dir',
        required=True,
        help='Path to WorkSubmissions folder (e.g., WorkSubmissions01)'
    )
    parser.add_argument(
        '--assignment-name',
        required=True,
        help='Assignment name (e.g., "Assignment 1")'
    )
    parser.add_argument(
        '--output-report',
        required=True,
        help='Path to save JSON report (e.g., submission_grades_report_hw1.json)'
    )

    args = parser.parse_args()

    # Validate assignment directory exists
    if not os.path.isdir(args.assignment_dir):
        print(f"Error: Assignment directory not found: {args.assignment_dir}")
        sys.exit(1)

    # Process assignment
    processor = AssignmentProcessor(args.assignment_dir, args.assignment_name)
    processor.process_all_students()

    # Generate report
    report = processor.generate_report(args.output_report)

    # Exit code based on success rate
    success_rate = processor.stats['grades_found'] / max(1, processor.stats['total_students'])
    if success_rate >= 0.95:
        print("\n[SUCCESS] Excellent! >95% success rate")
        sys.exit(0)
    elif success_rate >= 0.80:
        print("\n[WARNING] Good, but some manual review needed")
        sys.exit(0)
    else:
        print("\n[ERROR] Many failures - check errors")
        sys.exit(1)


if __name__ == '__main__':
    main()

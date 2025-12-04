#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate comprehensive summary report from all assignment reports."""

import json
import sys
from pathlib import Path

def main():
    """Generate summary report."""
    print('\n' + '='*80)
    print('COMPREHENSIVE GRADE EXTRACTION REPORT')
    print('='*80 + '\n')

    assignments = [
        ('submission_grades_report_hw1.json', 'Assignment 1'),
        ('submission_grades_report_hw2.json', 'Assignment 2'),
        ('submission_grades_report_hw3.json', 'Assignment 3'),
    ]

    total_students = 0
    total_found = 0
    all_manual_review = []

    for report_file, name in assignments:
        try:
            with open(report_file, encoding='utf-8') as f:
                data = json.load(f)

            print(f'{name}:')
            print(f'  Total Students: {data["total_students"]}')
            print(f'  Grades Found: {data["grades_found"]}')
            print(f'  Success Rate: {data["success_rate"]}')

            total_students += data['total_students']
            total_found += data['grades_found']

            dist = data['grade_distribution']
            if dist:
                grades = sorted([int(k) for k in dist.keys()])
                print(f'  Grade Range: {min(grades)} - {max(grades)}')
                most_common_grade = max(dist, key=dist.get)
                print(f'  Most Common: {most_common_grade} ({dist[most_common_grade]} students)')

            if data.get('needs_manual_review'):
                print(f'  Manual Review Needed: {len(data["needs_manual_review"])} students')
                all_manual_review.extend([
                    (name, s['participant_id'], s['reason'])
                    for s in data['needs_manual_review']
                ])

            print()

        except FileNotFoundError:
            print(f'{name}: Report not found\n')
        except Exception as e:
            print(f'{name}: Error reading report - {e}\n')

    print('='*80)
    print('OVERALL RESULTS:')
    print(f'  Total Students: {total_students}')
    print(f'  Total Grades Found: {total_found}')
    if total_students > 0:
        print(f'  Overall Success Rate: {total_found/total_students*100:.1f}%')
    print(f'  Manual Reviews Needed: {total_students - total_found}')
    print('='*80)

    if all_manual_review:
        print('\nSTUDENTS REQUIRING MANUAL REVIEW:')
        print('-'*80)
        for assignment, student_id, reason in all_manual_review:
            print(f'  {assignment} - Student {student_id}: {reason}')
        print('-'*80)

    print('\n[OK] Summary generation complete\n')


if __name__ == '__main__':
    main()

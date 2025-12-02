#!/usr/bin/env python3
"""
PDF Merger - Combine student submission PDFs with grade report PDFs

This script is for testing/standalone use. The main skill runs via Claude CLI.
"""
import os
import re
from pathlib import Path

try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("ERROR: PyPDF2 not installed. Run: pip install PyPDF2")
    exit(1)

def find_student_folders(submissions_dir):
    """Find all student submission folders."""
    folders = {}

    submissions_path = Path(submissions_dir)
    if not submissions_path.exists():
        print(f"ERROR: Submissions directory not found: {submissions_dir}")
        return folders

    for participant_dir in submissions_path.glob("Participant_*"):
        if not participant_dir.is_dir():
            continue

        # Extract student ID
        match = re.search(r"Participant_(\d+)", participant_dir.name)
        if match:
            student_id = match.group(1)
            folders[student_id] = str(participant_dir)

    return folders

def find_pdfs(student_folder):
    """
    Find submission PDF and grade report PDF in student folder.
    Returns: (submission_pdf, grade_report_pdf) or (None, None) if not found
    """
    folder_path = Path(student_folder)

    submission_pdf = None
    grade_report_pdf = None

    for pdf_file in folder_path.glob("*.pdf"):
        if "Student_Grade_Report" in pdf_file.name:
            grade_report_pdf = str(pdf_file)
        else:
            # This is the submission PDF
            submission_pdf = str(pdf_file)

    return submission_pdf, grade_report_pdf

def merge_pdfs(submission_pdf, grade_report_pdf, output_path):
    """
    Merge two PDFs into one.
    Returns: (success, page_count, error_message)
    """
    try:
        merger = PdfMerger()

        # Add submission first
        merger.append(submission_pdf)
        submission_pages = len(merger.pages)

        # Add grade report second
        merger.append(grade_report_pdf)
        total_pages = len(merger.pages)
        grade_report_pages = total_pages - submission_pages

        # Write combined PDF
        merger.write(output_path)
        merger.close()

        return True, (submission_pages, grade_report_pages, total_pages), None

    except Exception as e:
        return False, None, str(e)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Merge student submission PDFs with grade report PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge all students
  python merge_pdfs.py --submissions WorkSubmissions01

  # Merge specific student
  python merge_pdfs.py --submissions WorkSubmissions01 --student-id 38950
        """
    )

    parser.add_argument('--submissions', required=True, help='Path to submissions directory')
    parser.add_argument('--student-id', help='Specific student ID to process (optional)')
    parser.add_argument('--output-dir', help='Output directory (default: same as input)')

    args = parser.parse_args()

    print("=" * 60)
    print("PDF MERGER")
    print("=" * 60)

    # Find student folders
    print(f"\n[SCAN] Looking for students in: {args.submissions}")
    student_folders = find_student_folders(args.submissions)
    print(f"[OK] Found {len(student_folders)} student folders")

    # Filter to specific student if requested
    if args.student_id:
        if args.student_id in student_folders:
            student_folders = {args.student_id: student_folders[args.student_id]}
            print(f"[OK] Processing only student {args.student_id}")
        else:
            print(f"[ERROR] Student {args.student_id} not found")
            return 1

    # Statistics
    stats = {
        'processed': 0,
        'successful': 0,
        'failed': 0,
        'results': []
    }

    print(f"\n[MERGE] Processing {len(student_folders)} students...")
    print("-" * 60)

    # Process each student
    for student_id, folder in sorted(student_folders.items()):
        # Find PDFs
        submission_pdf, grade_report_pdf = find_pdfs(folder)

        if not submission_pdf:
            print(f"[FAIL] Student {student_id}: Missing submission PDF")
            stats['failed'] += 1
            stats['results'].append({
                'student_id': student_id,
                'success': False,
                'reason': 'Missing submission PDF'
            })
            continue

        if not grade_report_pdf:
            print(f"[FAIL] Student {student_id}: Missing grade report PDF")
            stats['failed'] += 1
            stats['results'].append({
                'student_id': student_id,
                'success': False,
                'reason': 'Missing grade report PDF'
            })
            continue

        # Determine output path
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = Path(folder)

        output_path = output_dir / f"Student_{student_id}_Complete_Submission.pdf"

        # Merge PDFs
        success, page_info, error = merge_pdfs(submission_pdf, grade_report_pdf, str(output_path))

        if success:
            sub_pages, report_pages, total_pages = page_info
            print(f"[OK] Student {student_id}: {sub_pages} pages + {report_pages} pages = {total_pages} pages total")
            stats['successful'] += 1
            stats['results'].append({
                'student_id': student_id,
                'success': True,
                'pages': page_info,
                'output': str(output_path)
            })
        else:
            print(f"[FAIL] Student {student_id}: {error}")
            stats['failed'] += 1
            stats['results'].append({
                'student_id': student_id,
                'success': False,
                'reason': error
            })

        stats['processed'] += 1

    # Print summary
    print("\n" + "=" * 60)
    print("PDF MERGE SUMMARY")
    print("=" * 60)
    print(f"\nStudents Processed: {stats['processed']}")
    print(f"Successful Merges: {stats['successful']} ({stats['successful']/stats['processed']*100:.1f}%)")
    print(f"Failed Merges: {stats['failed']} ({stats['failed']/stats['processed']*100:.1f}%)")

    if args.output_dir:
        print(f"\nOutput Location: {args.output_dir}")
    else:
        print(f"\nOutput Location: Same directory as originals")

    # Show failures if any
    if stats['failed'] > 0:
        print(f"\nFailed:")
        for result in stats['results']:
            if not result['success']:
                print(f"  [FAIL] Student {result['student_id']}: {result['reason']}")

    print("\n" + "=" * 60)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

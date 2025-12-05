#!/usr/bin/env python3
"""
Clean up old Complete_Submission PDFs and create new merged PDFs
with the Detailed_Feedback_Report and submission PDFs.
"""
import os
from pathlib import Path
from PyPDF2 import PdfMerger

def cleanup_and_merge_reports(submissions_dir):
    """
    1. Delete old Student_*_Complete_Submission.pdf files
    2. Find submission PDFs and Detailed_Feedback_Report PDFs
    3. Merge them into new Complete_Submission PDFs
    """

    submissions_path = Path(submissions_dir)
    if not submissions_path.exists():
        print(f"ERROR: Submissions directory not found: {submissions_dir}")
        return

    print("=" * 70)
    print("CLEANUP AND MERGE ASSIGNMENT 1 REPORTS")
    print("=" * 70)

    stats = {
        'folders_found': 0,
        'old_pdfs_deleted': 0,
        'merges_successful': 0,
        'merges_failed': 0,
        'missing_files': 0
    }

    # Process each student folder
    for participant_dir in sorted(submissions_path.glob("Participant_*_assignsubmission_file")):
        if not participant_dir.is_dir():
            continue

        stats['folders_found'] += 1

        # Extract student ID
        student_id = participant_dir.name.split("_")[1]

        print(f"\n[Student {student_id}]")

        # Step 1: Delete old Complete_Submission PDF
        old_complete_pdf = participant_dir / f"Student_{student_id}_Complete_Submission.pdf"
        if old_complete_pdf.exists():
            old_complete_pdf.unlink()
            stats['old_pdfs_deleted'] += 1
            print(f"  - Deleted old: Student_{student_id}_Complete_Submission.pdf")

        # Step 2: Find the submission PDF and detailed feedback report
        submission_pdf = None
        detailed_report = participant_dir / f"Detailed_Feedback_Report_{student_id}.pdf"

        # Find submission PDF (various possible names)
        possible_submission_names = [
            f"submission_form.pdf",
            f"submission.pdf",
            f"Assignment_1_Cover_Page.pdf",
            f"Assignment 1 - Cover Page.pdf"
        ]

        for pdf_file in participant_dir.glob("*.pdf"):
            # Skip if it's the detailed report or old complete submission
            if "Detailed_Feedback_Report" in pdf_file.name:
                continue
            if "Complete_Submission" in pdf_file.name:
                continue
            if "Grade_Report" in pdf_file.name:
                continue
            if "Detailed_Grade_Breakdown" in pdf_file.name:
                continue

            # This should be the submission PDF
            submission_pdf = pdf_file
            break

        # Step 3: Verify both files exist
        if not submission_pdf or not submission_pdf.exists():
            print(f"  [SKIP] Missing submission PDF")
            stats['missing_files'] += 1
            continue

        if not detailed_report.exists():
            print(f"  [SKIP] Missing Detailed_Feedback_Report_{student_id}.pdf")
            stats['missing_files'] += 1
            continue

        # Step 4: Merge PDFs (Detailed Report FIRST, then Submission)
        output_path = participant_dir / f"Student_{student_id}_Complete_Submission.pdf"

        try:
            merger = PdfMerger()

            # Add detailed feedback report FIRST
            merger.append(str(detailed_report))
            report_pages = len(merger.pages)

            # Add submission PDF SECOND
            merger.append(str(submission_pdf))
            total_pages = len(merger.pages)
            submission_pages = total_pages - report_pages

            # Write merged PDF
            merger.write(str(output_path))
            merger.close()

            print(f"  [OK] Merged: {report_pages} report pages + {submission_pages} submission pages = {total_pages} total")
            print(f"       Output: Student_{student_id}_Complete_Submission.pdf")
            stats['merges_successful'] += 1

        except Exception as e:
            print(f"  [FAIL] Merge error: {e}")
            stats['merges_failed'] += 1

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Student folders found: {stats['folders_found']}")
    print(f"Old Complete_Submission PDFs deleted: {stats['old_pdfs_deleted']}")
    print(f"Successful merges: {stats['merges_successful']}")
    print(f"Failed merges: {stats['merges_failed']}")
    print(f"Missing files (skipped): {stats['missing_files']}")
    print("=" * 70)

    if stats['merges_successful'] == stats['folders_found']:
        print("\nSUCCESS: All reports merged successfully!")
    else:
        print(f"\nWARNING: {stats['folders_found'] - stats['merges_successful']} students not processed")

if __name__ == '__main__':
    cleanup_and_merge_reports("WorkSubmissions01")

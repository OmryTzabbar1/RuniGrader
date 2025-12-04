#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract self-submitted grades from student PDFs and update submission_info.xlsx

This script thoroughly searches for student submission PDFs, extracts their
self-submitted grade using multiple patterns, and updates their submission_info.xlsx.

Usage:
    python extract_self_grade.py <participant_folder_path>
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
import pandas as pd
import PyPDF2

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if hasattr(sys.stderr, 'encoding') and sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class SelfGradeExtractor:
    """Extract self-grades from student submission PDFs."""

    # PDF filename patterns to prioritize
    PDF_PRIORITY_PATTERNS = [
        r'hw1.*\.pdf$',
        r'submission_form\.pdf$',
        r'submission\.pdf$',
        r'hw.*\.pdf$',
        r'הגשת.*\.pdf$',  # Hebrew: "submission"
        r'.*\.pdf$'  # Any PDF as last resort
    ]

    # Grade extraction patterns (ordered by specificity)
    GRADE_PATTERNS = [
        # English patterns - explicit grade mentions
        r'grade\s+suggestion\s*:\s*(\d+)',
        r'suggested\s+grade\s*:\s*(\d+)',
        r'self[\s-]*grade\s*:\s*(\d+)',
        r'grade\s*:\s*(\d+)',
        r'my\s+grade\s*:\s*(\d+)',

        # Hebrew patterns - various grade mentions
        r'ציון\s*:\s*(\d+)',  # "grade:"
        r'הצעת\s+ציון\s*:\s*(\d+)',  # "grade suggestion:"
        r'ציון\s+עצמי\s*:?\s*(\d+)',  # "self grade:" with optional colon
        r'ציון\s*עצמי\s*:?\s*(\d+)',  # "self grade" no space
        r'עצמי\s*:?\s*(\d+)',  # "self:" or "self" followed by number
        r'הציון\s+העצמי\s+שלי\s*:?\s*(\d+)',  # "my self grade"

        # Numbered list patterns (items 5-6 typically have the grade)
        r'(?:5\.|5\))\s*[^0-9]*?(\d+)',  # Item 5 in a list
        r'(?:6\.|6\))\s*[^0-9]*?(\d+)',  # Item 6 in a list

        # Fraction patterns (e.g., "95/100")
        r'(\d+)\s*/\s*100',  # X/100 format
    ]

    # Valid grade range
    MIN_GRADE = 60
    MAX_GRADE = 100

    def __init__(self, participant_folder):
        """Initialize extractor with participant folder path."""
        self.folder = Path(participant_folder)
        self.participant_id = self._extract_participant_id()

    def _extract_participant_id(self):
        """Extract participant ID from folder name."""
        match = re.search(r'Participant_(\d+)', self.folder.name)
        if match:
            return match.group(1)
        return "unknown"

    def find_submission_pdf(self):
        """
        Find the student's original submission PDF.

        Returns:
            Path to PDF or None if not found
        """
        # Exclude generated PDFs
        exclude_patterns = [
            'Detailed_Grade_Breakdown',
            'Student_Grade_Report',
            'Student_.*_Complete_Submission',
        ]

        # Find all PDFs
        all_pdfs = []
        for pdf in self.folder.rglob('*.pdf'):
            # Skip if in excluded directories
            if any(ex in str(pdf) for ex in ['node_modules', '.git', '__pycache__']):
                continue

            # Skip generated PDFs
            if any(re.search(pattern, pdf.name) for pattern in exclude_patterns):
                continue

            all_pdfs.append(pdf)

        if not all_pdfs:
            return None

        # Sort by priority
        def get_priority(pdf_path):
            """Lower number = higher priority."""
            for idx, pattern in enumerate(self.PDF_PRIORITY_PATTERNS):
                if re.search(pattern, pdf_path.name, re.IGNORECASE):
                    # Prefer PDFs in root folder over subdirectories
                    depth = len(pdf_path.relative_to(self.folder).parts)
                    return (idx, depth)
            return (999, 999)

        all_pdfs.sort(key=get_priority)
        return all_pdfs[0]

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from all pages of PDF.

        Returns:
            String with all text content
        """
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text_parts = []

                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    text_parts.append(text)

                return '\n'.join(text_parts)

        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def extract_grade_from_text(self, text):
        """
        Extract grade from text using multiple patterns.

        Returns:
            Integer grade or None if not found
        """
        # Clean text (normalize whitespace)
        text = re.sub(r'\s+', ' ', text)

        # Try each pattern
        for pattern in self.GRADE_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)

            for match in matches:
                try:
                    grade = int(match.group(1))

                    # Validate range
                    if self.MIN_GRADE <= grade <= self.MAX_GRADE:
                        return grade

                except (ValueError, IndexError):
                    continue

        # Last resort: Look for common grade values
        # First try in first 500 chars with context
        first_part = text[:500]
        common_grades = [100, 95, 90, 85, 80, 75, 70, 65, 60]

        for grade in common_grades:
            # Look for standalone number (not part of ID)
            pattern = rf'\b{grade}\b'
            if re.search(pattern, first_part):
                try:
                    # Check if it's near grade-related keywords
                    grade_str = str(grade)
                    if grade_str in text:
                        context = text[max(0, text.index(grade_str) - 50):
                                      text.index(grade_str) + 50]

                        if any(keyword in context.lower() for keyword in
                              ['grade', 'ציון', 'suggestion', 'הצעה', 'עצמי']):
                            return grade
                except ValueError:
                    continue

        # Ultimate fallback: If only one valid grade number found in entire text
        # Extract all numbers in valid range
        all_numbers = re.findall(r'\b(\d+)\b', text)
        valid_grades = [int(n) for n in all_numbers
                       if n.isdigit() and self.MIN_GRADE <= int(n) <= self.MAX_GRADE]

        # If exactly one valid grade found, use it
        if len(set(valid_grades)) == 1:
            return valid_grades[0]

        # If multiple valid grades, prefer the most common one in typical range (80-100)
        if valid_grades:
            from collections import Counter
            grade_counts = Counter(valid_grades)
            # Filter to likely self-grades (80-100 most common)
            likely_grades = [g for g in valid_grades if 80 <= g <= 100]
            if likely_grades:
                return Counter(likely_grades).most_common(1)[0][0]
            # Otherwise return most common valid grade
            return grade_counts.most_common(1)[0][0]

        return None

    def update_submission_info(self, grade):
        """
        Update submission_info.xlsx with extracted grade.

        Args:
            grade: Integer grade to store

        Returns:
            Boolean indicating success
        """
        excel_path = self.folder / 'submission_info.xlsx'

        if not excel_path.exists():
            print(f"Warning: submission_info.xlsx not found in {self.folder}")
            return False

        try:
            # Read Excel
            df = pd.read_excel(excel_path)

            # The "Suggested Grade" should be in row with Field="Suggested Grade"
            # Update the Value column for that row
            mask = df['Field'] == 'Suggested Grade'
            if mask.any():
                df.loc[mask, 'Value'] = grade
            else:
                # If row doesn't exist, add it
                new_row = pd.DataFrame({
                    'Field': ['Suggested Grade'],
                    'Value': [grade],
                    'Suggested Grade': [None]
                })
                df = pd.concat([df, new_row], ignore_index=True)

            # Save updated Excel
            df.to_excel(excel_path, index=False)
            print(f"[OK] Updated submission_info.xlsx with grade: {grade}")
            return True

        except Exception as e:
            print(f"Error updating Excel: {e}")
            return False

    def process(self):
        """
        Main processing pipeline.

        Returns:
            Dictionary with results
        """
        result = {
            'participant_id': self.participant_id,
            'folder': str(self.folder),
            'pdf_found': None,
            'self_grade_extracted': None,
            'excel_updated': False,
            'error': None,
            'notes': []
        }

        # Step 1: Find PDF
        pdf_path = self.find_submission_pdf()
        if not pdf_path:
            result['error'] = "No submission PDF found"
            result['notes'].append("Searched entire folder, no eligible PDFs")
            return result

        result['pdf_found'] = pdf_path.name
        result['notes'].append(f"Found PDF: {pdf_path.relative_to(self.folder)}")

        # Step 2: Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text or len(text) < 10:
            result['error'] = "Could not extract text from PDF"
            return result

        result['notes'].append(f"Extracted {len(text)} characters of text")

        # Step 3: Extract grade
        grade = self.extract_grade_from_text(text)
        if grade is None:
            result['error'] = "Could not find grade in PDF text"
            result['notes'].append("Tried all extraction patterns, no valid grade found")
            result['notes'].append(f"First 200 chars: {text[:200]}")
            return result

        result['self_grade_extracted'] = grade
        result['notes'].append(f"Extracted grade: {grade}")

        # Step 4: Update Excel
        success = self.update_submission_info(grade)
        result['excel_updated'] = success

        if success:
            result['notes'].append("Successfully updated submission_info.xlsx")

        return result


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python extract_self_grade.py <participant_folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a directory")
        sys.exit(1)

    # Process folder
    extractor = SelfGradeExtractor(folder_path)
    result = extractor.process()

    # Print results (handle encoding safely)
    try:
        print(f"\n{'='*60}")
        print(f"Participant ID: {result['participant_id']}")
        print(f"PDF Found: {result['pdf_found']}")
        print(f"Self-Grade: {result['self_grade_extracted']}")
        print(f"Excel Updated: {result['excel_updated']}")

        if result['error']:
            print(f"Error: {result['error']}")

        print(f"\nNotes:")
        for note in result['notes']:
            # Replace problematic characters for safe printing
            safe_note = note.encode('ascii', 'replace').decode('ascii')
            print(f"  - {safe_note}")

        print(f"{'='*60}\n")
    except UnicodeEncodeError:
        # Fallback to basic output if encoding fails
        print("\n" + "="*60)
        print(f"Participant ID: {result['participant_id']}")
        print(f"PDF Found: {result.get('pdf_found', 'N/A')}")
        print(f"Self-Grade: {result.get('self_grade_extracted', 'N/A')}")
        print(f"Excel Updated: {result.get('excel_updated', False)}")
        print("="*60 + "\n")

    # Exit code: 0 if successful, 1 if error
    sys.exit(0 if result['excel_updated'] else 1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Transfer weighted grades and key weaknesses from Excel to CSV.

Maps data from Assignment1_Grading_Summary.xlsx to work1-runi-grade-format.csv:
- Weighted Grade → ציונים column
- Key Weaknesses → הערות למשוב column
"""
import openpyxl
import csv
import re

def extract_student_id(identifier):
    """Extract numeric student ID from various formats."""
    # Handle formats like "38950", "משתתף:38950", "Participant_38950"
    match = re.search(r'(\d{5})', str(identifier))
    if match:
        return match.group(1)
    return None

def main():
    print("=" * 70)
    print("TRANSFER GRADES AND WEAKNESSES TO CSV")
    print("=" * 70)

    # Read Excel file
    print("\n[1] Reading Assignment1_Grading_Summary.xlsx...")
    wb = openpyxl.load_workbook("Assignment1_Grading_Summary.xlsx")
    ws = wb.active

    # Build mapping from student ID to data
    # Columns: 1=Student ID, 8=Weighted Grade, 11=Key Weaknesses
    excel_data = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        student_id = str(row[0]).strip()
        weighted_grade = row[7]  # Column 8 (0-indexed)
        key_weaknesses = row[10] if row[10] else ""  # Column 11

        excel_data[student_id] = {
            'weighted_grade': weighted_grade,
            'key_weaknesses': key_weaknesses
        }

    wb.close()
    print(f"   Loaded {len(excel_data)} students from Excel")

    # Read CSV file
    print("\n[2] Reading work1-runi-grade-format.csv...")
    csv_filename = "work1-runi-grade-format.csv"

    with open(csv_filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)

    print(f"   Loaded {len(rows)} rows from CSV")

    # Identify columns
    headers = rows[0]
    print(f"\n[3] Identifying columns...")

    # Find column indices
    id_col = headers.index('מספר מזהה')
    grade_col = headers.index('ציונים')
    feedback_col = headers.index('הערות למשוב')

    print(f"\n[4] Transferring data...")
    updates = 0
    missing = []

    for i in range(1, len(rows)):  # Skip header
        row = rows[i]
        csv_student_id = extract_student_id(row[id_col])

        if csv_student_id and csv_student_id in excel_data:
            # Update grade
            row[grade_col] = str(excel_data[csv_student_id]['weighted_grade'])
            # Update feedback
            row[feedback_col] = excel_data[csv_student_id]['key_weaknesses']
            updates += 1
            print(f"   [OK] Student {csv_student_id}: Grade={excel_data[csv_student_id]['weighted_grade']}")
        else:
            missing.append(csv_student_id if csv_student_id else row[id_col])

    print(f"\n[5] Writing updated CSV...")
    with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"   [OK] Saved {csv_filename}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total students in Excel: {len(excel_data)}")
    print(f"Students updated in CSV: {updates}")
    print(f"Students not found: {len(missing)}")

    if missing:
        print(f"\nMissing student IDs:")
        for sid in missing[:10]:
            print(f"  - {sid}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()

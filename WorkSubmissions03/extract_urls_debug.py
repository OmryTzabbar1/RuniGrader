import openpyxl

# Just check one file first
pid = '63690'
xlsx_path = f'Participant_{pid}_assignsubmission_file/submission_info.xlsx'

print(f"Checking {xlsx_path}...")
wb = openpyxl.load_workbook(xlsx_path)
ws = wb.active

print("\nAll cell values:")
for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    if i > 20:  # Only show first 20 rows
        break
    print(f"Row {i}: {row}")

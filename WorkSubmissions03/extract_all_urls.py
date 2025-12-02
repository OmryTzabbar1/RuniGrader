import openpyxl

participants = ['63690', '63696', '63698', '63700', '63701', '63707', '63709', '63718']

for pid in participants:
    xlsx_path = f'Participant_{pid}_assignsubmission_file/submission_info.xlsx'
    try:
        wb = openpyxl.load_workbook(xlsx_path)
        ws = wb.active

        # Look for row with "GitHub Repository" label
        github_info = None
        for row in ws.iter_rows(values_only=True):
            if row[0] == 'GitHub Repository':
                github_info = row[1]
                break

        print(f'{pid}|{github_info if github_info else "NONE"}')
    except Exception as e:
        print(f'{pid}|ERROR: {str(e)}')

import openpyxl

participants = ['63690', '63696', '63698', '63700', '63701', '63707', '63709', '63718']

for pid in participants:
    xlsx_path = f'Participant_{pid}_assignsubmission_file/submission_info.xlsx'
    try:
        wb = openpyxl.load_workbook(xlsx_path)
        ws = wb.active
        github_url = None
        for row in ws.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    val = str(cell.value).strip()
                    if 'github.com' in val and val != 'GitHub Repository':
                        github_url = val
                        break
            if github_url:
                break
        print(f'{pid}|{github_url if github_url else "NONE"}')
    except Exception as e:
        print(f'{pid}|ERROR: {str(e)}')

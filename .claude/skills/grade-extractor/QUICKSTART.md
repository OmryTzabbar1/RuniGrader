# Quick Start Guide - Grade Extractor Skill

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required package:
   ```bash
   pip install openpyxl
   ```

## Basic Usage

### Option 1: Use with Claude Code Agent (Recommended)

Simply ask Claude Code to extract grades:

```
Extract grades from WorkSubmissions01 and save to grades_hw1.xlsx
```

The agent will:
- Scan all submission folders
- Read each PDF
- Extract the 5 required fields
- Create a formatted Excel file
- Report progress and any issues

### Option 2: Manual Step-by-Step

#### Step 1: Create the Excel structure
```bash
python .claude/skills/grade-extractor/extract_grades.py WorkSubmissions01 grades.xlsx
```

This creates:
- `grades.xlsx` - Excel file with headers and participant IDs
- `grades_submissions.json` - List of all PDFs to process

#### Step 2: Process each PDF manually
For each submission, extract the 5 fields and run:
```bash
python .claude/skills/grade-extractor/update_excel.py grades.xlsx <participant_id> "<group_code>" "<student1>" "<student2>" "<github_url>" "<grade>"
```

Example:
```bash
python .claude/skills/grade-extractor/update_excel.py grades.xlsx 38950 "roeiandguy" "Roei Bracha 208933325" "Guy Bilitski 2087332532" "https://github.com/Roei-Bracha/ollama-chat-hw" "100"
```

## What Gets Extracted

The skill extracts these 5 fields from each PDF:

1. **Group Code** - The team/group name
2. **Student 1** - First student name and ID (9-digit UID)
3. **Student 2** - Second student name and ID (optional)
4. **GitHub Repository** - Full URL to the project repo
5. **Suggested Grade** - Number between 0-100

## Expected PDF Format

PDFs should contain the information in a numbered list format:

```
1. Group code: <name>
2. Student one: <First Last UID>
3. Student two: <First Last UID>
4. Repo link <URL>
5. Grade suggestion: <number>
```

The skill also handles:
- Form-style layouts
- Hebrew text (קוד קבוצה, הציון העצמי שלי)
- Variations like "Member A/B" instead of "Student one/two"
- Embedded hyperlinks

## Output

You'll get a professional Excel file with:
- Clean formatting and borders
- Proper column widths
- Frozen header row
- Clickable GitHub links
- All submission data organized

## Example Workflow

1. Students submit PDFs to `WorkSubmissions01/Participant_XXXXX_assignsubmission_file/`
2. Run: `Extract grades from WorkSubmissions01`
3. Claude Code reads all PDFs and extracts data
4. Get `student_grades.xlsx` with all information
5. Review and use for grading

## Troubleshooting

**No PDF found:** Some submission folders might be empty - the skill will skip them and report.

**Missing fields:** If a field can't be extracted, it's left empty in the Excel. Check the PDF manually.

**Hebrew text issues:** The skill handles Hebrew in PDFs for the grade field.

**Wrong data extracted:** The skill tries various patterns, but some PDFs might have unusual formatting. Review and manually correct if needed.

## Tips

- Process one folder at a time for better control
- Review the generated Excel file for completeness
- Keep the JSON file to track which PDFs were processed
- Use meaningful output filenames like `grades_hw1.xlsx`, `grades_hw2.xlsx`

## Need Help?

See the full documentation in `README.md` or `skill.md` for more details.

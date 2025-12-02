# Grade Extractor Skill

A Claude Code skill for extracting student submission information from PDFs and creating a structured Excel spreadsheet for grading.

## Overview

This skill automates the tedious process of manually extracting student information from assignment submission PDFs. It processes folders of student submissions and creates a well-formatted Excel file containing:

- Participant ID
- Group Code/Name
- Student 1 (Name and UID)
- Student 2 (Name and UID)
- GitHub Repository URL
- Suggested Grade
- PDF Filename

## Installation

1. The skill is already in `.claude/skills/grade-extractor/`
2. Install required Python package:
   ```bash
   pip install openpyxl
   ```

## Usage

### Using the Skill with Claude Code

Simply invoke the skill in a conversation with Claude Code:

```
Extract grades from WorkSubmissions01
```

Or be more specific:

```
Use the grade-extractor skill to process WorkSubmissions01 and create grades.xlsx
```

### Manual Usage

You can also run the scripts manually:

#### 1. Create Initial Excel Structure
```bash
python .claude/skills/grade-extractor/extract_grades.py WorkSubmissions01 output.xlsx
```

This will:
- Scan the submission folder
- Create an Excel file with headers
- Create a JSON file listing all submissions
- Populate Participant IDs and PDF filenames

#### 2. Update Individual Submissions
```bash
python .claude/skills/grade-extractor/update_excel.py output.xlsx 38950 "roeiandguy" "Roei Bracha 208933325" "Guy Bilitski 2087332532" "https://github.com/..." "100"
```

## Folder Structure

Your submission folders should follow this pattern:

```
WorkSubmissions01/
├── Participant_38950_assignsubmission_file/
│   └── hw1 llms agents.pdf
├── Participant_38951_assignsubmission_file/
│   └── submission_form.pdf
└── Participant_38952_assignsubmission_file/
    └── project.pdf
```

## PDF Format

Each PDF should contain these 5 elements (in any order, but typically numbered):

1. **Group Code**: The team/group identifier
2. **Student 1**: First student's name and ID
3. **Student 2**: Second student's name and ID (optional for solo work)
4. **GitHub Repository**: Link to the project repository
5. **Suggested Grade**: The grade the student(s) suggest (0-100)

### Example PDF Content

```
1. Group code: roeiandguy
2. Student one: Roei Bracha 208933325
3. Student two: Guy Bilitski 2087332532
4. Repo link https://github.com/Roei-Bracha/ollama-chat-hw
5. Grade suggestion: 100
```

The skill handles various formats including:
- Numbered lists (1., 2., 3., etc.)
- Form-style headers
- Mixed English and Hebrew text
- Embedded hyperlinks
- Variations in field names

## Output

The skill creates a professional Excel spreadsheet with:

- **Formatted headers** (blue background, white text)
- **Proper column widths** for readability
- **Clickable GitHub links**
- **Frozen header row** for easy scrolling
- **Text wrapping** for long content

### Example Output

| Participant ID | Group Code | Student 1 | Student 2 | GitHub Repository | Suggested Grade | PDF Filename |
|----------------|------------|-----------|-----------|-------------------|-----------------|--------------|
| 38950 | roeiandguy | Roei Bracha 208933325 | Guy Bilitski 2087332532 | https://github.com/Roei-Bracha/ollama-chat-hw | 100 | hw1 llms agents.pdf |
| 38951 | ron_itamar | ID 312544240 | ID 205949985 | https://github.com/RonKozitsa/LLM_course/... | 95 | submission_form.pdf |

## Features

- **Automatic PDF reading** using Claude Code's Read tool
- **Intelligent pattern matching** for various PDF formats
- **Handles edge cases**: solo submissions, missing fields, Hebrew text
- **Progress tracking** with TodoWrite tool
- **Error handling** and reporting
- **Professional formatting** in Excel output

## Troubleshooting

### Missing Dependencies
If you get an error about `openpyxl`, install it:
```bash
pip install openpyxl
```

### PDF Not Found
Ensure your submission folders contain PDF files. The skill looks for any `.pdf` file in each `Participant_*` folder.

### Missing Fields
If the skill can't extract a field, it will:
- Leave it empty in the Excel file
- Report it in the summary
- Continue processing other submissions

### Hebrew Text
The skill handles Hebrew text in PDFs, particularly for the suggested grade field which may appear as "הציון העצמי שלי".

## Advanced Usage

### Process Multiple Folders
You can process multiple submission folders by running the skill multiple times or modifying the scripts to accept multiple input folders.

### Custom Output Format
Modify `extract_grades.py` to customize the Excel output format, colors, or columns.

### Batch Processing
Create a batch script to process all WorkSubmissions folders at once.

## Files

- `prompt.md` - Skill instructions for Claude Code agent
- `skill.md` - Skill documentation
- `extract_grades.py` - Main script to scan submissions and create Excel structure
- `update_excel.py` - Script to update individual submission rows
- `requirements.txt` - Python dependencies
- `README.md` - This file

## License

This skill is part of your CoOp/Runi project and is for educational use.

## Support

If you encounter issues:
1. Check that PDFs follow the expected format
2. Ensure openpyxl is installed
3. Verify folder structure matches expected pattern
4. Review the skill's output for specific error messages

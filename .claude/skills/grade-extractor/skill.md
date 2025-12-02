# Grade Extractor Skill

Extract student submission information from PDFs and populate an Excel spreadsheet.

## What This Skill Does

This skill processes student assignment submissions stored in folders, where each student/group submits a PDF containing:

1. Group Code (name)
2. Student 1 (Format: First Name Last Name UID)
3. Student 2 (Format: First Name Last Name UID)
4. GitHub Repository (embedded link)
5. Suggested Grade (location varies, usually on first page)

The skill extracts this information and creates a structured Excel file for grading purposes.

## Usage

When invoked, you should:

1. Ask the user which submission folder(s) to process (WorkSubmissions01, WorkSubmissions02, etc.)
2. Ask for the output Excel filename
3. Process each PDF in the submission folders:
   - Use the Read tool to read each PDF
   - Extract the 5 required pieces of information
   - Populate the Excel file with the data

## Excel Output Format

The Excel file will contain these columns:

| Participant ID | Group Code | Student 1 | Student 2 | GitHub Repository | Suggested Grade | PDF Filename |
|---------------|------------|-----------|-----------|-------------------|-----------------|--------------|
| 38950 | roeiandguy | Roei Bracha 208933325 | Guy Bilitski 2087332532 | https://github.com/... | 100 | hw1 llms agents.pdf |

## Processing Steps

1. Scan the submission folder for all `Participant_*` directories
2. For each directory:
   - Extract the Participant ID from the folder name
   - Find the PDF file in the folder
   - Use the Read tool to read the PDF content
   - Extract the 5 required fields using pattern matching:
     - Look for numbered items (1., 2., 3., 4., 5.)
     - Look for keywords like "Group code:", "Student one:", "Repo link:", "Grade suggestion:"
     - Handle variations in formatting (some PDFs use "Member A/B", some use "Student one/two")
     - The suggested grade might be in English or Hebrew (הציון העצמי)
   - Write the extracted data to the Excel file
3. Save and report the output file location

## Example Patterns to Look For

### Pattern 1 (Simple format):
```
1. Group code: roeiandguy
2. Student one: Roei Bracha 208933325
3. Student two: Guy Bilitski 2087332532
4. Repo link https://github.com/Roei-Bracha/ollama-chat-hw
5. Grade suggestion: 100
```

### Pattern 2 (Form format):
```
1. Group Code: ron_itamar
2. Member A: ID 312544240
3. Member B: ID 205949985
4. GitHub Repository: https://github.com/RonKozitsa/LLM_course/tree/main/ollamachatbot-angular
הציון העצמי שלי 95/100:
```

## Important Notes

- The suggested grade is not always in the same location - search the entire first page if needed
- Some PDFs may have student names without UIDs, or UIDs on separate lines
- GitHub links may be embedded hyperlinks in the PDF
- Handle both English and Hebrew text
- Some students may submit alone (no Student 2)

## Error Handling

If any field cannot be found:
- Leave it empty in the Excel file
- Report which submissions had missing fields
- Continue processing other submissions

## Dependencies

This skill requires:
- openpyxl (for Excel file creation)
- Python 3.7+
- Access to the Read tool for PDF processing

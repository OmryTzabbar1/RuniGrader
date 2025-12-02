# Student Submission Grade Extractor

You are a specialized agent for extracting student submission information from PDF files and populating an Excel spreadsheet.

## Your Task

Process student assignment submissions where each student/group has submitted a PDF containing:

1. **Group Code** (group name)
2. **Student 1** (Format: First Name Last Name UID)
3. **Student 2** (Format: First Name Last Name UID) - may not exist for solo submissions
4. **GitHub Repository** (URL, may be embedded as hyperlink)
5. **Suggested Grade** (a number, usually on the first page but location varies)

## Step-by-Step Process

### Step 1: Initialize
- Ask the user which submission folder(s) to process (e.g., WorkSubmissions01, WorkSubmissions02, WorkSubmissions03)
- Ask for the desired output Excel filename (default: `student_grades.xlsx`)
- Confirm the working directory contains these folders

### Step 2: Scan Submissions
- Use the Glob or Bash tool to find all `Participant_*` folders in the specified submission directory
- Count how many submissions were found
- Report to the user

### Step 3: Create Excel File
- Install openpyxl if needed: `pip install openpyxl`
- Run the helper script to create the initial Excel structure:
  ```bash
  python .claude/skills/grade-extractor/extract_grades.py <submission_folder> <output_file>
  ```
- This creates an Excel file with headers and a JSON file listing all submissions

### Step 4: Extract Information from PDFs
For each submission in the JSON file:

1. **Read the PDF** using the Read tool with the path from the JSON
2. **Extract the 5 required fields** by looking for these patterns:

   **Group Code patterns:**
   - `1. Group code: <value>`
   - `Group Code: <value>`
   - `קוד קבוצה: <value>`
   - `Codegroupe: <value>`

   **Student 1 patterns:**
   - `2. Student one: <Name> <UID>`
   - `Member A: ID <UID>` (name may be elsewhere)
   - Format: First Last UID (9 digits)

   **Student 2 patterns:**
   - `3. Student two: <Name> <UID>`
   - `Member B: ID <UID>` (name may be elsewhere)
   - May be missing for solo submissions

   **GitHub Repository patterns:**
   - `4. Repo link <URL>`
   - `GitHub Repository: <URL>`
   - Look for `https://github.com/...` anywhere in the text
   - May be an embedded hyperlink

   **Suggested Grade patterns:**
   - `5. Grade suggestion: <number>`
   - `הציון העצמי שלי <number>/100`
   - `הציון העצמי שלי: <number>/100:`
   - Look on first page, search for any number near "grade", "הציון", "suggestion"
   - Usually a number between 0-100

3. **Handle variations:**
   - Some PDFs use numbered lists (1., 2., 3., 4., 5.)
   - Some use form-style headers
   - Some mix English and Hebrew
   - Student names might be on separate lines from UIDs
   - GitHub links might be embedded hyperlinks (look for the URL in the PDF text)

### Step 5: Update Excel File
- Use a Python script to update the Excel file with extracted data
- For each submission, populate all 5 fields
- If a field cannot be found, leave it empty and note it
- Make GitHub links clickable hyperlinks

### Step 6: Validate and Report
- Count how many submissions were processed
- Count how many had missing fields
- Report any errors or warnings
- Show the user the path to the completed Excel file

## Important Notes

- **The suggested grade location varies** - it might be:
  - On the first page in a numbered list
  - In a table or form
  - In Hebrew text
  - Search the entire first page if necessary

- **Handle missing data gracefully:**
  - Solo submissions won't have Student 2
  - Some fields might be hard to extract - do your best
  - Mark problematic submissions for manual review

- **Formatting:**
  - Keep the Excel file clean and professional
  - Use proper column widths
  - Make hyperlinks clickable
  - Apply borders and colors for readability

## Example Extraction

### PDF Content Example 1:
```
1. Group code: roeiandguy
2. Student one: Roei Bracha 208933325
3. Student two: Guy Bilitski 2087332532
4. Repo link https://github.com/Roei-Bracha/ollama-chat-hw
5. Grade suggestion: 100
```

**Extracted Data:**
- Group Code: `roeiandguy`
- Student 1: `Roei Bracha 208933325`
- Student 2: `Guy Bilitski 2087332532`
- GitHub: `https://github.com/Roei-Bracha/ollama-chat-hw`
- Grade: `100`

### PDF Content Example 2:
```
Group Code: ron_itamar
Member A: ID 312544240
Member B: ID 205949985
GitHub Repository: https://github.com/RonKozitsa/LLM_course/tree/main/ollamachatbot-angular
הציון העצמי שלי 95/100:
```

**Extracted Data:**
- Group Code: `ron_itamar`
- Student 1: `ID 312544240` (or extract name if found elsewhere)
- Student 2: `ID 205949985`
- GitHub: `https://github.com/RonKozitsa/LLM_course/tree/main/ollamachatbot-angular`
- Grade: `95`

## Error Handling

- If a PDF cannot be read, note it and continue
- If a field cannot be extracted, leave it empty
- At the end, report which submissions need manual review
- Save all partial progress to the Excel file

## Output

The final Excel file should have this structure:

| Participant ID | Group Code | Student 1 | Student 2 | GitHub Repository | Suggested Grade | PDF Filename |
|----------------|------------|-----------|-----------|-------------------|-----------------|--------------|
| 38950 | roeiandguy | Roei Bracha 208933325 | Guy Bilitski 2087332532 | https://github.com/Roei-Bracha/ollama-chat-hw | 100 | hw1 llms agents.pdf |
| 38951 | ron_itamar | ID 312544240 | ID 205949985 | https://github.com/RonKozitsa/... | 95 | submission_form.pdf |

## Tools You Should Use

1. **Bash** - to list directories, install packages
2. **Read** - to read PDF files
3. **Glob** - to find submission folders
4. **Edit or Write** - to update Excel file or create processing scripts
5. **TodoWrite** - to track progress through submissions

Be thorough, patient, and handle edge cases gracefully!

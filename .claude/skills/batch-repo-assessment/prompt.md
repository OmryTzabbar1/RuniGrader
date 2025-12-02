# Batch Repository Assessment Skill

You are helping to batch assess all student GitHub repositories using the `/git-repo-assessment` command.

## Context

The user has 36 student submissions, each with:
- A submission folder: `WorkSubmissions01/Participant_XXXXX_assignsubmission_file/`
- A GitHub repository URL extracted from their Excel file
- An existing `/git-repo-assessment` command that creates a markdown assessment file

## Your Task

1. **Load the assessment batch data** from `assessments_batch.json`

2. **Process repositories in batches of 5**:
   - For each repository in a batch:
     - Change to the student's folder: `cd <folder_path>`
     - Run: `/git-repo-assessment <github_url>`
     - This will create an assessment markdown file in the student's folder
     - Verify the file was created

3. **Track progress**:
   - Report after each batch completes (e.g., "Batch 1/8 complete: 5/36 repositories assessed")
   - Handle any errors gracefully
   - Continue with remaining repositories if one fails

4. **Important**:
   - EACH assessment markdown file MUST be saved in the INDIVIDUAL student's folder
   - The working directory should be the student's folder when calling the command
   - This ensures the output goes directly to the right location

5. **Final validation**:
   - After all batches, verify all 36 folders have the assessment markdown file
   - Report any missing assessments

## Expected Outcome

Each student folder will contain:
- `submission_info.xlsx` (already exists)
- `repo_assessment.md` or similar (created by git-repo-assessment command)
- The original PDF file

## Error Handling

- If a repository cannot be cloned, note it and continue
- If an assessment fails, record the error and proceed
- Provide a final summary of successes and failures

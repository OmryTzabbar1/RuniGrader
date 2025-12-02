#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch process all student submissions from PDFs to Excel
This script reads all PDFs and extracts the 5 required fields
"""

import re
import json
import sys

# Load the submissions JSON
with open('grades_hw1_submissions.json', 'r', encoding='utf-8') as f:
    submissions = json.load(f)

print(f"Processing {len(submissions)} submissions...\n")

# For each submission, output the commands needed
for idx, sub in enumerate(submissions, 1):
    participant_id = sub['participant_id']
    pdf_path = sub['pdf_path']

    print(f"# Submission {idx}/{len(submissions)}: Participant {participant_id}")
    print(f"# PDF: {sub['pdf_filename']}")
    print(f"# Read the PDF and extract data, then run:")
    print(f'# python .claude/skills/grade-extractor/update_excel.py grades_hw1.xlsx {participant_id} "<group>" "<student1>" "<student2>" "<github>" "<grade>"')
    print()

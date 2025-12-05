#!/usr/bin/env python3
"""
Generate detailed feedback PDFs for Assignment 2 and Assignment 3
"""
import json
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_detailed_report(student_id, assessment_data, output_path, assignment_name):
    """Create a detailed feedback PDF report without showing grades."""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c5aa0',
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )

    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#4a4a4a',
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor='#333333',
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=16
    )

    # Extract data
    total_score = assessment_data.get('total_score', 0)
    tier = assessment_data.get('performance_tier', 'Unknown')
    skills = assessment_data.get('skill_details', {})
    overall = assessment_data.get('overall_assessment', {})
    strengths_list = overall.get('strengths', [])
    weaknesses_list = overall.get('weaknesses', [])
    recommendations = assessment_data.get('recommended_actions', {})

    # Determine tone based on score
    if total_score >= 80:
        performance_level = "excellent"
        opening_tone = "very solid foundation"
    elif total_score >= 70:
        performance_level = "good"
        opening_tone = "solid foundation"
    elif total_score >= 55:
        performance_level = "developing"
        opening_tone = "good foundation with significant room for growth"
    else:
        performance_level = "needs improvement"
        opening_tone = "foundation that shows potential but requires substantial development"

    # Title
    story.append(Paragraph(f"{assignment_name} - Detailed Feedback Report", title_style))
    story.append(Paragraph(f"Student ID: {student_id}", ParagraphStyle(
        'StudentID',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        textColor='#666666',
        spaceAfter=20
    )))

    story.append(Spacer(1, 0.2*inch))

    # Introduction
    story.append(Paragraph("Assessment Overview", heading_style))

    if performance_level == "excellent":
        intro_text = f"""Your submission demonstrates a {opening_tone} in software engineering
        practices and LLM application development. You have successfully implemented most of the advanced
        requirements with only minor areas for enhancement. Your work shows strong attention to detail,
        comprehensive documentation, and professional development practices."""
    elif performance_level == "good":
        intro_text = f"""Your submission demonstrates a {opening_tone} in software engineering
        practices and LLM application development. You have successfully addressed the core requirements
        with some areas identified for enhancement. With focused improvements in the areas outlined below,
        you can elevate your work to an excellent standard."""
    elif performance_level == "developing":
        intro_text = f"""Your submission demonstrates a {opening_tone}. You have addressed several
        core requirements, and there is significant potential to elevate your work. The areas identified
        below represent opportunities for substantial improvement that will strengthen your software
        engineering practices and LLM application development skills."""
    else:
        intro_text = f"""Your submission demonstrates a {opening_tone}. While there are fundamental
        elements in place, there are multiple critical areas requiring attention. You have substantial
        potential to improve, and the recommendations below outline a clear path forward to strengthen
        your software engineering practices and meet the assignment requirements."""

    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 0.3*inch))

    # Strengths section
    if strengths_list and strengths_list[0] != "No skills with excellent scores (8+/10)":
        story.append(Paragraph("Areas of Excellence", heading_style))

        strength_text = "Your submission demonstrates particular strength in the following areas:"
        story.append(Paragraph(strength_text, body_style))
        story.append(Spacer(1, 0.1*inch))

        for strength in strengths_list:
            if '(' in strength:
                skill_name = strength.split('(')[0].strip()
                skill_key = skill_name.lower().replace(' ', '_')
                skill_detail = skills.get(skill_key, {})
                notes = skill_detail.get('notes', [])

                story.append(Paragraph(f"<b>{skill_name}</b>", subheading_style))

                if notes:
                    for note in notes[:3]:
                        story.append(Paragraph(f"• {note}", body_style))
                else:
                    story.append(Paragraph(f"• Excellent implementation of {skill_name.lower()} requirements", body_style))

                story.append(Spacer(1, 0.1*inch))

    # Areas for improvement
    story.append(Paragraph("Areas for Improvement and Development", heading_style))

    if performance_level in ["excellent", "good"]:
        improvement_intro = """While your submission is strong overall, the following areas present
        opportunities for minor enhancements that would further strengthen your work:"""
    else:
        improvement_intro = """The following areas require focused attention and development.
        Addressing these will significantly strengthen your software engineering practices and
        overall project quality:"""

    story.append(Paragraph(improvement_intro, body_style))
    story.append(Spacer(1, 0.15*inch))

    # Process weaknesses or skills needing improvement
    skills_to_improve = []

    if weaknesses_list and weaknesses_list[0] != "No critical weaknesses (<5/10)":
        for weakness in weaknesses_list:
            if '(' in weakness:
                skill_name = weakness.split('(')[0].strip()
                score_text = weakness.split('(')[1].replace(')', '')
                skills_to_improve.append((skill_name, score_text))
    else:
        # Find skills with room for improvement (score < 8)
        for skill_key, skill_data in skills.items():
            score = skill_data.get('score', 0)
            if score < 8:
                skill_name = skill_key.replace('_', ' ').title()
                skills_to_improve.append((skill_name, f"{score}/10"))

    # Detail each skill needing improvement
    for skill_name, score_text in skills_to_improve[:6]:
        skill_key = skill_name.lower().replace(' ', '_')
        skill_detail = skills.get(skill_key, {})
        recommendations_list = skill_detail.get('recommendations', [])
        notes = skill_detail.get('notes', [])

        story.append(Paragraph(f"<b>{skill_name}</b>", subheading_style))

        # Add context from notes if available
        if notes and len(notes) > 0:
            context_note = notes[0] if not notes[0].startswith("Found") else (notes[1] if len(notes) > 1 else None)
            if context_note:
                story.append(Paragraph(f"Current Status: {context_note}", body_style))

        # Add recommendations
        if recommendations_list:
            story.append(Paragraph("Recommended Actions:", body_style))
            for rec in recommendations_list[:4]:
                clean_rec = rec.split('(+')[0].strip()
                if clean_rec:
                    story.append(Paragraph(f"• {clean_rec}", body_style))

        story.append(Spacer(1, 0.15*inch))

    # Priority actions
    story.append(PageBreak())
    story.append(Paragraph("Priority Action Items", heading_style))

    immediate_actions = recommendations.get('immediate', [])
    high_priority = recommendations.get('high_priority', [])

    if immediate_actions and immediate_actions[0] != "All critical areas addressed - focus on optimization":
        story.append(Paragraph("<b>Immediate Focus Areas:</b>", subheading_style))
        story.append(Paragraph("""These items require your immediate attention as they represent
        critical gaps in the current submission:""", body_style))

        for action in immediate_actions[:5]:
            clean_action = action.split('(')[0].strip()
            story.append(Paragraph(f"• {clean_action}", body_style))

        story.append(Spacer(1, 0.2*inch))

    if high_priority and high_priority[0] != "Maintain current standards across all skills":
        story.append(Paragraph("<b>High Priority Enhancements:</b>", subheading_style))
        story.append(Paragraph("""These areas would significantly strengthen your submission
        and should be addressed after the immediate focus items:""", body_style))

        for action in high_priority[:5]:
            clean_action = action.split('(')[0].strip()
            story.append(Paragraph(f"• {clean_action}", body_style))

        story.append(Spacer(1, 0.2*inch))

    # Closing remarks
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Conclusion", heading_style))

    if performance_level == "excellent":
        closing = """Your submission demonstrates excellence in software engineering and LLM application
        development. The minor enhancements suggested above will help you maintain and further develop
        your already strong skills. Continue to build on this solid foundation, and focus on the advanced
        aspects that distinguish exceptional work from good work."""
    elif performance_level == "good":
        closing = """Your submission shows strong competency in software engineering and LLM application
        development. By addressing the areas outlined above, particularly the priority items, you can
        elevate your work to an excellent standard. You have demonstrated the foundational skills needed;
        now focus on deepening and broadening your implementation of professional practices."""
    elif performance_level == "developing":
        closing = """Your submission shows good potential and a developing understanding of software
        engineering principles. The areas identified above represent clear opportunities for growth.
        Focus on the immediate priority items first, then systematically work through the other
        recommendations. With dedicated effort on these areas, you can significantly strengthen your
        skills and project quality."""
    else:
        closing = """Your submission demonstrates potential, but requires substantial development in
        multiple critical areas. Focus first on the immediate priority items, which address fundamental
        requirements. Work systematically through each area, seeking examples and best practices.
        Remember that software engineering is a skill that develops through practice and iteration.
        Use this feedback as a roadmap for improvement."""

    story.append(Paragraph(closing, body_style))

    # Footer
    story.append(Spacer(1, 0.4*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor='#666666',
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"Assessment Date: {assessment_data.get('assessment_date', 'N/A')}", footer_style))
    story.append(Paragraph("This report provides developmental feedback to support your learning and growth.", footer_style))

    # Build PDF
    doc.build(story)
    return True

def generate_reports_for_assignment(assignment_num):
    """Generate reports for a specific assignment"""

    assessments_dir = Path(f"assessments_tier2_assignment{assignment_num}")
    submissions_dir = Path(f"WorkSubmissions0{assignment_num}")

    if not assessments_dir.exists():
        print(f"ERROR: {assessments_dir} not found")
        return 0

    if not submissions_dir.exists():
        print(f"ERROR: {submissions_dir} not found")
        return 0

    print(f"\n{'='*80}")
    print(f"GENERATING ASSIGNMENT {assignment_num} DETAILED FEEDBACK REPORTS")
    print(f"{'='*80}\n")

    report_count = 0

    for json_file in sorted(assessments_dir.glob("tier2_assessment_*.json")):
        student_id = json_file.stem.replace("tier2_assessment_", "")

        # Read assessment
        with open(json_file, 'r', encoding='utf-8') as f:
            assessment_data = json.load(f)

        # Find student folder
        student_folder = submissions_dir / f"Participant_{student_id}_assignsubmission_file"

        if student_folder.exists():
            output_path = student_folder / f"Detailed_Feedback_Report_{student_id}.pdf"

            try:
                create_detailed_report(student_id, assessment_data, str(output_path), f"Assignment {assignment_num}")
                print(f"Generated report for student {student_id}")
                report_count += 1
            except Exception as e:
                print(f"Error generating report for {student_id}: {e}")
        else:
            print(f"Warning: Folder not found for student {student_id}")

    print(f"\nCompleted Assignment {assignment_num}! Generated {report_count} detailed feedback reports.")
    return report_count

# Main execution
if __name__ == '__main__':
    total_reports = 0

    # Generate Assignment 2 reports
    total_reports += generate_reports_for_assignment(2)

    # Generate Assignment 3 reports
    total_reports += generate_reports_for_assignment(3)

    print(f"\n{'='*80}")
    print(f"OVERALL SUMMARY")
    print(f"{'='*80}")
    print(f"Total reports generated across all assignments: {total_reports}")
    print(f"{'='*80}")

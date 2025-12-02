#!/usr/bin/env python3
"""
Generate student-facing PDF grade reports with personalized feedback and emojis.
"""

import sys
import argparse
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def get_emoji_set(grade):
    """Return appropriate emojis based on grade level."""
    if grade >= 90:
        return {
            'celebration': '🎉',
            'star': '⭐',
            'trophy': '🏆',
            'fire': '🔥',
            'sparkles': '✨',
            'strong': '💪',
            'shine': '🌟',
            'rocket': '🚀',
            'check': '✅',
            'level': 'A-level'
        }
    elif grade >= 80:
        return {
            'check': '✅',
            'thumbsup': '👍',
            'lightbulb': '💡',
            'chart': '📈',
            'star': '⭐',
            'level': 'B-level'
        }
    elif grade >= 70:
        return {
            'check': '✓',
            'lightning': '⚡',
            'level': 'C-level'
        }
    elif grade >= 60:
        return {
            'check': '✓',
            'level': 'D-level'
        }
    else:
        return {
            'level': 'F-level'
        }

def get_feedback_tone(grade):
    """Return appropriate feedback tone based on grade."""
    if grade >= 90:
        return {
            'intro': 'Outstanding work',
            'transition': 'You demonstrated exceptional',
            'conclusion': 'Keep up the amazing work',
            'adjective': 'excellent'
        }
    elif grade >= 80:
        return {
            'intro': 'Great job',
            'transition': 'You showed strong',
            'conclusion': 'Keep up the good work',
            'adjective': 'strong'
        }
    elif grade >= 70:
        return {
            'intro': 'Good effort',
            'transition': 'You demonstrated solid',
            'conclusion': 'Continue improving',
            'adjective': 'good'
        }
    elif grade >= 60:
        return {
            'intro': 'You met the basic requirements',
            'transition': 'However, you need to focus on',
            'conclusion': 'Work on these areas for improvement',
            'adjective': 'adequate'
        }
    else:
        return {
            'intro': 'This submission requires significant improvement',
            'transition': 'You need to focus on',
            'conclusion': 'Please review the requirements and resubmit',
            'adjective': 'insufficient'
        }

def create_student_report(output_path, student_id, team, grade, repository, strengths, improvements, assignment="Assignment 3"):
    """Create student-facing PDF grade report."""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Get emojis and tone based on grade
    emojis = get_emoji_set(grade)
    tone = get_feedback_tone(grade)

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_LEFT,
        leading=16
    )

    # Title Page
    elements.append(Spacer(1, 0.5*inch))

    # Add celebratory emojis for high grades
    if grade >= 90:
        title_emojis = f"{emojis['celebration']} {emojis['trophy']} {emojis['star']}"
        elements.append(Paragraph(title_emojis, title_style))
        elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph(f"{assignment}", title_style))
    elements.append(Paragraph("Grade Report", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))

    # Student Info Box
    student_info = [
        ["Student ID:", student_id],
        ["Team:", team],
        ["Repository:", repository if repository else "N/A"],
        ["Assessment Date:", datetime.now().strftime("%B %d, %Y")],
    ]

    info_table = Table(student_info, colWidths=[2*inch, 4.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*inch))

    # Grade Box - Color coded
    if grade >= 90:
        grade_color = colors.HexColor('#27ae60')  # Green
        status_text = "EXCELLENT"
        grade_emoji = f"{emojis['trophy']} {emojis['star']}"
    elif grade >= 80:
        grade_color = colors.HexColor('#3498db')  # Blue
        status_text = "VERY GOOD"
        grade_emoji = emojis['check']
    elif grade >= 70:
        grade_color = colors.HexColor('#f39c12')  # Orange
        status_text = "GOOD"
        grade_emoji = emojis['check']
    elif grade >= 60:
        grade_color = colors.HexColor('#e67e22')  # Dark orange
        status_text = "PASS"
        grade_emoji = emojis['check']
    else:
        grade_color = colors.HexColor('#e74c3c')  # Red
        status_text = "NEEDS IMPROVEMENT"
        grade_emoji = ""

    grade_data = [
        [f"FINAL GRADE {grade_emoji}", f"{grade}%"],
        ["STATUS", status_text],
    ]

    grade_table = Table(grade_data, colWidths=[3.25*inch, 3.25*inch])
    grade_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), grade_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 16),
        ('FONTSIZE', (1, 0), (1, 0), 36),
        ('FONTSIZE', (0, 1), (-1, 1), 14),
        ('GRID', (0, 0), (-1, -1), 2, colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    elements.append(grade_table)

    elements.append(PageBreak())

    # Feedback Section
    if grade >= 90:
        feedback_title = f"{emojis['sparkles']} Your Outstanding Work {emojis['sparkles']}"
    elif grade >= 80:
        feedback_title = f"{emojis['star']} Your Strong Performance"
    elif grade >= 70:
        feedback_title = "Your Performance"
    else:
        feedback_title = "Assessment Feedback"

    elements.append(Paragraph(feedback_title, heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    # Opening paragraph
    if grade >= 90:
        opening = f"{tone['intro']}! {emojis['celebration']} {tone['transition']} technical skills and professional software engineering practices throughout this assignment. Your attention to detail and comprehensive approach set a high standard."
    elif grade >= 80:
        opening = f"{tone['intro']}! {tone['transition']} technical capabilities in this assignment. Your work demonstrates {tone['adjective']} understanding of software engineering principles."
    elif grade >= 70:
        opening = f"{tone['intro']}. {tone['transition']} foundation in software engineering. There are areas where you can strengthen your work to achieve higher marks."
    elif grade >= 60:
        opening = f"{tone['intro']}. {tone['transition']} improving your implementation, documentation, and testing practices to meet professional standards."
    else:
        opening = f"{tone['intro']}. {tone['transition']} fundamental software engineering practices including planning, documentation, testing, and version control."

    elements.append(Paragraph(opening, normal_style))
    elements.append(Spacer(1, 0.2*inch))

    # Strengths Section
    if strengths and len(strengths) > 0:
        if grade >= 90:
            strengths_title = f"{emojis['fire']} Key Strengths"
        elif grade >= 80:
            strengths_title = f"{emojis['thumbsup']} Key Strengths"
        elif grade >= 70:
            strengths_title = f"{emojis['check']} Strengths"
        else:
            strengths_title = "Strengths"

        elements.append(Paragraph(strengths_title, heading1_style))
        elements.append(Spacer(1, 0.1*inch))

        for strength in strengths:
            if grade >= 90:
                bullet = f"{emojis['star']} {strength}"
            elif grade >= 80:
                bullet = f"{emojis['check']} {strength}"
            elif grade >= 70:
                bullet = f"{emojis['check']} {strength}"
            else:
                bullet = f"• {strength}"
            elements.append(Paragraph(bullet, normal_style))

        elements.append(Spacer(1, 0.3*inch))

    # Areas for Improvement Section
    if improvements and len(improvements) > 0:
        if grade >= 90:
            improvements_title = f"{emojis['rocket']} To Reach Even Higher"
        elif grade >= 80:
            improvements_title = f"{emojis['lightbulb']} Areas for Improvement"
        elif grade >= 70:
            improvements_title = f"{emojis['lightning']} Areas Needing Attention"
        else:
            improvements_title = "Required Improvements"

        elements.append(Paragraph(improvements_title, heading1_style))
        elements.append(Spacer(1, 0.1*inch))

        for improvement in improvements:
            elements.append(Paragraph(f"• {improvement}", normal_style))

        elements.append(Spacer(1, 0.3*inch))

    # Closing paragraph
    if grade >= 90:
        closing = f"{emojis['strong']} {tone['conclusion']}! This submission demonstrates mastery of software engineering principles and would be competitive in a professional setting. {emojis['trophy']}"
    elif grade >= 80:
        closing = f"{tone['conclusion']}! With attention to the improvement areas noted above, you can reach the highest tier of performance."
    elif grade >= 70:
        closing = f"{tone['conclusion']}. Focus on the areas identified above to elevate your work to the next level."
    elif grade >= 60:
        closing = f"{tone['conclusion']}. Meeting these requirements will significantly improve your grade and professional readiness."
    else:
        closing = f"{tone['conclusion']}. Please review course materials and requirements carefully before your next submission."

    elements.append(Paragraph(closing, normal_style))

    elements.append(Spacer(1, 0.5*inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )

    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Assessed: {datetime.now().strftime('%B %d, %Y')}", footer_style))
    elements.append(Paragraph("This grade reflects your overall software engineering practices", footer_style))

    # Build PDF
    doc.build(elements)
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Generate student-facing grade report PDF')
    parser.add_argument('--student-id', required=True, help='Student ID')
    parser.add_argument('--team', required=True, help='Team name')
    parser.add_argument('--grade', required=True, type=int, help='Final grade (0-100)')
    parser.add_argument('--repository', default='', help='Repository name/URL')
    parser.add_argument('--output-dir', required=True, help='Output directory for PDF')
    parser.add_argument('--strengths', default='', help='Pipe-separated list of strengths')
    parser.add_argument('--improvements', default='', help='Pipe-separated list of improvements')
    parser.add_argument('--assignment', default='Assignment 3', help='Assignment name')

    args = parser.parse_args()

    # Parse strengths and improvements
    strengths = [s.strip() for s in args.strengths.split('|') if s.strip()] if args.strengths else []
    improvements = [i.strip() for i in args.improvements.split('|') if i.strip()] if args.improvements else []

    # Generate output filename
    output_filename = f"Student_Grade_Report_{args.student_id}.pdf"
    output_path = f"{args.output_dir}/{output_filename}"

    # Generate PDF
    create_student_report(
        output_path=output_path,
        student_id=args.student_id,
        team=args.team,
        grade=args.grade,
        repository=args.repository,
        strengths=strengths,
        improvements=improvements,
        assignment=args.assignment
    )

    print(f"[OK] Student grade report generated: {output_path}")
    print(f"     Grade: {args.grade}% - {'PASS' if args.grade >= 60 else 'FAIL'}")

if __name__ == '__main__':
    main()

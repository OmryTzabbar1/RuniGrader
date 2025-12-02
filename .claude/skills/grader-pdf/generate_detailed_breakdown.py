#!/usr/bin/env python3
"""
Generate detailed grade breakdown PDF from Tier 2 assessment JSON.
Shows exactly where students earned and lost points.
"""
import json
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


def create_detailed_grade_breakdown(assessment_json_path, output_pdf_path, assignment_name="Assignment"):
    """
    Generate comprehensive PDF grade breakdown from assessment JSON.

    Args:
        assessment_json_path: Path to tier2_assessment_<student_id>.json
        output_pdf_path: Where to save the PDF
        assignment_name: Name of the assignment (e.g., "Assignment 2")
    """
    # Load assessment data
    with open(assessment_json_path, 'r') as f:
        assessment = json.load(f)

    student_id = assessment['student_id']
    total_score = assessment['total_score']
    performance_tier = assessment['performance_tier']
    skills = assessment['skills']
    skill_details = assessment.get('skill_details', {})

    # Create PDF
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        leading=14
    )

    story = []

    # ===== PAGE 1: EXECUTIVE SUMMARY =====
    story.append(Paragraph(f"DETAILED GRADE BREAKDOWN", title_style))
    story.append(Paragraph(f"{assignment_name}", heading_style))
    story.append(Spacer(1, 0.2*inch))

    # Student info table
    info_data = [
        ['Student ID:', student_id],
        ['Repository:', assessment.get('repository_name', 'N/A')],
        ['Assessment Date:', assessment.get('assessment_date', 'N/A')],
    ]

    info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495e')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))

    # Overall score (large and prominent)
    score_text = f"<b>FINAL SCORE: {total_score:.1f} / 100</b>"
    score_para = Paragraph(score_text, ParagraphStyle(
        'ScoreStyle',
        parent=title_style,
        fontSize=24,
        textColor=get_score_color(total_score),
        alignment=TA_CENTER
    ))
    story.append(score_para)
    story.append(Spacer(1, 0.1*inch))

    # Performance tier
    tier_text = f"<b>Performance Tier: {performance_tier}</b>"
    tier_para = Paragraph(tier_text, ParagraphStyle(
        'TierStyle',
        parent=heading_style,
        fontSize=16,
        textColor=get_tier_color(performance_tier),
        alignment=TA_CENTER
    ))
    story.append(tier_para)
    story.append(Spacer(1, 0.3*inch))

    # Skills summary table
    story.append(Paragraph("Skills Summary", heading_style))

    skills_summary_data = [['Skill', 'Score', 'Status']]
    for skill_name, score in skills.items():
        display_name = skill_name.replace('_', ' ').title()
        status = get_status_text(score)
        skills_summary_data.append([
            display_name,
            f"{score}/10",
            status
        ])

    summary_table = Table(skills_summary_data, colWidths=[3.5*inch, 1.2*inch, 1.8*inch])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))

    # Add color coding to status column
    for i, (skill_name, score) in enumerate(skills.items(), start=1):
        summary_table.setStyle(TableStyle([
            ('TEXTCOLOR', (2, i), (2, i), get_score_color(score * 10))
        ]))

    story.append(summary_table)
    story.append(PageBreak())

    # ===== PAGES 2-11: DETAILED SKILL BREAKDOWNS =====
    skill_criteria = get_skill_criteria_definitions()

    for skill_name, score in skills.items():
        display_name = skill_name.replace('_', ' ').title()
        skill_detail = skill_details.get(skill_name, {})

        # Skill header
        skill_title = f"Skill: {display_name}"
        story.append(Paragraph(skill_title, title_style))

        score_text = f"<b>Score: {score}/10 points</b>"
        score_para = Paragraph(score_text, ParagraphStyle(
            'SkillScoreStyle',
            parent=heading_style,
            fontSize=16,
            textColor=get_score_color(score * 10),
            alignment=TA_CENTER
        ))
        story.append(score_para)

        status_text = f"Status: {get_status_text(score)}"
        story.append(Paragraph(status_text, body_style))
        story.append(Spacer(1, 0.2*inch))

        # Points breakdown table
        story.append(Paragraph("Points Breakdown", heading_style))

        criteria_list = skill_criteria.get(skill_name, [])
        breakdown_data = [['Criterion', 'Max Points', 'Earned', 'Status']]

        for criterion in criteria_list:
            crit_name = criterion['name']
            max_pts = criterion['points']
            earned_pts = get_earned_points(skill_detail, criterion, score)
            status_icon = '✓' if earned_pts >= max_pts else '✗'

            breakdown_data.append([
                crit_name,
                f"{max_pts:.1f}",
                f"{earned_pts:.1f}",
                status_icon
            ])

        breakdown_data.append(['TOTAL', '10.0', f"{score:.1f}", ''])

        breakdown_table = Table(breakdown_data, colWidths=[3.2*inch, 1.0*inch, 1.0*inch, 0.8*inch])
        breakdown_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#ecf0f1')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#bdc3c7')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 0.15*inch))

        # What was found
        notes = skill_detail.get('notes', [])
        if notes:
            story.append(Paragraph("What Was Found", subheading_style))
            for note in notes:
                if 'found' in note.lower() or 'exists' in note.lower() or '+' in note:
                    story.append(Paragraph(f"• {note}", body_style))
            story.append(Spacer(1, 0.1*inch))

        # What was missing
        story.append(Paragraph("What Was Missing", subheading_style))
        missing_items = []
        for note in notes:
            if 'not found' in note.lower() or 'no ' in note.lower() or '0 points' in note.lower():
                missing_items.append(note)

        if missing_items:
            for item in missing_items:
                story.append(Paragraph(f"• {item}", body_style))
        else:
            story.append(Paragraph("• All criteria met!", body_style))
        story.append(Spacer(1, 0.1*inch))

        # How to improve
        recommendations = skill_detail.get('recommendations', [])
        if recommendations:
            points_possible = 10 - score
            story.append(Paragraph(f"How to Improve (+{points_possible:.1f} points)", subheading_style))
            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", body_style))

        story.append(PageBreak())

    # ===== FINAL PAGE: OVERALL SUMMARY =====
    story.append(Paragraph("Overall Assessment Summary", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Key strengths
    strengths = [name for name, score in skills.items() if score >= 8]
    story.append(Paragraph("Key Strengths (8+ points)", heading_style))
    if strengths:
        for skill in strengths:
            display_name = skill.replace('_', ' ').title()
            story.append(Paragraph(f"• {display_name}: {skills[skill]}/10", body_style))
    else:
        story.append(Paragraph("• No skills scored 8 or above", body_style))
    story.append(Spacer(1, 0.15*inch))

    # Critical gaps
    gaps = [name for name, score in skills.items() if score < 5]
    story.append(Paragraph("Critical Gaps (<5 points)", heading_style))
    if gaps:
        for skill in gaps:
            display_name = skill.replace('_', ' ').title()
            story.append(Paragraph(f"• {display_name}: {skills[skill]}/10", body_style))
    else:
        story.append(Paragraph("• No critical gaps identified", body_style))
    story.append(Spacer(1, 0.15*inch))

    # Overall recommendations
    overall_rec = assessment.get('recommended_actions', {})
    if overall_rec:
        story.append(Paragraph("Recommended Actions", heading_style))

        immediate = overall_rec.get('immediate', [])
        if immediate:
            story.append(Paragraph("<b>Immediate Priority:</b>", subheading_style))
            for action in immediate:
                story.append(Paragraph(f"• {action}", body_style))

        high_priority = overall_rec.get('high_priority', [])
        if high_priority:
            story.append(Paragraph("<b>High Priority:</b>", subheading_style))
            for action in high_priority:
                story.append(Paragraph(f"• {action}", body_style))

    # Build PDF
    doc.build(story)
    return output_pdf_path


def get_score_color(score):
    """Return color based on score percentage."""
    if score >= 80:
        return colors.HexColor('#27ae60')  # Green
    elif score >= 55:
        return colors.HexColor('#f39c12')  # Orange
    else:
        return colors.HexColor('#e74c3c')  # Red


def get_tier_color(tier):
    """Return color based on performance tier."""
    tier_colors = {
        'Excellence': colors.HexColor('#27ae60'),
        'Good': colors.HexColor('#2ecc71'),
        'Potential': colors.HexColor('#f39c12'),
        'Below Standard': colors.HexColor('#e74c3c')
    }
    return tier_colors.get(tier, colors.black)


def get_status_text(score):
    """Return status text based on score."""
    if score >= 8:
        return "✓ Excellent"
    elif score >= 6:
        return "✓ Good"
    elif score >= 4:
        return "⚠ Fair"
    else:
        return "✗ Poor"


def get_skill_criteria_definitions():
    """Return detailed criteria breakdown for each skill."""
    return {
        'project_planning': [
            {'name': 'PRD.md exists', 'points': 2.0, 'key': 'prd_found'},
            {'name': 'ARCHITECTURE.md exists', 'points': 5.0, 'key': 'architecture_found'},
            {'name': 'Problem Statement', 'points': 1.0, 'key': 'has_problem'},
            {'name': 'Functional Requirements', 'points': 1.5, 'key': 'has_requirements'},
            {'name': 'Success Metrics', 'points': 0.5, 'key': 'has_metrics'}
        ],
        'code_documentation': [
            {'name': 'README.md >1KB', 'points': 3.0, 'key': 'readme_exists'},
            {'name': 'Installation instructions', 'points': 1.0, 'key': 'has_installation_instructions'},
            {'name': 'Usage examples', 'points': 1.0, 'key': 'has_usage_examples'},
            {'name': 'Code structure documented', 'points': 2.0, 'key': 'code_structure_documented'},
            {'name': 'Python docstrings (>50%)', 'points': 3.0, 'key': 'python_files_with_docstrings'}
        ],
        'config_security': [
            {'name': 'No hardcoded secrets (CRITICAL)', 'points': 5.0, 'key': 'hardcoded_secrets_found'},
            {'name': '.env.example exists', 'points': 2.0, 'key': 'env_example_exists'},
            {'name': '.gitignore exists', 'points': 1.0, 'key': 'gitignore_exists'},
            {'name': 'Uses environment variables', 'points': 2.0, 'key': 'uses_environment_variables'}
        ],
        'testing_quality': [
            {'name': 'Test files exist', 'points': 3.0, 'key': 'test_files_found'},
            {'name': 'Multiple test files (>3)', 'points': 2.0, 'key': 'multiple_tests'},
            {'name': 'Test framework configured', 'points': 2.0, 'key': 'test_framework_configured'},
            {'name': 'Test functions (>10)', 'points': 3.0, 'key': 'test_count'}
        ],
        'research_analysis': [
            {'name': 'Jupyter notebooks exist', 'points': 4.0, 'key': 'jupyter_notebooks_found'},
            {'name': 'Multiple notebooks (>2)', 'points': 2.0, 'key': 'multiple_notebooks'},
            {'name': 'Has visualizations/plots', 'points': 2.0, 'key': 'has_visualizations'},
            {'name': 'Analysis documentation', 'points': 2.0, 'key': 'analysis_docs'}
        ],
        'ui_ux': [
            {'name': 'Screenshots/images (1+)', 'points': 3.0, 'key': 'screenshots_found'},
            {'name': 'Screenshots/images (5+)', 'points': 3.0, 'key': 'many_screenshots'},
            {'name': 'UI documentation', 'points': 2.0, 'key': 'ui_documentation'},
            {'name': 'User guide exists', 'points': 2.0, 'key': 'user_guide_exists'}
        ],
        'version_management': [
            {'name': 'Git commits >10', 'points': 2.0, 'key': 'git_commits_count'},
            {'name': 'Meaningful commit messages', 'points': 2.0, 'key': 'has_meaningful_commits'},
            {'name': 'PROMPT_BOOK.md exists', 'points': 5.0, 'key': 'prompt_book_exists'},
            {'name': 'Branching strategy', 'points': 1.0, 'key': 'branching_documented'}
        ],
        'costs_pricing': [
            {'name': 'Cost analysis document', 'points': 5.0, 'key': 'cost_analysis_exists'},
            {'name': 'Cost mentions in docs', 'points': 3.0, 'key': 'cost_mentions'},
            {'name': 'Budget tracking', 'points': 2.0, 'key': 'budget_tracking'}
        ],
        'extensibility': [
            {'name': 'Plugin/extension system', 'points': 3.0, 'key': 'has_plugin_system'},
            {'name': 'Modular structure (3+ dirs)', 'points': 3.0, 'key': 'modular_structure'},
            {'name': 'Interfaces/APIs', 'points': 2.0, 'key': 'has_interfaces'},
            {'name': 'Extension documentation', 'points': 2.0, 'key': 'extension_docs'}
        ],
        'quality_standards': [
            {'name': 'Linting configuration', 'points': 2.0, 'key': 'linting_configured'},
            {'name': 'CI/CD pipeline', 'points': 3.0, 'key': 'ci_cd_pipeline'},
            {'name': 'Code style guide', 'points': 2.0, 'key': 'code_style_guide'},
            {'name': 'Pre-commit hooks', 'points': 2.0, 'key': 'precommit_hooks'},
            {'name': 'Project setup file', 'points': 1.0, 'key': 'has_project_setup'}
        ]
    }


def get_earned_points(skill_detail, criterion, total_score):
    """Calculate earned points for a specific criterion."""
    key = criterion.get('key')
    max_points = criterion['points']

    if key in skill_detail:
        value = skill_detail[key]

        # Boolean checks
        if isinstance(value, bool):
            # Special case: hardcoded_secrets_found (inverted logic)
            if key == 'hardcoded_secrets_found':
                return max_points if not value else 0
            return max_points if value else 0

        # Numeric checks
        if isinstance(value, (int, float)):
            if key == 'git_commits_count':
                return max_points if value > 10 else 0
            if key == 'test_files_found':
                return max_points if value > 0 else 0
            if key == 'jupyter_notebooks_found':
                return max_points if value > 0 else 0
            if key == 'screenshots_found':
                if criterion['name'] == 'Screenshots/images (5+)':
                    return max_points if value >= 5 else 0
                return max_points if value > 0 else 0

    # Proportional calculation as fallback
    return (total_score / 10.0) * max_points


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_detailed_breakdown.py <assessment_json_path> <output_pdf_path> [assignment_name]")
        sys.exit(1)

    assessment_json_path = sys.argv[1]
    output_pdf_path = sys.argv[2]
    assignment_name = sys.argv[3] if len(sys.argv) > 3 else "Assignment"

    try:
        result_path = create_detailed_grade_breakdown(
            assessment_json_path,
            output_pdf_path,
            assignment_name
        )
        print(f"[OK] Generated detailed grade breakdown: {result_path}")
        print(f"     File size: {Path(result_path).stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"[ERROR] Failed to generate breakdown: {e}")
        sys.exit(1)

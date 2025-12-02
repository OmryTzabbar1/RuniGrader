#!/usr/bin/env python3
"""
Single Student Weighted Grade Calculator

Quick tool to calculate weighted grade for a single student.
"""

import sys
import math
import argparse

# Constants
SCALE_COEFFICIENT_A = 0.086603
SCALE_EXPONENT_B = 0.027465
MIN_SELF_GRADE = 60
MAX_SELF_GRADE = 100


def calculate_scale(self_grade):
    """Calculate exponential scale multiplier."""
    return SCALE_COEFFICIENT_A * math.exp(SCALE_EXPONENT_B * self_grade)


def calculate_weighted_grade(self_grade, base_grade):
    """
    Calculate weighted grade with penalty for overconfidence.

    Args:
        self_grade: Student's claimed grade (60-100)
        base_grade: Actual grade earned (0-100)

    Returns:
        dict with calculation details
    """
    # Validate
    if not (MIN_SELF_GRADE <= self_grade <= MAX_SELF_GRADE):
        print(f"⚠️  Warning: Self-grade {self_grade} out of range [{MIN_SELF_GRADE}, {MAX_SELF_GRADE}]")
        self_grade = max(MIN_SELF_GRADE, min(MAX_SELF_GRADE, self_grade))

    # Calculate scale
    scale = calculate_scale(self_grade)

    # Calculate difference
    difference = self_grade - base_grade

    # Apply penalty
    if difference > 0:
        penalty = difference * scale
        weighted_grade = max(0, base_grade - penalty)
        status = "OVERCONFIDENT" if penalty > 5 else "SLIGHTLY OPTIMISTIC"
    else:
        penalty = 0
        weighted_grade = base_grade
        if difference < 0:
            status = "HUMBLE"
        else:
            status = "ACCURATE"

    return {
        'self_grade': self_grade,
        'base_grade': base_grade,
        'scale': scale,
        'difference': difference,
        'penalty': penalty,
        'weighted_grade': weighted_grade,
        'status': status
    }


def print_result(result):
    """Print calculation result in formatted way."""
    print("\n" + "="*60)
    print("+================================================+")
    print("|       WEIGHTED GRADE CALCULATION              |")
    print("+================================================+")
    print()

    print(f"Self-Proclaimed Grade:  {result['self_grade']}/100")
    print(f"Base Grade (Earned):    {result['base_grade']:.2f}/100")
    print(f"Difference:             {result['difference']:.2f} points")
    print()

    print(f"Scale Multiplier:       {result['scale']:.4f}")
    print(f"Penalty Applied:        {result['penalty']:.2f} points")
    print()

    print("+================================================+")
    print(f"|  WEIGHTED GRADE:  {result['weighted_grade']:6.2f}/100              |")
    print("+================================================+")
    print()

    # Status with emoji
    status_emoji = {
        'ACCURATE': '[OK]',
        'HUMBLE': '[STAR]',
        'SLIGHTLY OPTIMISTIC': '[WARN]',
        'OVERCONFIDENT': '[FAIL]'
    }

    emoji = status_emoji.get(result['status'], '')
    print(f"Assessment: {emoji} {result['status']}")

    if result['status'] == 'ACCURATE':
        print("-> Perfect self-awareness! No penalty applied.")
    elif result['status'] == 'HUMBLE':
        print(f"-> You underestimated by {abs(result['difference']):.1f} points - you earned more!")
    elif result['status'] == 'SLIGHTLY OPTIMISTIC':
        print(f"-> Small penalty for slight overconfidence.")
    else:
        print(f"-> Large penalty for significant overconfidence.")

    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Calculate weighted grade for a single student',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Perfect accuracy
  python calculate_single_weighted.py --self-grade 85 --base-grade 85

  # Humble student
  python calculate_single_weighted.py --self-grade 70 --base-grade 85

  # Overconfident student
  python calculate_single_weighted.py --self-grade 95 --base-grade 70
        """
    )

    parser.add_argument('--student-id', help='Student ID (optional, for display)')
    parser.add_argument('--self-grade', type=int, required=True,
                        help=f'Student self-proclaimed grade ({MIN_SELF_GRADE}-{MAX_SELF_GRADE})')
    parser.add_argument('--base-grade', type=float, required=True,
                        help='Base grade from Tier 2 assessment (0-100)')

    args = parser.parse_args()

    if args.student_id:
        print(f"\nCalculating for Student ID: {args.student_id}")

    result = calculate_weighted_grade(args.self_grade, args.base_grade)
    print_result(result)

    return 0


if __name__ == '__main__':
    sys.exit(main())

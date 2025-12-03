"""
Weighted Grade Calculator Module
Implements exponential self-grading penalty formula
"""
import math
import os
import re
from pathlib import Path
import pandas as pd


# Formula constants
SCALE_COEFFICIENT_A = 0.086603
SCALE_EXPONENT_B = 0.027465
MIN_SELF_GRADE = 60
MAX_SELF_GRADE = 100


def calculate_scale(self_grade: float) -> float:
    """Calculate the exponential scale multiplier."""
    return SCALE_COEFFICIENT_A * math.exp(SCALE_EXPONENT_B * self_grade)


def calculate_weighted_grade(self_grade: float, base_grade: float) -> tuple[float, float]:
    """
    Calculate weighted grade using exponential penalty formula.

    Args:
        self_grade: Student's self-proclaimed grade
        base_grade: Actual grade from Tier 2 assessment

    Returns:
        tuple: (weighted_grade, penalty)
    """
    # Clamp self_grade to valid range
    self_grade = max(MIN_SELF_GRADE, min(MAX_SELF_GRADE, self_grade))

    # Calculate scale
    scale = calculate_scale(self_grade)

    # Apply penalty only if overestimated
    if self_grade > base_grade:
        difference = self_grade - base_grade
        penalty = difference * scale
        weighted_grade = max(0, base_grade - penalty)
    else:
        # Reward humility - no penalty
        penalty = 0
        weighted_grade = base_grade

    return weighted_grade, penalty


def extract_self_grade_from_submission_info(submission_dir: Path) -> float | None:
    """
    Extract self-proclaimed grade from submission_info.xlsx.

    Args:
        submission_dir: Path to student's submission directory

    Returns:
        float: Self-grade if found, None otherwise
    """
    submission_info_path = submission_dir / "submission_info.xlsx"

    if not submission_info_path.exists():
        return None

    try:
        df = pd.read_excel(submission_info_path)

        # Look for "Suggested Grade" field
        suggested_grade_row = df[df['Field'] == 'Suggested Grade']

        if not suggested_grade_row.empty:
            self_grade = float(suggested_grade_row['Value'].iloc[0])
            # Clamp to valid range
            return max(MIN_SELF_GRADE, min(MAX_SELF_GRADE, self_grade))

        return None
    except Exception as e:
        print(f"Error extracting self-grade from {submission_info_path}: {e}")
        return None




def get_weighted_grade_for_student(
    student_id: str,
    base_grade: float,
    submissions_dir: str
) -> tuple[float, float, float | None]:
    """
    Calculate weighted grade for a student.

    Args:
        student_id: Student ID
        base_grade: Base grade from Tier 2 assessment
        submissions_dir: Directory containing student submissions

    Returns:
        tuple: (weighted_grade, penalty, self_grade)
    """
    # Find student submission directory
    submissions_path = Path(submissions_dir)
    student_dirs = list(submissions_path.glob(f"Participant_{student_id}_assignsubmission_file"))

    self_grade = None

    if student_dirs:
        student_dir = student_dirs[0]
        self_grade = extract_self_grade_from_submission_info(student_dir)

    # If no self-grade found, use base grade (no penalty)
    if self_grade is None:
        self_grade = base_grade

    weighted_grade, penalty = calculate_weighted_grade(self_grade, base_grade)

    return weighted_grade, penalty, self_grade


if __name__ == "__main__":
    # Test the calculator
    print("Testing Weighted Grade Calculator")
    print("=" * 50)

    test_cases = [
        (85, 85, "Accurate"),
        (70, 85, "Humble"),
        (95, 85, "Slightly Optimistic"),
        (100, 70, "Very Overconfident"),
        (90, 90, "Perfect Accuracy")
    ]

    for self_grade, base_grade, label in test_cases:
        weighted, penalty = calculate_weighted_grade(self_grade, base_grade)
        print(f"\n{label}:")
        print(f"  Self-Grade: {self_grade}")
        print(f"  Base Grade: {base_grade}")
        print(f"  Weighted Grade: {weighted:.2f}")
        print(f"  Penalty: {penalty:.2f}")

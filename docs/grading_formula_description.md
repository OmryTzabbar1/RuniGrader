# Exponential Self-Grading Formula

## Overview

This grading system adjusts a student's self-assigned grade based on how many requirements they actually met. It rewards accurate or humble self-assessment and penalizes overconfidence.

## The Formula

### Step 1: Calculate the Scale Multiplier

```
Scale = 0.086603 × e^(0.027465 × self_grade)
```

Where `self_grade` is the grade the student claims (60-100).

**Pre-calculated scale values:**
| Self-Grade | Scale |
|------------|-------|
| 60 | 0.45 |
| 65 | 0.52 |
| 70 | 0.59 |
| 75 | 0.68 |
| 80 | 0.78 |
| 85 | 0.89 |
| 90 | 1.03 |
| 95 | 1.18 |
| 100 | 1.35 |

### Step 2: Calculate the Base Grade

```
base_grade = (requirements_met / 22) × 100
```

Where `requirements_met` is the number of requirements the student actually satisfied (0-22).

### Step 3: Calculate the Final Grade

**If self_grade > base_grade (student overestimated):**
```
difference = self_grade - base_grade
penalty = difference × scale
final_grade = max(0, base_grade - penalty)
```

**If self_grade ≤ base_grade (student underestimated or was accurate):**
```
final_grade = base_grade
```

The student receives what they actually earned—no penalty for being humble.

## Implementation Example (Pseudocode)

```python
import math

def calculate_final_grade(self_grade, requirements_met):
    # Step 1: Calculate scale
    scale = 0.086603 * math.exp(0.027465 * self_grade)
    
    # Step 2: Calculate base grade
    base_grade = (requirements_met / 22) * 100
    
    # Step 3: Calculate final grade
    if self_grade > base_grade:
        difference = self_grade - base_grade
        penalty = difference * scale
        final_grade = max(0, base_grade - penalty)
    else:
        final_grade = base_grade
    
    return final_grade
```

## Key Behaviors

1. **Perfect accuracy is rewarded**: If a student claims 80 and meets exactly 17-18 requirements (base ≈ 77-82), they get their base grade.

2. **Underestimation is rewarded**: If a student claims 60 but meets 22/22 requirements, they get 100 (what they earned).

3. **Overestimation is penalized**: If a student claims 100 but only meets 18/22 requirements (base = 81.8), they receive 57.3. The penalty increases with the size of the overestimation.

4. **Higher claims = higher risk**: The scale multiplier increases exponentially with self-grade, so claiming 100 carries more risk than claiming 80.

## Example Calculations

| Self-Grade | Met | Base | Final | Explanation |
|------------|-----|------|-------|-------------|
| 100 | 22/22 | 100.0 | 100.0 | Accurate, no penalty |
| 100 | 21/22 | 95.5 | 89.3 | Slight overestimate, small penalty |
| 100 | 18/22 | 81.8 | 57.3 | Significant overestimate, large penalty |
| 60 | 22/22 | 100.0 | 100.0 | Underestimated, gets full earned grade |
| 80 | 18/22 | 81.8 | 81.8 | Underestimated slightly, gets earned grade |
| 90 | 18/22 | 81.8 | 73.4 | Overestimated by ~8 points, penalized |

## Constants Summary

- **Scale coefficient (a):** 0.086603
- **Scale exponent (b):** 0.027465
- **Total requirements:** 22
- **Valid self-grade range:** 60-100

---
name: 4-testing-quality
description: Evaluates unit tests, test coverage, edge case handling, and test automation. Use for Tier 2 testing quality assessment.
version: 2.0.0
---

# Skill 4: Testing & Quality

You are an autonomous agent that thoroughly evaluates testing practices and quality assurance.

**Your Mission:** Find and assess test files, test coverage, edge cases, and test automation, no matter where they're located in the repository.

**Scoring:** 10 points maximum
- Test Presence & Quality: 4 points
- Edge Case Testing: 3 points
- Test Coverage Configuration: 2 points
- Test Automation (CI/CD): 1 point

**Passing Threshold:** 7/10 (70%)

---

## Your Process

### Phase 1: Discovery (Find ALL test files)

**DO NOT assume standard locations!** Tests might be in tests/, test/, src/test/, or scattered throughout.

1. **Run the helper script first:**
```bash
python .claude/skills/4-testing-quality/analyze_tests.py <repo_path>
```

This will:
- Find ALL test files recursively (test_*.py, *_test.py, *.test.js, *.spec.js, *Test.java)
- Count test functions/methods in each file
- Count assertions
- Detect mocking/stubbing usage
- Find coverage configuration files
- Check if tests run in CI/CD

2. **Manual search if needed:**
```bash
# Find test files (Python)
find . -name "test_*.py" -o -name "*_test.py" | head -20

# Find test files (JavaScript/TypeScript)
find . -name "*.test.js" -o -name "*.test.ts" -o -name "*.spec.js" -o -name "*.spec.ts" | head -20

# Find test files (Java)
find . -name "*Test.java" -o -name "Test*.java" | head -20

# Find test directories
find . -type d -name "test" -o -name "tests" -o -name "__tests__" | head -10

# Count test functions
grep -r "def test_\|it(\|test(\|describe(" . --include="*.py" --include="*.js" --include="*.ts" | wc -l
```

3. **Read test files:**
```bash
# Use Read tool on sample test files
Read <test_file_path>
```

### Phase 2: Test Presence & Quality (4 points)

**Required Elements:**
1. Test files exist (minimum 3 files)
2. Adequate number of tests (minimum 10 test functions)
3. Tests have assertions
4. Tests use mocking where appropriate

**Scoring Logic:**
```
Start with 4 points

Test Files:
- No test files found: 0 points (STOP HERE)
- 1-2 test files: 1.0 point
- 3-5 test files: 2.0 points
- 6-10 test files: 3.0 points
- 10+ test files: 4.0 points (excellent)

Test Count:
- <5 tests: -1.0
- 5-9 tests: +0
- 10-19 tests: +0
- 20+ tests: +0.5 bonus

Test Quality:
- No assertions: -1.0 (tests without assertions are useless)
- Has mocking/stubbing: +0.5 bonus
- Tests are organized (in test directory): +0.5 bonus

Max: 4.5 points (capped at 4.0)
```

**Analyze Test Files:**
```bash
# Read sample test files to verify quality
Read <test_file_1>
Read <test_file_2>
```

Check for:
- Test functions follow naming convention (test_*, it(), @Test)
- Tests have assertions (assert, expect, assertEquals)
- Tests are meaningful (not just empty)
- Tests cover different scenarios

### Phase 3: Edge Case Testing (3 points)

**Check for edge case coverage:**

1. **Boundary testing:**
```bash
# Search for boundary-related tests
grep -ri "boundary\|edge\|limit\|max\|min\|empty\|zero" . --include="*test*.py" --include="*test*.js" | head -20
```

2. **Error/exception testing:**
```bash
# Python
grep -r "with pytest.raises\|assertRaises\|try.*except" . --include="*test*.py" | wc -l

# JavaScript
grep -r "expect.*toThrow\|expect.*throw\|catch" . --include="*test*.js" --include="*test*.ts" | wc -l

# Java
grep -r "@Test.*expected\|assertThrows" . --include="*Test.java" | wc -l
```

3. **Null/None/undefined handling:**
```bash
grep -ri "none\|null\|undefined\|nil" . --include="*test*" | wc -l
```

**Scoring Logic:**
```
Edge Case Testing Score:

Excellent (3.0 points):
- Tests boundary conditions (empty, max, min)
- Tests error/exception handling
- Tests null/None/undefined cases
- Has at least 5 edge case tests

Good (2.0 points):
- Tests some boundary conditions
- Some error handling tests
- 3-4 edge case tests

Adequate (1.0 point):
- Minimal edge case coverage
- 1-2 edge case tests

Poor (0 points):
- No edge case tests found
```

**Read test files to verify:**
```bash
Read <test_file_with_edge_cases>
```

### Phase 4: Test Coverage Configuration (2 points)

**Check for coverage tools:**

```bash
# Python coverage
find . -name "pytest.ini" -o -name ".coveragerc" -o -name "setup.cfg" -o -name "pyproject.toml"

# JavaScript coverage
find . -name "jest.config.js" -o -name "jest.config.ts" -o -name ".nycrc" -o -name "karma.conf.js"

# Java coverage
find . -name "jacoco.xml" -o -name "pom.xml" | xargs grep -l "jacoco" 2>/dev/null

# Coverage reports
find . -name "coverage.xml" -o -name "coverage.json" -o -path "*/htmlcov/*"
```

**Scoring:**
- Has coverage configuration: +2.0 points
- No coverage configuration: +0 points

**Read coverage config if found:**
```bash
Read <coverage_config_path>
```

Verify:
- Coverage tool is configured
- Minimum coverage threshold set (if specified)
- Coverage report generation enabled

### Phase 5: Test Automation (CI/CD) (1 point)

**Check if tests run automatically:**

```bash
# GitHub Actions
find . -path "*/.github/workflows/*.yml" -exec grep -l "pytest\|npm test\|mvn test\|gradle test" {} \;

# GitLab CI
find . -name ".gitlab-ci.yml" -exec grep -l "test" {} \;

# Travis CI
find . -name ".travis.yml" -exec grep -l "test" {} \;

# Circle CI
find . -path "*/.circleci/config.yml" -exec grep -l "test" {} \;
```

**Scoring:**
- Tests run in CI/CD: +1.0 point
- Tests configured but maybe not running: +0.5 points
- No CI/CD testing: +0 points

**Read CI config if found:**
```bash
Read .github/workflows/<workflow_file>
```

Verify tests actually run (not just CI exists).

---

## Scoring Summary

```
Total: 10 points maximum

Test Presence & Quality: 0-4 points
  - Test file count: 1-4 points
  - Test function count: bonus/penalty
  - Has assertions: required
  - Has mocking: bonus

Edge Case Testing: 0-3 points
  - Boundary tests: required
  - Error handling: required
  - Null/edge cases: required
  - Quality & coverage: 3+ points

Coverage Configuration: 0-2 points
  - pytest.ini, jest.config.js, etc.: 2 points
  - No coverage config: 0 points

Test Automation: 0-1 point
  - Tests in CI/CD: 1 point
  - No automation: 0 points

Total: Sum of all components (max 10.0)
```

---

## Output Format

```json
{
  "skill": "testing-quality",
  "score": 7.5,
  "max_score": 10.0,
  "passed": true,
  "files_found": {
    "test_files": ["tests/test_api.py", "tests/test_utils.py", "src/components/Button.test.js"],
    "coverage_config": ["pytest.ini", "jest.config.js"],
    "ci_files": [".github/workflows/test.yml"]
  },
  "test_presence": {
    "score": 3.5,
    "test_file_count": 8,
    "total_test_count": 34,
    "total_assertions": 67,
    "files_with_mocks": 3,
    "quality": "good"
  },
  "edge_case_testing": {
    "score": 2.5,
    "has_boundary_tests": true,
    "has_error_tests": true,
    "has_null_tests": true,
    "edge_case_count": 12,
    "quality": "good"
  },
  "coverage_config": {
    "score": 2.0,
    "has_config": true,
    "tools": ["pytest", "jest"],
    "config_files": ["pytest.ini", "jest.config.js"]
  },
  "test_automation": {
    "score": 1.0,
    "has_ci": true,
    "tests_run_in_ci": true,
    "ci_platform": "GitHub Actions"
  },
  "recommendations": [
    "Increase edge case coverage to 15+ tests",
    "Add integration tests",
    "Set coverage threshold to 80%"
  ]
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** only check tests/ directory
✅ **DO** search entire repository recursively

❌ **DON'T** assume test files follow Python naming convention
✅ **DO** check for JS (.test.js, .spec.js), Java (*Test.java), and others

❌ **DON'T** count empty test files as valid
✅ **DO** verify tests have actual test functions and assertions

❌ **DON'T** miss tests in src/__tests__/ or alongside source files
✅ **DO** search for test directories and co-located tests

❌ **DON'T** give points for tests without assertions
✅ **DO** verify tests actually assert something

❌ **DON'T** assume CI exists means tests run
✅ **DO** read CI config and verify test commands

---

## Example Execution

```bash
# Step 1: Run helper script
python .claude/skills/4-testing-quality/analyze_tests.py /path/to/repo

# Output shows:
# - 8 test files found
# - 34 total tests
# - 67 assertions
# - 3 files with mocks
# - pytest.ini found
# - GitHub Actions with tests

# Step 2: Manual verification
find /path/to/repo -name "*test*.py" | head -10
grep -r "def test_" /path/to/repo | wc -l

# Step 3: Read sample test files
Read /path/to/repo/tests/test_api.py
Read /path/to/repo/tests/test_edge_cases.py

# Step 4: Check for edge cases
grep -ri "boundary\|edge\|empty" /path/to/repo/tests/

# Step 5: Check coverage config
Read /path/to/repo/pytest.ini

# Step 6: Check CI
Read /path/to/repo/.github/workflows/test.yml

# Step 7: Calculate score
# Test files: 3.0 (8 files)
# Edge cases: 2.5 (good coverage)
# Coverage config: 2.0 (has pytest.ini)
# CI automation: 1.0 (tests run in GH Actions)
# Total: 8.5/10

# Step 8: Generate JSON output
```

---

## Tips for Accurate Assessment

1. **Test multiple languages** - Project may have Python, JS, and Java tests
2. **Check test quality** - Not just presence, but meaningful tests with assertions
3. **Verify edge cases** - Look for boundary, error, and null handling
4. **Read sample tests** - Verify they're real tests, not stubs
5. **Check CI config** - Tests existing ≠ tests running automatically
6. **Give partial credit** - 5 tests is better than 0 tests
7. **Look for test patterns** - Different frameworks use different conventions

**Edge Cases Matter:** Testing happy path only isn't enough - check for error handling!

**Success = Finding all tests that exist and assessing their quality fairly!**

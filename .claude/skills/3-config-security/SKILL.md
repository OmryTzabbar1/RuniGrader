---
name: 3-config-security
description: Evaluates configuration management and security practices. Detects hardcoded secrets and checks for proper env config. Use for Tier 2 security assessment.
version: 2.0.0
---

# Skill 3: Configuration & Security

You are an autonomous agent that performs thorough security and configuration assessment.

**Your Mission:** Detect hardcoded secrets and evaluate configuration management practices.

**Scoring:** 10 points maximum
- Hardcoded secrets/credentials: -2 points per instance (not auto-fail)
- Configuration management: 0-10 points based on best practices

---

## Your Process

### Phase 1: Secret Detection (-2 points per secret found)

**⚠️ Hardcoded secrets result in -2 points EACH (not auto-fail)**

1. **Run the advanced secret scanner:**
```bash
python .claude/skills/3-config-security/scan_secrets.py <repo_path>
```

This scans for:
- API keys (OpenAI, AWS, Google Cloud, generic)
- Hardcoded passwords
- Access tokens (GitHub, OAuth)
- Database credentials in URLs
- Any suspicious patterns

2. **Manual verification if scanner finds nothing:**

Check common locations:
```bash
# Search for API key patterns
grep -ri "api[_-]\?key\s*=" . --include="*.py" --include="*.js" --include="*.ts" --include="*.java" | head -20

# Search for OpenAI keys
grep -r "sk-[a-zA-Z0-9]\{20,\}" . --include="*.py" --include="*.js" --include="*.env" --include="*.txt"

# Search for AWS keys
grep -r "AKIA[0-9A-Z]\{16\}" . --include="*.py" --include="*.js" --include="*.java"

# Search for hardcoded passwords
grep -ri "password\s*=\s*[\"']" . --include="*.py" --include="*.js" --include="*.config" | grep -v "your_password\|password_here\|<password>"

# Search for database URLs with credentials
grep -r "://.*:.*@" . --include="*.py" --include="*.js" --include="*.properties"

# Check config files
find . -name "config.py" -o -name "config.js" -o -name "settings.py" -o -name "application.properties" | head -10
```

3. **Read suspicious config files:**
```bash
# Use Read tool on any config files found
Read <config_file_path>
```

Look for:
- Long strings that look like API keys (20+ characters)
- Patterns like `sk-...`, `AKIA...`, `AIza...`
- Hardcoded passwords or tokens
- Database connection strings with credentials

**⚠️ IMPORTANT:**
- Comments with secrets still count as hardcoded (-2 points each)
- Example/dummy keys like "your_api_key_here" or "sk-xxx" are OK (no deduction)
- Placeholder keys like "sk-ant-api03-YOUR-KEY-HERE" are OK (no deduction)
- Real keys (even if expired) result in -2 points each

**Scoring for Security:**
```
Start with 10 points

FOR EACH hardcoded secret found:
  Deduct 2 points

Minimum score: 0 (can't go below 0)

Example:
- 0 secrets found: Start with 10 points, proceed to Phase 2
- 1 secret found: -2 points, assess configuration (max 8/10)
- 3 secrets found: -6 points, assess configuration (max 4/10)
- 5+ secrets found: Likely 0/10 even with good config
```

### Phase 2: Configuration Management Assessment

**Assess regardless of secrets found (secrets just reduce max score)**

Check for proper configuration practices:

1. **Check for .env.example or env.example (2 points):**
```bash
find . -maxdepth 2 -name ".env.example" -o -name "env.example" -o -name ".env.sample" -o -name "example.env"
```

If found, READ IT:
```bash
Read <env_example_path>
```

Verify it:
- Contains variable names (API_KEY=, DATABASE_URL=, etc.)
- Does NOT contain real values (should be placeholders)
- Provides examples of what to set

**Scoring:**
- Has .env.example with good examples: +2 points
- Has .env.example but poor (empty or no examples): +1 point
- No .env.example: +0 points

2. **Check for .gitignore (1 point):**
```bash
find . -maxdepth 1 -name ".gitignore"
```

READ IT:
```bash
Read .gitignore
```

Verify:
- Contains `.env` entry (critical!)
- Contains other secret files (credentials.json, etc.)
- Ignores local config files

**Scoring:**
- Has .gitignore with .env ignored: +1 point
- Has .gitignore but missing .env: +0.5 points
- No .gitignore: +0 points

3. **Check for environment variable usage in code (2 points):**
```bash
# Python
grep -r "os\.getenv\|os\.environ" . --include="*.py" | wc -l

# JavaScript/TypeScript
grep -r "process\.env" . --include="*.js" --include="*.ts" | wc -l

# Java
grep -r "System\.getenv" . --include="*.java" | wc -l

# Show examples
grep -r "os\.getenv\|process\.env" . --include="*.py" --include="*.js" | head -5
```

**Scoring:**
- Uses environment variables extensively (10+ times): +2 points
- Uses environment variables moderately (3-9 times): +1.5 points
- Uses environment variables minimally (1-2 times): +0.5 points
- No environment variable usage: +0 points

### Phase 3: Additional Security Checks (Bonus)

Look for additional security measures:

1. **Check for dependency scanning:**
```bash
find . -name "requirements.txt" -o -name "package.json" -o -name "go.mod"
find . -path "*/.github/workflows/*" -name "*.yml" | xargs grep -l "security\|vulnerability" 2>/dev/null
```

2. **Check for security documentation:**
```bash
find . -name "SECURITY.md" -o -name "security.md"
grep -ri "security\|vulnerability\|disclosure" README.md docs/*.md 2>/dev/null
```

**Bonus points (max +0.5):**
- Has SECURITY.md: +0.3 points
- Has dependency scanning in CI: +0.2 points

---

## Scoring Summary

```
Total: 10 points maximum

Base Score Calculation:
  .env.example: 0-3 points
  .gitignore with .env: 0-2 points
  Environment variable usage: 0-3 points
  Security docs/tools: 0-2 points
  Total possible: 10 points

Deductions:
  -2 points per hardcoded secret found
  -1 point if .env not in .gitignore

Final Score:
  Max(0, Base Score - Deductions)

Examples:
  - Good config (9 pts) + 0 secrets = 9/10
  - Good config (9 pts) + 1 secret = 7/10 (9 - 2)
  - Poor config (4 pts) + 2 secrets = 0/10 (4 - 4)
  - Excellent config (10 pts) + 3 placeholder keys = 10/10 (placeholders don't count)
```

---

## Output Format

```json
{
  "skill": "config-security",
  "score": 7.5,
  "max_score": 10.0,
  "passed": true,
  "security_status": "PASS",
  "secret_scan": {
    "secrets_found": false,
    "files_scanned": 45,
    "suspicious_patterns": 0,
    "scan_details": "No hardcoded secrets detected"
  },
  "configuration": {
    "has_env_example": true,
    "env_example_quality": "good",
    "has_gitignore": true,
    "env_in_gitignore": true,
    "uses_environment_variables": true,
    "env_var_count": 15
  },
  "breakdown": {
    "security_baseline": 5.0,
    "env_example": 2.0,
    "gitignore": 1.0,
    "env_var_usage": 2.0,
    "bonus": 0.3
  },
  "issues": [],
  "recommendations": [
    "Add security policy documentation",
    "Consider adding dependency vulnerability scanning"
  ]
}
```

**If secrets found:**
```json
{
  "skill": "config-security",
  "score": 0.0,
  "max_score": 10.0,
  "passed": false,
  "security_status": "FAIL",
  "secret_scan": {
    "secrets_found": true,
    "files_scanned": 45,
    "suspicious_patterns": 3,
    "findings": [
      {
        "file": "src/config.py",
        "line": 12,
        "type": "OpenAI API Key",
        "severity": "CRITICAL",
        "matched": "sk-...masked..."
      },
      {
        "file": "backend/settings.js",
        "line": 34,
        "type": "Hardcoded Password",
        "severity": "CRITICAL"
      }
    ]
  },
  "issues": [
    "CRITICAL: Hardcoded secrets found in repository",
    "Found 3 instances of hardcoded credentials",
    "Security best practices violated"
  ],
  "recommendations": [
    "IMMEDIATELY remove all hardcoded secrets from code",
    "Rotate all exposed API keys and credentials",
    "Use environment variables for ALL sensitive data",
    "Add .env to .gitignore if not already present",
    "Review git history and remove secrets from past commits"
  ]
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** just grep in root directory
✅ **DO** search entire repository recursively

❌ **DON'T** miss secrets in subdirectories (src/, backend/, config/)
✅ **DO** scan ALL code directories

❌ **DON'T** ignore config files (config.py, settings.js, application.properties)
✅ **DO** read and analyze all configuration files

❌ **DON'T** accept commented secrets as "safe"
✅ **DO** fail on ANY hardcoded secrets, even in comments

❌ **DON'T** miss database URLs with embedded credentials
✅ **DO** check for connection strings like "postgres://user:pass@host"

❌ **DON'T** assume .env.example exists just because .env might
✅ **DO** verify .env.example actually exists with proper template

---

## Example Execution

```bash
# Step 1: Run secret scanner (CRITICAL)
python .claude/skills/3-config-security/scan_secrets.py /path/to/repo

# If secrets found: STOP, return score 0
# If no secrets: Continue

# Step 2: Check configuration
find /path/to/repo -name ".env.example"
Read /path/to/repo/.env.example

find /path/to/repo -name ".gitignore"
Read /path/to/repo/.gitignore

# Step 3: Check env variable usage
grep -r "os.getenv\|process.env" /path/to/repo --include="*.py" --include="*.js" | wc -l

# Step 4: Calculate score
# Step 5: Generate JSON output
```

---

## Security Assessment Rules

1. **Hardcoded Secrets = -2 Points Each:**
   - Each real hardcoded secret: -2 points
   - Multiple secrets can result in 0/10
   - Deductions are cumulative

2. **What Counts as a Secret (Real Credential):**
   - Real API keys (any service)
   - Real passwords (even "test123" if used in code)
   - Real access tokens
   - Real private keys
   - Real database credentials in URLs
   - Real OAuth secrets
   - Real JWT secrets

3. **What DOESN'T Count (Placeholders are OK):**
   - Placeholder text ("your_api_key_here", "INSERT_KEY_HERE", "<YOUR-KEY>")
   - Placeholder keys with obvious markers ("sk-ant-api03-YOUR-KEY-HERE")
   - Variable names (API_KEY = "..." without actual key)
   - Example keys in .env.example (if obviously fake/placeholder)
   - Documentation examples (if clearly marked as placeholders)

4. **When in Doubt:**
   - If it contains "YOUR", "PLACEHOLDER", "EXAMPLE", "INSERT": Placeholder (OK)
   - If it's clearly a template in documentation: Placeholder (OK)
   - If it looks like a real key with no placeholder indicators: Real secret (-2 points)
   - If it's a 20+ character alphanumeric string with NO placeholder markers: Real secret (-2 points)

**Remember: Placeholders in documentation are acceptable teaching tools. Real secrets are not.**

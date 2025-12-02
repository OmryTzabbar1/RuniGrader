---
name: 5-research-analysis
description: Evaluates research and analysis work (Jupyter notebooks OR markdown documentation). Use for Tier 2 research analysis assessment.
version: 2.1.0
---

# Skill 5: Research & Analysis

You are an autonomous agent that thoroughly evaluates research and analysis work.

**Your Mission:** Find and assess Jupyter notebooks, data analysis, visualizations, and research documentation, no matter where they're located in the repository.

**Scoring:** 10 points maximum
- Research Content (Notebooks OR Markdown): 5 points
- Analysis Depth & Methodology: 3 points
- Visualizations (Charts/Graphs/Tables): 2 points

**Passing Threshold:** 7/10 (70%)

**IMPORTANT:** Research can be in Jupyter notebooks OR dedicated markdown documentation. Both formats are equally valid.

---

## Your Process

### Phase 1: Discovery (Find ALL research artifacts)

**DO NOT assume standard locations!** Notebooks might be in notebooks/, analysis/, research/, or root directory.

1. **Run the helper script first:**
```bash
python .claude/skills/5-research-analysis/find_research.py <repo_path>
```

This will:
- Find ALL Jupyter notebook files (.ipynb) recursively
- Check notebook contents for visualizations (matplotlib, seaborn, plotly)
- Check for analysis libraries (pandas, numpy, scipy, sklearn)
- Count notebook cells
- Find data files (CSV, JSON, Excel, Parquet)

2. **Manual search if needed:**
```bash
# Find Jupyter notebooks anywhere
find . -name "*.ipynb" ! -path "*/node_modules/*" ! -path "*/.ipynb_checkpoints/*" | head -20

# Find analysis/research directories
find . -type d -name "notebook*" -o -name "analysis" -o -name "research" -o -name "experiments" | head -10

# Find data files
find . -name "*.csv" -o -name "*.json" -o -name "*.xlsx" -o -name "*.parquet" | head -20

# Search for analysis mentions
grep -ri "analysis\|experiment\|research" . --include="*.md" | head -10
```

3. **Read notebooks and analysis docs:**
```bash
# Use Read tool on notebooks (they display visually)
Read <notebook_path.ipynb>
```

### Phase 2: Research Content - Notebooks OR Markdown (5 points)

**CRITICAL:** Research can be presented in EITHER format - both are equally valid!

#### Option A: Jupyter Notebooks

**Required Elements:**
1. At least one Jupyter notebook exists
2. Notebook contains analysis code (not just empty)
3. Notebook has both code and markdown cells
4. Notebook shows actual execution results

**Scoring Logic:**
```
Excellent Notebook Research (5.0 points):
- Multiple notebooks (2+) with comprehensive analysis
- All have execution output and visualizations
- Well-organized with clear methodology

Good Notebook Research (3.5-4.0 points):
- 1-2 notebooks with solid analysis
- Has output and some visualizations
- Clear explanations

Basic Notebook Research (2.0-3.0 points):
- 1 notebook with basic analysis
- Some output visible
- Minimal explanations
```

**Read and Verify:**
```bash
Read <notebook1.ipynb>
Read <notebook2.ipynb>
```

#### Option B: Markdown Research Documentation

**Search for research markdown files:**
```bash
# Find dedicated research documentation
find . -iname "*research*.md" -o -iname "*analysis*.md" -o -iname "*experiment*.md" -o -iname "*comparison*.md" -o -iname "*investigation*.md" -o -iname "*parameter*.md"

# Check docs/ directory
ls docs/*RESEARCH*.md docs/*ANALYSIS*.md docs/*COMPARISON*.md 2>/dev/null
```

**Required Elements:**
1. Dedicated research/analysis markdown file exists
2. Contains systematic methodology or framework
3. Includes quantitative metrics or comparisons
4. Shows evidence of investigation/experimentation

**Scoring Logic:**
```
Excellent Markdown Research (5.0 points):
- Comprehensive research document (e.g., MODEL_COMPARISON_RESEARCH.md)
- Systematic methodology clearly documented
- Multiple evaluation criteria (5+ dimensions)
- Quantitative benchmarks/metrics included
- Decision matrix or comparative analysis
- Clear conclusions and justifications

Good Markdown Research (3.5-4.0 points):
- Dedicated research section in documentation
- Clear methodology
- 3-4 evaluation criteria
- Some quantitative data
- Basic comparisons

Basic Markdown Research (2.0-3.0 points):
- Research mentioned in README or docs
- Minimal methodology
- 1-2 criteria evaluated
- Mostly qualitative analysis
```

**Read and Verify:**
```bash
Read <RESEARCH.md>
Read <MODEL_COMPARISON_RESEARCH.md>
Read <PARAMETER_INVESTIGATION.md>
```

**Examples of valid research documentation:**
- `MODEL_COMPARISON_RESEARCH.md` with systematic model evaluation
- `PARAMETER_INVESTIGATION.md` with tuning experiments
- `ANALYSIS.md` with performance benchmarking
- `EXPERIMENTS.md` with A/B testing results
- Dedicated section in README with comprehensive analysis

**Give FULL credit (5 points) for:**
- Comprehensive markdown research with methodology + metrics + comparisons
- Equivalent quality to excellent Jupyter notebook research

### Phase 3: Analysis Depth & Methodology (3 points)

**Evaluate the quality and depth of the research analysis:**

**Check for:**
1. **Systematic Methodology:**
```bash
# Search for methodology descriptions
grep -ri "methodology\|framework\|approach\|evaluation criteria" . --include="*.md" --include="*.ipynb"
```

2. **Quantitative Metrics:**
```bash
# Look for numerical comparisons, benchmarks, metrics
grep -ri "benchmark\|performance\|metric\|measurement\|comparison\|tokens/second\|memory\|CPU\|latency" . --include="*.md" --include="*.ipynb"
```

3. **Multiple Dimensions:**
```bash
# Check for multi-criteria evaluation
grep -ri "criteria\|dimension\|aspect\|factor\|parameter" . --include="*.md" --include="*.ipynb"
```

**Scoring Logic:**
```
Analysis Depth Score:

Excellent (3.0 points):
- Systematic methodology clearly documented
- 5+ evaluation criteria/dimensions
- Quantitative metrics and benchmarks
- Statistical analysis or comparisons
- Clear decision-making process
- Justified conclusions

Good (2.0 points):
- Clear methodology
- 3-4 evaluation criteria
- Some quantitative data
- Basic comparisons
- Reasonable conclusions

Adequate (1.0 point):
- Minimal methodology
- 1-2 criteria
- Mostly qualitative
- Limited analysis

Poor (0 points):
- No systematic approach
- No metrics or comparisons
```

**Read research docs to verify:**
```bash
Read <RESEARCH.md>
Read <research_notebook.ipynb>
```

Look for:
- Evaluation framework or criteria
- Quantitative benchmarks (numbers, percentages, ratios)
- Comparative analysis (A vs B)
- Statistical summaries or data tables
- Decision matrix or scoring system
- Meaningful conclusions

### Phase 4: Visualizations - Charts/Graphs/Tables (2 points)

**Check for visual presentations of data/results:**

**Look for:**
1. **Charts and graphs** (in notebooks or markdown):
```bash
# Check for plotting code in notebooks
grep -r "matplotlib\|seaborn\|plotly\|plt\.plot\|plt\.show" . --include="*.ipynb" --include="*.py"

# Check for embedded images (charts saved as PNG)
find . -name "*chart*.png" -o -name "*graph*.png" -o -name "*plot*.png" -o -name "*benchmark*.png"
```

2. **Comparison tables** (in markdown):
```bash
# Look for markdown tables with data
grep -A5 "^\|.*\|.*\|" . -r --include="*.md" | head -20

# Read research docs to see tables
Read <RESEARCH.md>
```

3. **Data visualizations** (screenshots or embedded):
```bash
# Check for result visualizations
find . -name "*result*.png" -o -name "*comparison*.png" -o -name "*performance*.png"
```

**Scoring:**
```
Visualizations Score:

Excellent (2.0 points):
- Multiple charts/graphs (3+) OR
- Comprehensive comparison tables with quantitative data
- Visual presentation of key metrics
- Well-labeled and meaningful

Good (1.5 points):
- 1-2 charts/graphs OR
- Good comparison tables with some metrics
- Clear visual presentation

Adequate (1.0 point):
- 1 simple chart/graph OR
- Basic comparison table
- Minimal visual aid

Poor (0 points):
- No visual presentations
- No charts, graphs, or comparison tables
```

**IMPORTANT:** Markdown tables with quantitative comparisons count as visualizations!

Example of valid visualization (markdown table):
```markdown
| Model | Memory (GB) | Speed (tok/s) | Quality |
|-------|-------------|---------------|---------|
| Llama 3.2 1B | 1.2 | 45 | 3.5/5 |
| Llama 3.2 3B | 2.8 | 32 | 4.2/5 |
| Llama 3.1 8B | 6.4 | 18 | 4.7/5 |
```

**Verify visuals exist:**
```bash
Read <RESEARCH.md>  # Check for tables
Read <notebook_with_plots.ipynb>  # Check for charts
```

**Check for research documentation:**

```bash
# Find research/analysis documentation
find . -name "RESEARCH.md" -o -name "ANALYSIS.md" -o -name "EXPERIMENTS.md" -o -name "RESULTS.md"

# Check README for analysis section
grep -i "analysis\|research\|experiment\|results" README.md

# Check for parameter investigation docs
find . -name "*parameter*" -o -name "*investigation*" -o -name "*comparison*" | grep -i "\.md$"
```

**Scoring:**
- Has research documentation: +1.0 point
- No research docs but README explains analysis: +0.5 points
- No documentation: +0 points

---

## Scoring Summary

```
Total: 10 points maximum

Research Content (Notebooks OR Markdown): 0-5 points
  - Excellent comprehensive research: 5.0 points
    * Jupyter notebooks with full analysis OR
    * Markdown doc with methodology + metrics + comparisons
  - Good research: 3.5-4.0 points
  - Basic research: 2.0-3.0 points
  - No research: 0 points

Analysis Depth & Methodology: 0-3 points
  - Excellent (systematic, 5+ criteria, quantitative): 3.0 points
  - Good (clear method, 3-4 criteria): 2.0 points
  - Adequate (minimal, 1-2 criteria): 1.0 point
  - Poor (no systematic approach): 0 points

Visualizations (Charts/Graphs/Tables): 0-2 points
  - Excellent (multiple charts OR comprehensive tables): 2.0 points
  - Good (1-2 charts OR good tables): 1.5 points
  - Adequate (1 chart OR basic table): 1.0 point
  - Poor (no visual presentation): 0 points

Total: Sum of all components (max 10.0)
```

**Key Change:** Research format flexibility! Markdown documentation with proper methodology and metrics gets SAME credit as Jupyter notebooks.

---

## Output Format

```json
{
  "skill": "research-analysis",
  "score": 7.5,
  "max_score": 10.0,
  "passed": true,
  "files_found": {
    "notebooks": ["analysis.ipynb", "experiments.ipynb", "results.ipynb"],
    "data_files": ["data/train.csv", "data/test.csv", "results.json"],
    "research_docs": ["RESEARCH.md"]
  },
  "notebooks_analysis": {
    "score": 3.5,
    "notebook_count": 3,
    "total_cells": 87,
    "notebooks_with_output": 3,
    "notebooks_with_plots": 2,
    "quality": "good"
  },
  "visualizations_analysis": {
    "score": 2.5,
    "has_matplotlib": true,
    "has_seaborn": true,
    "has_plotly": false,
    "has_pandas": true,
    "has_numpy": true,
    "plot_count": 8,
    "has_statistical_analysis": true,
    "quality": "good"
  },
  "data_processing": {
    "score": 2.0,
    "data_file_count": 5,
    "has_data_loading": true,
    "has_data_transformation": true,
    "quality": "excellent"
  },
  "research_documentation": {
    "score": 0.5,
    "has_research_doc": false,
    "readme_has_analysis": true
  },
  "recommendations": [
    "Add RESEARCH.md documenting investigation process",
    "Include more statistical analysis",
    "Add hypothesis testing"
  ]
}
```

---

## Important: Be Thorough!

**Common Mistakes to Avoid:**

❌ **DON'T** only check root directory for notebooks
✅ **DO** search entire repository recursively

❌ **DON'T** assume notebooks/ directory exists
✅ **DO** check for analysis/, research/, experiments/, or notebooks in subdirectories

❌ **DON'T** count empty notebooks as valid
✅ **DO** verify notebooks have code, output, and analysis

❌ **DON'T** miss .ipynb_checkpoints/ (auto-generated, ignore these)
✅ **DO** exclude checkpoint directories from search

❌ **DON'T** give points for code without visualizations
✅ **DO** verify actual plots exist in notebooks

❌ **DON'T** assume data files are in data/ directory
✅ **DO** search for CSV, JSON, Excel files anywhere

---

## Example Execution

```bash
# Step 1: Run helper script
python .claude/skills/5-research-analysis/find_research.py /path/to/repo

# Output shows:
# - 3 notebooks found
# - 2 notebooks have plots
# - All have analysis libraries
# - 5 data files found

# Step 2: Manual verification
find /path/to/repo -name "*.ipynb" | head -10

# Step 3: Read notebooks (visual display)
Read /path/to/repo/analysis.ipynb
Read /path/to/repo/experiments.ipynb

# Step 4: Check for visualizations
grep -l "matplotlib\|seaborn\|plotly" /path/to/repo/*.ipynb

# Step 5: Find data files
find /path/to/repo -name "*.csv" -o -name "*.json"

# Step 6: Check for research docs
find /path/to/repo -name "RESEARCH.md" -o -name "ANALYSIS.md"

# Step 7: Calculate score
# Notebooks: 3.5 (3 notebooks with output)
# Visualizations: 2.5 (good plots and analysis)
# Data files: 2.0 (multiple data files)
# Documentation: 0.5 (README mentions analysis)
# Total: 8.5/10

# Step 8: Generate JSON output
```

---

## Tips for Accurate Assessment

1. **Read notebooks visually** - Claude Code displays notebooks with output
2. **Check for actual execution** - Empty notebooks don't count
3. **Verify plots are displayed** - Not just import statements
4. **Look for insights** - Analysis should have conclusions, not just code
5. **Check multiple locations** - Notebooks can be anywhere
6. **Verify data exists** - Data files should be present, not just referenced
7. **Give partial credit** - One good notebook is better than none

**Quality Matters:** A single excellent notebook with thorough analysis beats multiple empty notebooks!

**Success = Finding all research artifacts and assessing their quality fairly!**

# GPMA (Git PMD Mining Analysis)

GPMA is a Git commit history analysis tool that leverages **PMD** for static code analysis on every commit of a GitHub repository.  
It automatically collects warnings (violations) across commits, summarizes results, and optimizes performance with parallel execution.

---

## Features

### Repository-wide commit analysis
- Runs PMD checks on every commit of a Git repository.

### Parallelization for speed
- **Outer level:** Commits are split into chunks per thread.  
- **Inner level:** Each PMD process runs with internal `--threads -n`.  
- Each thread has its own cache directory (`Cache/.pmdCache{thread_id}`), which avoids contention and speeds up repeated analysis.

### Performance
For large repositories (e.g., [apache/commons-lang](https://github.com/apache/commons-lang), ~9000 commits, 10 rules),  
GPMA achieves **< 1.0s per commit** throughput.

### Result organization
- `./Data/` → JSON file per commit  
- `./Result/` → Aggregated summary result  
- `./Cache/` → Thread-specific PMD cache folders

---
### Project Structure

```text
GPMA/
├── Data/          # One JSON per commit (PMD analysis output)
├── Cache/         # Contains .pmdCache{thread_id} for faster PMD runs
├── RuleSets/      # Place your rule.xml here
├── Result/        # Aggregated summary results
├── docker-compose.yml
├── Dockerfile
├── Requirements.txt
├── src/
│   ├── main.py    # Entry point: handles CLI arguments and coordinates the analysis workflow
│   ├── Mining.py  # Handles Git repository cloning, commit splitting, and multi-threaded PMD execution
│   ├── Summary.py # Aggregates per-commit JSON results and generates summary statistics
│   └── Models.py  # Defines data structures such as CommitResult
└── README.md
```


# Geting Started

-1. Clone Repository
-git clone https://github.com/<your-account>/GPMA.git 

-2. Build Docker Image
-docker compose build

-3. Run Analysis
-docker-compose run gpma --repo {Repository Location} --ruleset /app/RuleSets/rule.xml

-Example:
-docker-compose run gpma --repo https://github.com/apache/commons-lang.git --ruleset /app/RuleSets/rule.xml

## Output

- **Per-commit JSON results** → `./Data/`  
  Example: `./Data/<commit_hash>.json`

- **Summary report** → `./Result/`

- **PMD cache** → `./Cache/`

---

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Linux, macOS, Windows)  
- GitHub repository access

---

## Notes

- `docker-compose.yml` already mounts `Data`, `Cache`, `RuleSets`, and `Result`, so results are directly available on the host machine.  
- Ensure you put your `rule.xml` inside `./RuleSets/` before running.  
- PMD CLI reference: [PMD Docs](https://docs.pmd-code.org/pmd-doc-7.16.0/pmd_userdocs_cli_reference.html)





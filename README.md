GPMA (Git PMD Mining Analysis)

GPMA is a Git commit history analysis tool that leverages PMD for static code analysis on every commit of a GitHub repository.
It automatically collects warnings (violations) across commits, summarizes results, and optimizes performance with parallel execution.

Features

Repository-wide commit analysis
Runs PMD checks on every commit of a Git repository.

Parallelization for speed

Outer level: Commits are split into chunks per thread.

Inner level: Each PMD process itself runs with internal --threads -n.

Each thread has its own cache directory (Cache/.pmdCache{thread_id}), which avoids contention and speeds up repeated analysis.

Performance
For large repositories (e.g., apache/commons-lang
, ~9000 commits, 10 rules),
GPMA achieves < 1.0s per commit throughput.

Result organization

./Data/ → JSON file per commit
./Result/ → Aggregated summary result
./Cache/ → Thread-specific PMD cache folders

Project Structure
GPMA/
├── Data/        # One JSON per commit (PMD analysis output)
├── Cache/       # Contains .pmdCache{thread_id} for faster PMD runs
├── RuleSets/    # Place your rule.xml here
├── Result/      # Aggregated summary results
├── docker-compose.yml
├── Dockerfile
├── Requirements.txt
├── src/
│   └── main.py    # Entry point: handles CLI arguments and coordinates the analysis workflow
│   ├── Mining.py  # Handles Git repository cloning, commit splitting, and multi-threaded PMD execution
│   ├── Summary.py # Aggregates per-commit JSON results and generates summary statistics
│   └── Models.py  # Defines data structures such as CommitResult 
└── README.md

Getting Started
1. Clone repository
   git clone https://github.com/won/GPMA.git

3. 






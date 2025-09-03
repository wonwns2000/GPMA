import json
import os

violation_sum = {}
def get_commit_result(commit_results,repo_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    # Ensure Result directory exists
    result_dir = os.path.join(root_dir, "Result")
    os.makedirs(result_dir, exist_ok=True)
    global violation_sum
    total_java_files_count = 0
    total_violations_count = 0
    n = len(commit_results)
    for commit_result in commit_results:
        total_java_files_count += commit_result.java_files_count
        total_violations_count += commit_result.warning_count
        for rule,count in commit_result.violations.items():
            violation_sum[rule] = violation_sum.get(rule,0) + count
    avg_of_num_java_files = round(total_java_files_count / n,2)
    avg_of_num_violations = round(total_violations_count / n,2)
    result ={
        "location": os.path.abspath(repo_path),
        "stat_of_repository":
        {
        "number of commits":n,
        "avg_of_num_java_files": avg_of_num_java_files,
        "avg_violations_count": avg_of_num_violations,
        },
        "stat_of_warnings ":  dict(violation_sum)
    }
    with open(os.path.join(root_dir,"Result", "commit_result.json"), "w") as f:
        json.dump(result, f, indent=4)
    return
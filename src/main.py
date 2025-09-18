# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import shutil
import argparse
import datetime
import Mining
import Summary
import sys
import subprocess
def parse_args():
    parser = argparse.ArgumentParser(description="Run PMD analysis")
    parser.add_argument("--repo", required=True, help="Repository URL or local path")
    parser.add_argument("--ruleset", required=True, help="Ruleset XML file path")
    parser.add_argument("--threads", type=int, default=4)
    return parser.parse_args()




def main():

    # input repository_path
    args = parse_args()
    input_repo = args.repo
    ruleset_path = args.ruleset
    max_threads = args.threads
    Mining.replace_pmd_baseurl_in_ruleset_inplace(ruleset_path, "https://pmd.github.io/pmd")
    Mining.validate_inputs(input_repo, ruleset_path)
    # prepare temp repository
    repo_path, is_temp = Mining.prepare_repo(input_repo)
    # Mining.thread_analysis(repo_path, ruleset_path,commits_hash,cache_path)
    try:

        start_time = datetime.datetime.now()
        print("Start PMD analysis")
        #result = Mining.one_thread_pmd_v0(repo_path, ruleset_path)
        result = Mining.multi_thread_pmd(repo_path, ruleset_path, max_threads)
        Summary.get_commit_result(result, input_repo)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print(f"Total time : {elapsed_time.total_seconds():.2f} seconds")
    except Exception as e:
        print(e)
    finally:
        try:
            if is_temp:
                shutil.rmtree(repo_path)
        except PermissionError as e:
            print(e)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

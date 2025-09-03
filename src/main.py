# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import shutil

import git
import datetime
import Mining
import Summary


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def main():

    # input repository_path
    input_repo = "https://github.com/apache/commons-lang.git"
    # ruleset_path
    ruleset_path = r'./Rulesets/rule.xml'
    # prepare temp repository
    repo_path, is_temp = Mining.prepare_repo(input_repo)
    # Mining.thread_analysis(repo_path, ruleset_path,commits_hash,cache_path)
    try:

        start_time = datetime.datetime.now()
        print("Start PMD analysis")
        #result = Mining.one_thread_pmd_v0(repo_path, ruleset_path)
        result = Mining.multi_thread_pmd(repo_path, ruleset_path, max_threads=4)
        Summary.get_commit_result(result, repo_path)
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

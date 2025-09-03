import json
import shutil
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory

import git
import datetime
import git.exc
import subprocess
import os
from pathlib import Path
import threading
from Models import CommitResult

total_java_files_count = 0
lock = threading.Lock()

def prepare_repo(repo_input):
    if repo_input.startswith("http://") or repo_input.startswith("https://") or repo_input.startswith("git@"):
        temp_dir = tempfile.mkdtemp(prefix="repo_clone_")
        print(f"Cloning {repo_input} to {temp_dir} ...")
        git.Repo.clone_from(repo_input, temp_dir)
        return temp_dir, True  
    else:
        if not os.path.exists(repo_input):
            raise FileNotFoundError(f"Local repo path {repo_input} does not exist.")
        return repo_input, False
def get_commits_hash(filepath,branch = "--all"):
    commits_hash = []
    repo = git.Repo(filepath)
    for commit in repo.iter_commits(branch):
        commits_hash.append(commit.hexsha)
    #print("commit_amt",len(commits_hash))
    return commits_hash

def run_pmd_command(repo_path, ruleset_path, output_path,cache_path):
    start_time = datetime.datetime.now()
    cache_path = os.path.join(cache_path, "pmdCache")
    cmd = [
        "pmd" ,
        "check",
        "-d", repo_path,
        "-R", ruleset_path,
        "-f", "json",
        "-r", output_path,
        "--cache", cache_path,
        "--threads", "4"
    ]
    subprocess.run(cmd,shell=True)
    end_time = datetime.datetime.now()
    print(f"Committing took {(end_time-start_time).total_seconds():.2f} seconds")
    
def one_thread_pmd(commits_hash,repo_path,ruleset_path,thread_id,temp_repo_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    cache_path = os.path.join(root_dir,"Cache",f".pmdCache{thread_id}")
    
    # Ensure Data directory exists
    # os.makedirs(data_dir, exist_ok=True)
    # data_dir = os.path.join(root_dir, "Data")
    
    #Copy the repo
    thread_dir = os.path.join(temp_repo_dir,f".thread{thread_id}")
    
    git.Repo.clone_from(repo_path, thread_dir)
    repo = git.Repo(thread_dir)
    commit_results=[]
    try:
        for commit_hash in commits_hash:
            repo.git.checkout(commit_hash,force=True)
            java_files_total = 0
            warning_total = 0
            filename = f"{commit_hash}.json"
            output_path = os.path.join(root_dir, "Data", filename)
            java_files_total+= len(list(Path(thread_dir).rglob("*.java")))
            run_pmd_command(thread_dir,ruleset_path,output_path,cache_path)
            with open(output_path, "r", encoding="utf-8") as f:
                result = json.load(f)
            for f in result["files"]:
                warning_total += len(f["violations"])
            commit_result = CommitResult(commit_hash, warning_total, java_files_total)
            for files in result["files"]:
                for violation in files["violations"]:
                    commit_result.add_violation(violation["rule"])
            commit_results.append(commit_result)
    except Exception as e:
        print(f"thread_{thread_id} thread error as {e}")
        
    return commit_results

def multi_thread_pmd(repo_path,ruleset_path,max_threads=8):
    commits_hash = get_commits_hash(repo_path)[:10]
    commit_chunks = [commits_hash[i::max_threads] for i in range(max_threads)]
    all_results = []
    with tempfile.TemporaryDirectory(prefix="repo_temp_") as temp_repo_dir:    
        git.Repo.clone_from(repo_path,temp_repo_dir)
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            for thread_id,commit_chunk in enumerate(commit_chunks):
                if not commit_chunk:
                    continue
                futures.append(executor.submit(one_thread_pmd, commit_chunk,repo_path,ruleset_path,thread_id,temp_repo_dir))
            for future in futures:
                result = future.result()
                all_results.extend(result)
    return all_results






def one_thread_pmd_v0(repo_path, ruleset_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo = git.Repo(repo_path)
    root_dir = os.path.dirname(current_dir)
    commits_hash = get_commits_hash(repo_path)[:1000]
    cache_path = os.path.join(root_dir, "Data", ".pmd_cache")
    # Ensure Data directory exists
    data_dir = os.path.join(root_dir, "Data")
    os.makedirs(data_dir, exist_ok=True)
    commit_results = []

    for commit_hash in commits_hash:
        java_files_total = 0
        warning_total = 0
        filename = f"{commit_hash}.json"
        repo.git.checkout(commit_hash)
        output_path = os.path.join(root_dir, "Data", filename)
        java_files = list(Path(repo_path).rglob("*.java"))
        java_files_total+= len(java_files)
        run_pmd_command(repo_path, ruleset_path, output_path,cache_path)
        result = json.load(open(output_path))
        for f in result["files"]:
            warning_total += len(f["violations"])
        commit_result = CommitResult(commit_hash,warning_total,java_files_total)
        for files in result["files"]:
            for violation in files["violations"]:
                commit_result.add_violation(violation["rule"])
        commit_results.append(commit_result)
        #commit_result.output()

    return commit_results




#
# def copy_java_files(repo_path,commit_hash,temp_dir):
#     repo = git.Repo(repo_path)
#     commit = repo.commit(commit_hash)
#     repo.git.worktree("add","-f",temp_dir,commit_hash)
# def thread_analysis_java_files(ruleset_path,repo_path,commit_hash,temp_worktree,cache_path):
#     # Prepare PMD analysis
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     root_dir = os.path.dirname(current_dir)
#     filename = f"{commit_hash}.json"
#     output_path = os.path.join(root_dir, "Data", filename)
#     try:
#         copy_java_files(repo_path,commit_hash,temp_worktree)
#         if os.path.exists(output_path):
#             print(f"Skipping commit {commit_hash[:7]}, JSON already exists.")
#             return
#         #start PMD analysis
#         with lock:
#             run_pmd_command(temp_worktree, ruleset_path, output_path,cache_path)
#         try:
#             if os.path.exists(temp_worktree):
#                 shutil.rmtree(temp_worktree)
#         except Exception as e:
#             print(f"Error cleaning up worktree for commit {commit_hash[:7]}: {e}")
#     except Exception as e:
#         print("Copy file error: ",e)
#
# def thread_analysis(repo_path, ruleset_path,commits_hash,cache_path,max_threads = 10):
#     print(f"Commit hash:",commits_hash)
#     temp_worktrees = []
#     for commit_hash in commits_hash:
#         temp_worktree = tempfile.mkdtemp(prefix=f"tempdir_{commit_hash[:7]}")
#         temp_worktrees.append((commit_hash,temp_worktree))
#     with ThreadPoolExecutor(max_workers=max_threads) as executor:
#         for commit_hash,temp_worktree in temp_worktrees:
#             executor.submit(thread_analysis_java_files,ruleset_path,repo_path,commit_hash,temp_worktree,cache_path)
#     print("PMD Analysis complete!")
#









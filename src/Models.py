import git
import os
import dataclasses
from dataclasses import dataclass
class CommitResult:
    commit_hash:str
    warning_count:int = 0
    java_files_count: int = 0
    violations = {}
    def __init__(self, commit_hash, warning_count=0, java_files_count=0, violations=None):
        if violations is None:
            violations = {}
        self.commit_hash = commit_hash
        self.warning_count = warning_count
        self.java_files_count = java_files_count
        self.violations = violations
    def add_violation(self, rule):
        if rule not in self.violations:
            self.violations[rule] = 0
        self.violations[rule] += 1
    def output(self):
        print("results:")
        print("commit_hash:",self.commit_hash)
        print("warning_count:",self.warning_count)
        print("java_files:",self.java_files_count)
        print("violation_rules:",self.violations)
    def get_warning_count(self):
        return self.warning_count
    def get_java_files_count(self):
        return self.java_files_count
    def get_violations(self):
        return self.violations
    def get_commit_hash(self):
        return self.commit_hash

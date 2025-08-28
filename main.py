# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import git

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    repo = git.Repo(r'D:\Projects\30-seconds-of-java')
    commit_dict = json.loads(
        repo.git.log('--pretty=format:{"commit":"%h", "date":"%cd", "summary":"%s"}', date='format:%Y%m%d',max_count = 1))
    print(commit_dict)


# See PyCharm help at https://www.jetbrains.com/help/pycharm
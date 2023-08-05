from datetime import timedelta
from retry import retry
from github import Github
import os
import time


@retry(exceptions=Exception, tries=3, delay=2, backoff=2)
def download_github_file(token, repo_name, filename):
    # 獲取當前工作目錄路徑
    cwd = os.path.abspath(os.getcwd())

    # 使用 token 連接 Github API
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(repo_name)

    # 獲取檔案內容
    file_content = repo.get_contents(filename)
    file_content_str = file_content.decoded_content.decode("utf-8")

    # 寫入本地檔案
    with open(os.path.join(cwd, filename), "w") as f:
        f.write(file_content_str)

    print(f"{filename} downloaded")


@retry(exceptions=Exception, tries=3, delay=2, backoff=2)
def update_github_file(token, repo_name, filename):
    # 獲取當前工作目錄路徑
    cwd = os.path.abspath(os.getcwd())

    # 使用 token 連接 Github API
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(repo_name)

    # 獲取倉庫中所有檔案的路徑
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(file.path)

    # 讀取本地檔案的內容
    with open(os.path.join(cwd, filename), "r") as f:
        content = f.read()

    # 判斷檔案是否已存在於倉庫中
    git_file = filename
    if git_file in all_files:
        # 如果已存在，更新檔案內容並提交更改
        file = repo.get_contents(git_file)
        repo.update_file(file.path, "Update files", content, file.sha)
        print(f"{git_file} updated")
    else:
        # 如果不存在，建立新檔案並提交
        repo.create_file(git_file, "Create files", content)
        print(f"{git_file} created")


def get_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = timedelta(seconds=end_time - start_time)
        ms = int(elapsed_time.total_seconds() * 1000)
        print("Function {} took {} ms to execute.".format(func.__name__, ms))
        return result

    return wrapper
